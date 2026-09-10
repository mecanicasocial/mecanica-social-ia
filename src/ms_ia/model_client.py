"""
Cliente de inferencia para el harness (modo model).

- Credenciales solo desde variables de entorno.
- Sin SDKs propietarios: HTTP JSON estilo OpenAI chat/completions.
- No registra ni devuelve la API key.
"""

from __future__ import annotations

import json
import os
import urllib.error
import urllib.request
from dataclasses import dataclass
from typing import Any


class ModelClientError(RuntimeError):
    """Error controlado al llamar al proveedor de modelo."""


@dataclass
class CompletionResult:
    text: str
    raw: dict[str, Any]
    model_id: str


class OpenAICompatibleClient:
    """Cliente mínimo chat/completions compatible con APIs estilo OpenAI."""

    def __init__(
        self,
        *,
        base_url: str,
        api_key: str,
        model_id: str,
        timeout_sec: float = 60.0,
        api_key_header: str = "Authorization",
        api_key_prefix: str = "Bearer ",
    ) -> None:
        if not base_url:
            raise ModelClientError("base_url vacío")
        if not api_key:
            raise ModelClientError(
                "Falta API key en entorno. Defina la variable indicada en "
                "models/<id>/config.yaml (p. ej. MS_IA_MODEL_API_KEY). "
                "Ver infra/secretos-y-entorno.md"
            )
        if not model_id:
            raise ModelClientError("model_id vacío")
        self.base_url = base_url.rstrip("/")
        self._api_key = api_key
        self.model_id = model_id
        self.timeout_sec = timeout_sec
        self.api_key_header = api_key_header
        self.api_key_prefix = api_key_prefix

    def complete(
        self,
        *,
        system_or_prompt: str,
        user_input: str,
        temperature: float = 0.0,
        max_tokens: int = 512,
    ) -> CompletionResult:
        url = f"{self.base_url}/chat/completions"
        payload = {
            "model": self.model_id,
            "temperature": temperature,
            "max_tokens": max_tokens,
            "messages": [
                {"role": "system", "content": system_or_prompt},
                {"role": "user", "content": user_input},
            ],
        }
        data = json.dumps(payload).encode("utf-8")
        headers = {
            "Content-Type": "application/json",
            "Accept": "application/json",
            self.api_key_header: f"{self.api_key_prefix}{self._api_key}",
        }
        req = urllib.request.Request(url, data=data, headers=headers, method="POST")
        try:
            with urllib.request.urlopen(req, timeout=self.timeout_sec) as resp:
                body = resp.read().decode("utf-8")
        except urllib.error.HTTPError as exc:
            raise ModelClientError(
                f"HTTP {exc.code} al llamar al modelo ({self.model_id})"
            ) from None
        except urllib.error.URLError as exc:
            raise ModelClientError(f"Error de red al llamar al modelo: {exc.reason}") from None

        try:
            raw = json.loads(body)
        except json.JSONDecodeError as exc:
            raise ModelClientError(f"Respuesta no JSON del proveedor: {exc}") from None

        text = _extract_text(raw)
        if text is None:
            raise ModelClientError("Respuesta del proveedor sin content de mensaje")
        return CompletionResult(
            text=text,
            raw={"id": raw.get("id"), "model": raw.get("model")},
            model_id=self.model_id,
        )


def _extract_text(raw: dict[str, Any]) -> str | None:
    choices = raw.get("choices")
    if not isinstance(choices, list) or not choices:
        return None
    first = choices[0]
    if not isinstance(first, dict):
        return None
    message = first.get("message")
    if isinstance(message, dict) and isinstance(message.get("content"), str):
        return message["content"]
    if isinstance(first.get("text"), str):
        return first["text"]
    return None


def build_client_from_model_config(model_cfg: dict[str, Any]) -> OpenAICompatibleClient:
    """
    Construye cliente desde models/<id>/config.yaml + entorno.

    Campos esperados (no secretos):
      provider: openai-compatible
      model_id: str (o env MS_IA_MODEL_ID)
      base_url: str opcional público
      api_key_env: nombre de variable (default MS_IA_MODEL_API_KEY)
      base_url_env: nombre de variable (default MS_IA_MODEL_BASE_URL)
      timeout_sec: float
      api_key_header / api_key_prefix opcionales
    """
    provider = str(model_cfg.get("provider") or "").lower()
    if provider not in {"openai-compatible", "openai_compatible", "openai"}:
        raise ModelClientError(
            f"Proveedor no soportado por el cliente actual: {provider!r}. "
            "Use provider: openai-compatible"
        )

    api_key_env = str(model_cfg.get("api_key_env") or "MS_IA_MODEL_API_KEY")
    base_url_env = str(model_cfg.get("base_url_env") or "MS_IA_MODEL_BASE_URL")
    model_id_env = str(model_cfg.get("model_id_env") or "MS_IA_MODEL_ID")

    api_key = os.environ.get(api_key_env, "").strip()
    base_url = (
        os.environ.get(base_url_env, "").strip()
        or str(model_cfg.get("base_url") or "").strip()
    )
    model_id = (
        os.environ.get(model_id_env, "").strip()
        or str(model_cfg.get("model_id") or "").strip()
    )

    timeout = float(
        os.environ.get("MS_IA_MODEL_TIMEOUT_SEC")
        or model_cfg.get("timeout_sec")
        or 60
    )
    header = str(model_cfg.get("api_key_header") or "Authorization")
    prefix = str(
        model_cfg.get("api_key_prefix") if "api_key_prefix" in model_cfg else "Bearer "
    )

    if not base_url:
        raise ModelClientError(
            f"Falta base_url (config o variable {base_url_env}). "
            "Ver infra/secretos-y-entorno.md"
        )

    return OpenAICompatibleClient(
        base_url=base_url,
        api_key=api_key,
        model_id=model_id,
        timeout_sec=timeout,
        api_key_header=header,
        api_key_prefix=prefix,
    )
