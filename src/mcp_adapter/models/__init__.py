"""Unified API models for all parsers."""

from .api_spec import (
    NormalizedAPISpec,
    Endpoint,
    Parameter,
    ParameterLocation,
    HTTPMethod,
    AuthConfig,
    AuthType,
    SchemaModel,
    PropertySchema,
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
]
