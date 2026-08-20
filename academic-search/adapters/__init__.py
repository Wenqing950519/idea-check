"""Optional and injected retrieval adapters."""

from .base import RetrievalAdapter, AdapterUnavailableError
from .local_document import LocalDocumentAdapter
from .web_search import WebSearchAdapter

__all__ = ["RetrievalAdapter", "AdapterUnavailableError", "LocalDocumentAdapter", "WebSearchAdapter"]
