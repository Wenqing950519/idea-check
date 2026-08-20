"""Academic discovery providers and routing."""

from .base import DiscoveryProvider, DiscoveryRouter, ProviderUnavailableError
from .openalex import OpenAlexProvider

__all__ = ["DiscoveryProvider", "DiscoveryRouter", "ProviderUnavailableError", "OpenAlexProvider"]
