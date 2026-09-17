#!/usr/bin/env python3
"""
Harness de evaluación para mecanica-social-ia.

Contrato: evaluations/harness.md
- Mide y reporta; no otorga aprobación institucional.
- Modo offline: validación estructural (componente + suite).
- Modo model: llama a un proveedor vía src/ms_ia (secretos solo por env).
- apto_para_aprobacion_operativa es siempre false en este harness.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

try:
    import yaml
except ImportError:  # pragma: no cover
    print(
        "ERROR: se requiere PyYAML. Instale con: pip install pyyaml",
        file=sys.stderr,
    )
    sys.exit(2)

REPO_ROOT = Path(__file__).resolve().parent.parent
SRC_ROOT = REPO_ROOT / "src"
if str(SRC_ROOT) not in sys.path:
    sys.path.insert(0, str(SRC_ROOT))

CAMPOS_COMPONENTE_MINIMOS = (
    "id",
    "version",
    "estado",
    "proposito",
    "nivel_riesgo",
    "datos_prohibidos",
    "prompt_text",
)
CAMPOS_JSON_INTAKE = ("nombre", "email", "telefono", "interes")


def load_yaml(path: Path) -> Any:
    with path.open(encoding="utf-8") as fh:
        data = yaml.safe_load(fh)
    if data is None:
        raise ValueError(f"YAML vacío: {path}")
    return data


def _as_expected_obj(expected: Any) -> tuple[dict[str, Any] | None, str | None]:
    """Normaliza expected a dict JSON-like."""
    if isinstance(expected, dict):
        return expected, None
    if isinstance(expected, str):
        try:
            obj = json.loads(expected)
        except json.JSONDecodeError as exc:
            return None, f"expected no es JSON válido: {exc}"
        if not isinstance(obj, dict):
            return None, "expected JSON debe ser un objeto"
        return obj, None
    return None, "expected debe ser objeto o string JSON"


def _parse_model_json(text: str) -> tuple[dict[str, Any] | None, str | None]:
    """Extrae un objeto JSON de la salida del modelo (raw o en fence)."""
    if not text or not str(text).strip():
        return None, "salida vacía"
    raw = str(text).strip()
    try:
        obj = json.loads(raw)
        if isinstance(obj, dict):
            return obj, None
        return None, "JSON no es objeto"
    except json.JSONDecodeError:
        pass
    fence = re.search(r"```(?:json)?\s*(\{.*?\})\s*```", raw, re.DOTALL | re.IGNORECASE)
    if fence:
        try:
            obj = json.loads(fence.group(1))
            if isinstance(obj, dict):
                return obj, None
        except json.JSONDecodeError as exc:
            return None, f"JSON en fence inválido: {exc}"
    start = raw.find("{")
    end = raw.rfind("}")
    if start >= 0 and end > start:
        try:
            obj = json.loads(raw[start : end + 1])
            if isinstance(obj, dict):
                return obj, None
            return None, "JSON embebido no es objeto"
        except json.JSONDecodeError as exc:
            return None, f"JSON embebido inválido: {exc}"
    return None, "no se encontró objeto JSON en la salida"


def _norm_val(value: Any) -> str:
    if value is None:
        return ""
    return " ".join(str(value).strip().lower().split())


def _field_match(expected: Any, actual: Any) -> bool:
    return _norm_val(expected) == _norm_val(actual)


def _no_invention(
    input_text: str, output_obj: dict[str, Any], marker: str = "NO_PROPORCIONADO"
) -> bool:
    """Heurística: valores no marcador deben anclarse en el input."""
    blob = _norm_val(input_text)
    for key, val in output_obj.items():
        if val is None:
            continue
        s = str(val).strip()
        if not s or s == marker:
            continue
        token = _norm_val(s)
        if len(token) < 3:
            continue
        if key in {"email", "telefono"}:
            compact_blob = blob.replace(" ", "")
            compact_tok = token.replace(" ", "")
            if compact_tok and compact_tok not in compact_blob and token not in blob:
                return False
            continue
        parts = [
            p for p in re.split(r"[^\w@.+-]+", token, flags=re.UNICODE) if len(p) >= 4
        ]
        if not parts:
            if token not in blob:
                return False
            continue
        for p in parts:
            if p not in blob:
                return False
    return True


def validate_component(component: dict[str, Any], path: Path) -> list[dict[str, Any]]:
    findings: list[dict[str, Any]] = []
    for field in CAMPOS_COMPONENTE_MINIMOS:
        ok = field in component and component[field] not in (None, "")
        findings.append(
            {
                "check": f"campo_componente:{field}",
                "ok": bool(ok),
                "detalle": None if ok else f"Falta o vacío en {path.name}",
            }
        )

    riesgo = str(component.get("nivel_riesgo", "")).lower()
    findings.append(
        {
            "check": "nivel_riesgo_valido",
            "ok": riesgo in {"bajo", "medio", "alto"},
            "detalle": None
            if riesgo in {"bajo", "medio", "alto"}
            else f"valor inválido: {component.get('nivel_riesgo')!r}",
        }
    )

    estado = str(component.get("estado", "")).lower()
    estados_ok = {
        "borrador",
        "prueba",
        "aprobado",
        "restringido",
        "obsoleto",
        "suspendido",
        "retirado",
        "draft",
        "testing",
        "approved",
        "deprecated",
        "archived",
    }
    findings.append(
        {
            "check": "estado_valido",
            "ok": estado in estados_ok,
            "detalle": None if estado in estados_ok else f"estado desconocido: {estado!r}",
        }
    )

    ejemplos = component.get("ejemplos") or []
    if not isinstance(ejemplos, list):
        findings.append(
            {
                "check": "ejemplos_lista",
                "ok": False,
                "detalle": "ejemplos debe ser lista",
            }
        )
        ejemplos = []
    else:
        findings.append({"check": "ejemplos_lista", "ok": True, "detalle": None})

    for i, ej in enumerate(ejemplos):
        if not isinstance(ej, dict):
            findings.append(
                {
                    "check": f"ejemplo_{i}",
                    "ok": False,
                    "detalle": "ejemplo no es objeto",
                }
            )
            continue
        has_io = "input" in ej and "expected" in ej
        obj, err = (
            _as_expected_obj(ej.get("expected")) if has_io else (None, "faltan input/expected")
        )
        ok = has_io and obj is not None
        findings.append(
            {
                "check": f"ejemplo_{i}_estructura",
                "ok": ok,
                "detalle": err,
            }
        )
        if ok and obj is not None:
            missing = [c for c in CAMPOS_JSON_INTAKE if c not in obj]
            findings.append(
                {
                    "check": f"ejemplo_{i}_campos",
                    "ok": not missing,
                    "detalle": None if not missing else f"faltan campos: {missing}",
                }
            )

    return findings


def validate_suite(
    suite: dict[str, Any], path: Path
) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    findings: list[dict[str, Any]] = []
    case_results: list[dict[str, Any]] = []

    for field in ("id", "version", "componente_objetivo", "casos"):
        ok = field in suite and suite[field] not in (None, "")
        findings.append(
            {
                "check": f"campo_suite:{field}",
                "ok": bool(ok),
                "detalle": None if ok else f"Falta en {path.name}",
            }
        )

    clasif = str(suite.get("datos_clasificacion", "")).lower()
    findings.append(
        {
            "check": "datos_clasificacion",
            "ok": clasif in {"sintetica", "publica", "autorizada"},
            "detalle": None if clasif else "sin clasificación",
        }
    )

    casos = suite.get("casos") or []
    if not isinstance(casos, list) or not casos:
        findings.append(
            {
                "check": "casos_no_vacios",
                "ok": False,
                "detalle": "la suite no tiene casos",
            }
        )
        return findings, case_results

    findings.append({"check": "casos_no_vacios", "ok": True, "detalle": None})

    ids: set[str] = set()
    required = suite.get("campos_requeridos") or list(CAMPOS_JSON_INTAKE)

    for caso in casos:
        if not isinstance(caso, dict):
            case_results.append(
                {
                    "caso_id": None,
                    "ok": False,
                    "checks": ["caso_no_objeto"],
                    "detalle": "caso inválido",
                }
            )
            continue

        cid = caso.get("id")
        checks: list[dict[str, Any]] = []
        ok = True

        if not cid or cid in ids:
            checks.append({"check": "id_unico", "ok": False})
            ok = False
        else:
            checks.append({"check": "id_unico", "ok": True})
            ids.add(str(cid))

        if not caso.get("input"):
            checks.append({"check": "input_presente", "ok": False})
            ok = False
        else:
            checks.append({"check": "input_presente", "ok": True})

        obj, err = _as_expected_obj(caso.get("expected"))
        if obj is None:
            checks.append({"check": "expected_json", "ok": False, "detalle": err})
            ok = False
        else:
            checks.append({"check": "expected_json", "ok": True})
            missing = [c for c in required if c not in obj]
            if missing:
                checks.append(
                    {
                        "check": "campos_requeridos",
                        "ok": False,
                        "detalle": f"faltan: {missing}",
                    }
                )
                ok = False
            else:
                checks.append({"check": "campos_requeridos", "ok": True})

        case_results.append(
            {
                "caso_id": cid,
                "ok": ok,
                "tags": caso.get("tags") or [],
                "checks": checks,
            }
        )

    return findings, case_results


def _render_prompt(prompt_text: str, user_input: str) -> str:
    text = prompt_text or ""
    replacements = {
        "{{ texto_formulario }}": user_input,
        "{{texto_formulario}}": user_input,
        "{{ input }}": user_input,
        "{{input}}": user_input,
    }
    out = text
    for k, v in replacements.items():
        out = out.replace(k, v)
    return out


def run_model_cases(
    component: dict[str, Any],
    suite: dict[str, Any],
    model_cfg: dict[str, Any],
    max_cases: int | None = None,
) -> tuple[list[dict[str, Any]], dict[str, Any]]:
    """Ejecuta casos contra el modelo. Devuelve (case_results, stats)."""
    from ms_ia.model_client import ModelClientError, build_client_from_model_config

    try:
        client = build_client_from_model_config(model_cfg)
    except ModelClientError as exc:
        raise ModelClientError(f"ERROR modo model: {exc}") from exc

    temperature = float(
        model_cfg.get("temperature") if model_cfg.get("temperature") is not None else 0
    )
    max_tokens = int(model_cfg.get("max_tokens") or 512)
    required = suite.get("campos_requeridos") or list(CAMPOS_JSON_INTAKE)
    marker = str(suite.get("marcador_faltante") or "NO_PROPORCIONADO")
    prompt_text = str(component.get("prompt_text") or "")

    casos = list(suite.get("casos") or [])
    if max_cases is not None:
        casos = casos[: max(0, max_cases)]

    results: list[dict[str, Any]] = []
    totals = {
        "n": 0,
        "json_ok": 0,
        "campos_ok": 0,
        "exact_fields": 0,
        "exact_fields_total": 0,
        "no_invencion_ok": 0,
        "caso_ok": 0,
    }

    for caso in casos:
        if not isinstance(caso, dict):
            continue
        cid = caso.get("id")
        user_input = str(caso.get("input") or "")
        expected, exp_err = _as_expected_obj(caso.get("expected"))
        checks: list[dict[str, Any]] = []
        ok = True
        output_obj: dict[str, Any] | None = None
        raw_text = ""
        error = None

        totals["n"] += 1

        if expected is None:
            checks.append({"check": "expected_json", "ok": False, "detalle": exp_err})
            ok = False
        else:
            checks.append({"check": "expected_json", "ok": True})

        try:
            system_prompt = prompt_text
            completion = client.complete(
                system_or_prompt=system_prompt,
                user_input=user_input,
                temperature=temperature,
                max_tokens=max_tokens,
            )
            raw_text = completion.text
            output_obj, parse_err = _parse_model_json(raw_text)
            if output_obj is None:
                checks.append({"check": "json_valido", "ok": False, "detalle": parse_err})
                ok = False
            else:
                checks.append({"check": "json_valido", "ok": True})
                totals["json_ok"] += 1
                missing = [c for c in required if c not in output_obj]
                if missing:
                    checks.append(
                        {
                            "check": "campos_requeridos_presentes",
                            "ok": False,
                            "detalle": f"faltan: {missing}",
                        }
                    )
                    ok = False
                else:
                    checks.append({"check": "campos_requeridos_presentes", "ok": True})
                    totals["campos_ok"] += 1

                if expected is not None and output_obj is not None:
                    field_hits = 0
                    field_total = 0
                    for key, exp_v in expected.items():
                        field_total += 1
                        act_v = output_obj.get(key)
                        hit = _field_match(exp_v, act_v)
                        if hit:
                            field_hits += 1
                        checks.append(
                            {
                                "check": f"campo:{key}",
                                "ok": hit,
                                "detalle": None
                                if hit
                                else f"esperado≈{exp_v!r} obtenido≈{act_v!r}",
                            }
                        )
                        if not hit:
                            ok = False
                    totals["exact_fields"] += field_hits
                    totals["exact_fields_total"] += field_total

                    inv_ok = _no_invention(user_input, output_obj, marker=marker)
                    checks.append({"check": "no_invencion", "ok": inv_ok})
                    if inv_ok:
                        totals["no_invencion_ok"] += 1
                    else:
                        ok = False
        except Exception as exc:  # noqa: BLE001
            error = str(exc)
            checks.append({"check": "llamada_modelo", "ok": False, "detalle": error})
            ok = False

        if ok:
            totals["caso_ok"] += 1

        results.append(
            {
                "caso_id": cid,
                "ok": ok,
                "tags": caso.get("tags") or [],
                "checks": checks,
                "salida_modelo": output_obj,
                "error": error,
                "salida_preview": (raw_text[:500] + "…")
                if len(raw_text) > 500
                else raw_text or None,
            }
        )

    return results, totals


def build_result(
    component: dict[str, Any],
    component_path: Path,
    suite: dict[str, Any],
    suite_path: Path,
    comp_findings: list[dict[str, Any]],
    suite_findings: list[dict[str, Any]],
    case_results: list[dict[str, Any]],
    ejecutado_por: str,
    *,
    mode: str = "offline",
    model_ref: str | None = None,
    model_stats: dict[str, Any] | None = None,
) -> dict[str, Any]:
    n_casos = len(case_results)
    n_pass = sum(1 for c in case_results if c.get("ok"))
    n_fail = n_casos - n_pass
    structural_ok = all(f.get("ok") for f in comp_findings + suite_findings)

    if mode == "offline":
        thresholds_ok = structural_ok and n_fail == 0 and n_casos > 0
        tasa = (n_pass / n_casos * 100.0) if n_casos else 0.0
        metricas = [
            {
                "id": "esquema_componente_valido",
                "nombre": "Esquema de componente válido",
                "valor": all(f.get("ok") for f in comp_findings),
                "unidad": "booleano",
                "umbral": True,
                "umbral_cumplido": all(f.get("ok") for f in comp_findings),
                "metodo": "validación offline de campos mínimos",
                "n_casos": 0,
                "limitaciones": "No evalúa calidad del modelo",
            },
            {
                "id": "json_valido",
                "nombre": "Expected de casos es JSON objeto válido",
                "valor": round(tasa, 2),
                "unidad": "porcentaje",
                "umbral": 100,
                "umbral_cumplido": n_fail == 0 and n_casos > 0,
                "metodo": "parseo de expected en suite",
                "n_casos": n_casos,
                "limitaciones": "Valida fixtures, no salidas del modelo",
            },
            {
                "id": "campos_requeridos_presentes",
                "nombre": "Campos requeridos en expected",
                "valor": round(tasa, 2),
                "unidad": "porcentaje",
                "umbral": 100,
                "umbral_cumplido": n_fail == 0 and n_casos > 0,
                "metodo": "presencia de claves en expected",
                "n_casos": n_casos,
                "limitaciones": "No compara con output de modelo",
            },
        ]
        alcance = "estructural"
        notas = (
            "Corrida offline estructural. No llama a modelos. "
            "No constituye evidencia de exactitud de extracción ni aprobación operativa."
        )
        limitaciones = [
            "Modo offline: no evalúa el comportamiento del modelo.",
            "Los expected son fixtures sintéticas, no predicciones.",
            "apto_para_aprobacion_operativa es siempre false en este modo.",
        ]
    else:
        stats = model_stats or {}
        n = stats.get("n") or n_casos or 1
        json_rate = (stats.get("json_ok", 0) / n) * 100.0
        campos_rate = (stats.get("campos_ok", 0) / n) * 100.0
        inv_rate = (stats.get("no_invencion_ok", 0) / n) * 100.0
        ef = stats.get("exact_fields", 0)
        eft = stats.get("exact_fields_total", 0) or 1
        exact_rate = (ef / eft) * 100.0
        caso_rate = (stats.get("caso_ok", 0) / n) * 100.0
        tasa = caso_rate

        json_ok = json_rate >= 100.0
        campos_ok = campos_rate >= 95.0
        exact_ok = exact_rate >= 95.0
        inv_ok = inv_rate >= 100.0
        thresholds_ok = (
            structural_ok and json_ok and campos_ok and exact_ok and inv_ok and n_casos > 0
        )

        metricas = [
            {
                "id": "esquema_componente_valido",
                "nombre": "Esquema de componente válido",
                "valor": all(f.get("ok") for f in comp_findings),
                "unidad": "booleano",
                "umbral": True,
                "umbral_cumplido": all(f.get("ok") for f in comp_findings),
                "metodo": "validación de campos mínimos",
                "n_casos": 0,
                "limitaciones": "Precheck estructural",
            },
            {
                "id": "json_valido",
                "nombre": "Salida del modelo es JSON objeto válido",
                "valor": round(json_rate, 2),
                "unidad": "porcentaje",
                "umbral": 100,
                "umbral_cumplido": json_ok,
                "metodo": "parseo de salida del modelo",
                "n_casos": n_casos,
                "limitaciones": "Acepta JSON en fences markdown",
            },
            {
                "id": "campos_requeridos_presentes",
                "nombre": "Campos requeridos en salida del modelo",
                "valor": round(campos_rate, 2),
                "unidad": "porcentaje",
                "umbral": 95,
                "umbral_cumplido": campos_ok,
                "metodo": "presencia de claves en salida",
                "n_casos": n_casos,
                "limitaciones": "No valida tipos semánticos ricos",
            },
            {
                "id": "exactitud_extraccion",
                "nombre": "Exactitud de campos vs expected",
                "valor": round(exact_rate, 2),
                "unidad": "porcentaje",
                "umbral": 95,
                "umbral_cumplido": exact_ok,
                "metodo": "comparación normalizada campo a campo",
                "n_casos": n_casos,
                "limitaciones": "Normalización simple; sin sinónimos",
            },
            {
                "id": "no_invencion",
                "nombre": "Sin invención evidente respecto al input",
                "valor": round(inv_rate, 2),
                "unidad": "porcentaje",
                "umbral": 100,
                "umbral_cumplido": inv_ok,
                "metodo": "heurística de substrings sobre input",
                "n_casos": n_casos,
                "limitaciones": "Heurística; requiere muestreo humano",
            },
        ]
        alcance = "modelo"
        notas = (
            "Corrida con modelo. Secretos solo por entorno. "
            "No constituye aprobación operativa ni autorización de proveedor productivo."
        )
        limitaciones = [
            "Modo model: evalúa salidas del proveedor configurado en el entorno.",
            "apto_para_aprobacion_operativa es siempre false en este harness.",
            "Heurística no_invencion no reemplaza revisión humana.",
            "El slot de modelo puede estar en estado propuesto (ver model-card).",
        ]

    now = datetime.now(timezone.utc)
    resultado_id = f"eval-{now.strftime('%Y%m%d')}-{mode}"
    rel_comp = (
        str(component_path.relative_to(REPO_ROOT))
        if component_path.is_relative_to(REPO_ROOT)
        else str(component_path)
    )
    rel_suite = (
        str(suite_path.relative_to(REPO_ROOT))
        if suite_path.is_relative_to(REPO_ROOT)
        else str(suite_path)
    )

    return {
        "schema_version": "1.0.0",
        "resultado_id": resultado_id,
        "fecha_utc": now.strftime("%Y-%m-%dT%H:%M:%SZ"),
        "componente": {
            "tipo": "prompt",
            "id": component.get("id"),
            "version": component.get("version"),
            "ruta": rel_comp,
            "nivel_riesgo_declarado": component.get("nivel_riesgo"),
            "estado_declarado": component.get("estado"),
        },
        "suite": {
            "id": suite.get("id"),
            "version": suite.get("version"),
            "ruta": rel_suite,
            "n_casos": n_casos,
        },
        "ejecucion": {
            "modo": mode,
            "harness_ref": "evaluations/harness.md",
            "modelo_ref": model_ref,
            "entorno": "local",
            "semilla": None,
            "ejecutado_por": ejecutado_por,
            "notas": notas,
        },
        "metricas": metricas,
        "resumen": {
            "n_casos": n_casos,
            "n_pasados": n_pass,
            "n_fallidos": n_fail,
            "tasa_exito_primaria": round(tasa, 2),
            "umbrales_obligatorios_ok": thresholds_ok,
            "alcance": alcance,
            "apto_para_aprobacion_operativa": False,
        },
        "validacion_estructural": {
            "componente": comp_findings,
            "suite": suite_findings,
        },
        "casos_detalle": case_results,
        "limitaciones": limitaciones,
        "decision_institucional": {
            "estado": "no_aplicable",
            "referencia": None,
            "notas": "La decisión vive en gobernanza (PR/registro); no la inventa el harness.",
        },
    }


def _resolve_model_ref(model_ref: str | None) -> tuple[Path, dict[str, Any], str]:
    ref = model_ref or "models/openai-compatible-eval"
    path = Path(ref)
    if not path.is_absolute():
        path = (REPO_ROOT / path).resolve()
    cfg_path = path / "config.yaml" if path.is_dir() else path
    if not cfg_path.exists():
        raise FileNotFoundError(
            f"No se encontró config de modelo en {cfg_path}. "
            "Cree models/<id>/config.yaml o pase --model-ref"
        )
    cfg = load_yaml(cfg_path)
    if not isinstance(cfg, dict):
        raise ValueError("config de modelo debe ser un objeto YAML")
    rel = (
        str(cfg_path.parent.relative_to(REPO_ROOT))
        if cfg_path.parent.is_relative_to(REPO_ROOT)
        else str(cfg_path.parent)
    )
    return cfg_path, cfg, rel


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Harness de mecanica-social-ia (no aprueba uso operativo)."
    )
    parser.add_argument(
        "--component",
        required=True,
        help="Ruta al YAML del componente (p. ej. prompts/formulario-intake-v1.0.0.yaml)",
    )
    parser.add_argument(
        "--suite",
        required=True,
        help="Ruta a la suite YAML (p. ej. evaluations/casos-prueba/intake-test-set.yaml)",
    )
    parser.add_argument(
        "--mode",
        default="offline",
        choices=["offline", "model"],
        help="offline = estructural; model = llama al proveedor (secretos por env)",
    )
    parser.add_argument(
        "--model-ref",
        default=None,
        help="Ruta a models/<id> (default: models/openai-compatible-eval)",
    )
    parser.add_argument(
        "--config",
        default=None,
        help="YAML de config de corrida no sensible (opcional; ver config.example.yaml)",
    )
    parser.add_argument(
        "--max-cases",
        type=int,
        default=None,
        help="Limitar número de casos (útil en pruebas)",
    )
    parser.add_argument(
        "--output",
        default="evaluations/resultados",
        help="Directorio de salida para el JSON de resultado",
    )
    parser.add_argument(
        "--ejecutado-por",
        default=None,
        help="Identificador de quien ejecuta la corrida",
    )
    args = parser.parse_args(argv)

    run_cfg: dict[str, Any] = {}
    if args.config:
        cfg_path = Path(args.config)
        if not cfg_path.is_absolute():
            cfg_path = (REPO_ROOT / cfg_path).resolve()
        loaded = load_yaml(cfg_path)
        if isinstance(loaded, dict):
            run_cfg = loaded

    mode = args.mode or run_cfg.get("mode") or "offline"
    model_ref = args.model_ref or run_cfg.get("model_ref")
    max_cases = args.max_cases if args.max_cases is not None else run_cfg.get("max_cases")
    ejecutado_por = args.ejecutado_por or (
        "harness-model" if mode == "model" else "harness-offline"
    )

    if mode not in {"offline", "model"}:
        print(f"ERROR: modo no soportado: {mode}", file=sys.stderr)
        return 2

    component_path = Path(args.component).resolve()
    suite_path = Path(args.suite).resolve()
    output_dir = Path(args.output)
    if not output_dir.is_absolute():
        output_dir = (REPO_ROOT / output_dir).resolve()

    try:
        component = load_yaml(component_path)
        suite = load_yaml(suite_path)
    except Exception as exc:  # noqa: BLE001
        print(f"ERROR al cargar YAML: {exc}", file=sys.stderr)
        return 2

    if not isinstance(component, dict) or not isinstance(suite, dict):
        print(
            "ERROR: componente y suite deben ser documentos YAML objeto",
            file=sys.stderr,
        )
        return 2

    comp_findings = validate_component(component, component_path)
    suite_findings, structural_cases = validate_suite(suite, suite_path)

    model_rel = None
    model_stats = None
    if mode == "offline":
        case_results = structural_cases
        if max_cases is not None:
            case_results = case_results[: max(0, max_cases)]
    else:
        if not all(f.get("ok") for f in comp_findings + suite_findings):
            print(
                "ERROR: precheck estructural falló; no se llama al modelo",
                file=sys.stderr,
            )
            for f in comp_findings + suite_findings:
                if not f.get("ok"):
                    print(
                        f"  - {f.get('check')}: {f.get('detalle')}",
                        file=sys.stderr,
                    )
            return 2
        if any(not c.get("ok") for c in structural_cases):
            print(
                "ERROR: hay casos estructurales inválidos; no se llama al modelo",
                file=sys.stderr,
            )
            return 2
        try:
            _cfg_path, model_cfg, model_rel = _resolve_model_ref(
                model_ref if isinstance(model_ref, str) else None
            )
        except (OSError, ValueError, FileNotFoundError) as exc:
            print(f"ERROR model-ref: {exc}", file=sys.stderr)
            return 2

        estado_modelo = str(model_cfg.get("estado") or "").lower()
        if estado_modelo in {"retirado", "obsoleto"}:
            print(
                f"ERROR: modelo en estado {estado_modelo!r}; no se ejecuta",
                file=sys.stderr,
            )
            return 2

        try:
            case_results, model_stats = run_model_cases(
                component, suite, model_cfg, max_cases=max_cases
            )
        except Exception as exc:  # ModelClientError y fallos de cliente
            from ms_ia.model_client import ModelClientError

            if isinstance(exc, ModelClientError) or str(exc).startswith("ERROR modo model"):
                print(str(exc), file=sys.stderr)
                return 2
            raise

    result = build_result(
        component,
        component_path,
        suite,
        suite_path,
        comp_findings,
        suite_findings,
        case_results,
        ejecutado_por,
        mode=mode,
        model_ref=model_rel,
        model_stats=model_stats,
    )

    output_dir.mkdir(parents=True, exist_ok=True)
    cid = component.get("id") or "componente"
    ver = component.get("version") or "0.0.0"
    day = datetime.now(timezone.utc).strftime("%Y-%m-%d")
    out_path = output_dir / f"{day}-{cid}-v{ver}-{mode}.json"
    with out_path.open("w", encoding="utf-8") as fh:
        json.dump(result, fh, ensure_ascii=False, indent=2)
        fh.write("\n")

    resumen = result["resumen"]
    title = "offline (estructural)" if mode == "offline" else "model"
    print(f"=== Harness {title} ===")
    print(f"Componente: {cid} v{ver} (estado={component.get('estado')})")
    print(f"Suite:      {suite.get('id')} v{suite.get('version')}")
    if model_rel:
        print(f"Modelo:     {model_rel}")
    print(f"Casos:      {resumen['n_pasados']}/{resumen['n_casos']} OK")
    print(f"Umbrales:   {'OK' if resumen['umbrales_obligatorios_ok'] else 'FALLA'}")
    print("Apto aprobación operativa: NO")
    print(f"Resultado:  {out_path}")

    if not resumen["umbrales_obligatorios_ok"]:
        print("\nFallos:")
        for f in comp_findings + suite_findings:
            if not f.get("ok"):
                print(f"  - {f.get('check')}: {f.get('detalle')}")
        for c in case_results:
            if not c.get("ok"):
                print(f"  - caso {c.get('caso_id')}: {c.get('checks')}")
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
