"""Base generator interface for all target languages."""

from abc import ABC, abstractmethod
from typing import Dict, Any
from pathlib import Path


class BaseGenerator(ABC):
    """Abstract base class for MCP server generators."""

    def __init__(self, api_spec: Dict[str, Any]):
        """Initialize generator with API specification.

        Args:
            api_spec: Parsed API specification dictionary
        """
        self.api_spec = api_spec

    @abstractmethod
    def generate(self, output_dir: Path) -> None:
        """Generate MCP server code in output directory.

        Args:
            output_dir: Directory to write generated files
        """
        pass

    @abstractmethod
    def validate_spec(self) -> bool:
        """Validate that API spec contains required information.

        Returns:
            True if spec is valid, False otherwise
        """
        pass
