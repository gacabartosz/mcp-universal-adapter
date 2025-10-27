"""Base parser interface for all API specification formats."""

from abc import ABC, abstractmethod
from pathlib import Path

from mcp_adapter.models import NormalizedAPISpec


class BaseParser(ABC):
    """Abstract base class for all API parsers.

    All parsers (OpenAPI, GraphQL, REST, HAR) must inherit from this
    and implement the parse() method to convert their format into
    the unified NormalizedAPISpec format.
    """

    def __init__(self, source: str | Path):
        """Initialize parser with source.

        Args:
            source: URL or file path to API specification
        """
        self.source = str(source)

    @abstractmethod
    async def parse(self) -> NormalizedAPISpec:
        """Parse API specification into normalized format.

        Returns:
            NormalizedAPISpec: Unified API specification

        Raises:
            ParserError: If parsing fails
        """
        pass

    @abstractmethod
    def validate(self) -> bool:
        """Validate that source is correct format for this parser.

        Returns:
            bool: True if valid, False otherwise
        """
        pass

    def is_url(self, source: str) -> bool:
        """Check if source is a URL."""
        return source.startswith("http://") or source.startswith("https://")

    def is_file(self, source: str) -> bool:
        """Check if source is a file path."""
        return Path(source).exists()


class ParserError(Exception):
    """Base exception for parser errors."""

    pass


class ParserValidationError(ParserError):
    """Raised when parser validation fails."""

    pass


class ParserNetworkError(ParserError):
    """Raised when network request fails."""

    pass
