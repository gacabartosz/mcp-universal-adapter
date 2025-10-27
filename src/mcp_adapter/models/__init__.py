"""Unified API models for all parsers."""

from .api_spec import (
    AuthConfig,
    AuthType,
    Endpoint,
    HTTPMethod,
    NormalizedAPISpec,
    Parameter,
    ParameterLocation,
    PropertySchema,
    SchemaModel,
    ServerConfig,
)

__all__ = [
    "NormalizedAPISpec",
    "Endpoint",
    "Parameter",
    "ParameterLocation",
    "HTTPMethod",
    "AuthConfig",
    "AuthType",
    "SchemaModel",
    "PropertySchema",
    "ServerConfig",
]
