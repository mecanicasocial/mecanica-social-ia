#!/usr/bin/env python3
"""
Harness de evaluación offline para mecanica-social-ia.

Contrato: evaluations/harness.md
- Mide y reporta; no otorga aprobación institucional.
- Modo offline: validación estructural (componente + suite).
- No llama a proveedores de modelos ni lee secretos.
"""

from __future__ import annotations

import argparse
import json
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
        obj, err = _as_expected_obj(ej.get("expected")) if has_io else (None, "faltan input/expected")
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


def validate_suite(suite: dict[str, Any], path: Path) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
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

        failed = [c for c in checks if not c.get("ok")]
        case_results.append(
            {
                "caso_id": cid,
                "tags": caso.get("tags") or [],
                "estado": "pass" if ok else "fail",
                "ok": ok,
                "metricas_locales": {},
                "mensaje": None
                if ok
                else "; ".join(
                    f"{c.get('check')}: {c.get('detalle') or 'fail'}" for c in failed
                ),
                "checks": checks,
            }
        )

    return findings, case_results


def build_result(
    component: dict[str, Any],
    component_path: Path,
    suite: dict[str, Any],
    suite_path: Path,
    comp_findings: list[dict[str, Any]],
    suite_findings: list[dict[str, Any]],
    case_results: list[dict[str, Any]],
    ejecutado_por: str,
) -> dict[str, Any]:
    n_casos = len(case_results)
    n_pass = sum(1 for c in case_results if c.get("ok"))
    n_fail = n_casos - n_pass
    structural_ok = all(f.get("ok") for f in comp_findings + suite_findings) and n_fail == 0
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

    now = datetime.now(timezone.utc)
    resultado_id = f"eval-{now.strftime('%Y%m%d')}-offline"
    rel_comp = str(component_path.relative_to(REPO_ROOT)) if component_path.is_relative_to(REPO_ROOT) else str(component_path)
    rel_suite = str(suite_path.relative_to(REPO_ROOT)) if suite_path.is_relative_to(REPO_ROOT) else str(suite_path)

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
            "modo": "offline",
            "harness_ref": "evaluations/harness.md",
            "modelo_ref": None,
            "entorno": "local",
            "semilla": None,
            "ejecutado_por": ejecutado_por,
            "notas": (
                "Corrida offline estructural. No llama a modelos. "
                "No constituye evidencia de exactitud de extracción ni aprobación operativa."
            ),
        },
        "metricas": metricas,
        "resumen": {
            "n_casos": n_casos,
            "n_pasados": n_pass,
            "n_fallidos": n_fail,
            "tasa_exito_primaria": round(tasa, 2),
            "umbrales_obligatorios_ok": structural_ok,
            "alcance": "estructural",
            "apto_para_aprobacion_operativa": False,
        },
        "validacion_estructural": {
            "componente": comp_findings,
            "suite": suite_findings,
        },
        "casos_detalle": case_results,
        "limitaciones": [
            "Modo offline: no evalúa el comportamiento del modelo.",
            "Los expected son fixtures sintéticas, no predicciones.",
            "apto_para_aprobacion_operativa es siempre false en este modo.",
        ],
        "decision_institucional": {
            "estado": "no_aplicable",
            "referencia": None,
            "notas": "La decisión vive en gobernanza (PR/registro); no la inventa el harness.",
        },
    }


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Harness offline de mecanica-social-ia (no aprueba uso operativo)."
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
        choices=["offline"],
        help="Solo offline está implementado en este MVP",
    )
    parser.add_argument(
        "--output",
        default="evaluations/resultados",
        help="Directorio de salida para el JSON de resultado",
    )
    parser.add_argument(
        "--ejecutado-por",
        default="harness-offline",
        help="Identificador de quien ejecuta la corrida",
    )
    args = parser.parse_args(argv)

    if args.mode != "offline":
        print("ERROR: solo modo offline implementado", file=sys.stderr)
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
        print("ERROR: componente y suite deben ser documentos YAML objeto", file=sys.stderr)
        return 2

    comp_findings = validate_component(component, component_path)
    suite_findings, case_results = validate_suite(suite, suite_path)
    result = build_result(
        component,
        component_path,
        suite,
        suite_path,
        comp_findings,
        suite_findings,
        case_results,
        args.ejecutado_por,
    )

    output_dir.mkdir(parents=True, exist_ok=True)
    cid = component.get("id") or "componente"
    ver = component.get("version") or "0.0.0"
    day = datetime.now(timezone.utc).strftime("%Y-%m-%d")
    out_path = output_dir / f"{day}-{cid}-v{ver}-offline.json"
    with out_path.open("w", encoding="utf-8") as fh:
        json.dump(result, fh, ensure_ascii=False, indent=2)
        fh.write("\n")

    resumen = result["resumen"]
    print("=== Harness offline (estructural) ===")
    print(f"Componente: {cid} v{ver} (estado={component.get('estado')})")
    print(f"Suite:      {suite.get('id')} v{suite.get('version')}")
    print(f"Casos:      {resumen['n_pasados']}/{resumen['n_casos']} estructurales OK")
    print(f"Umbrales:   {'OK' if resumen['umbrales_obligatorios_ok'] else 'FALLA'}")
    print("Apto aprobación operativa: NO (modo offline)")
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
