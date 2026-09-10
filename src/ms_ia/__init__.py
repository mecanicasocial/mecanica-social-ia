"""Utilidades compartidas de mecanica-social-ia."""

from .model_client import ModelClientError, OpenAICompatibleClient, build_client_from_model_config

__all__ = [
    "ModelClientError",
    "OpenAICompatibleClient",
    "build_client_from_model_config",
]
