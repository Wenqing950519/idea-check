from __future__ import annotations

import html
import re
from collections.abc import Callable
from pathlib import Path

from adapters.base import AdapterUnavailableError


class FullTextReader:
    """Local-first full-text path with an injected PDF parser boundary."""

    def __init__(self, pdf_parser: Callable[[Path], str] | None = None) -> None:
        self.pdf_parser = pdf_parser

    def read(self, path: str | Path) -> tuple[str, str]:
        source = Path(path)
        suffix = source.suffix.casefold()
        if suffix in {".txt", ".md", ".csv", ".json"}:
            return source.read_text(encoding="utf-8"), self._mime(suffix)
        if suffix in {".html", ".htm"}:
            raw = source.read_text(encoding="utf-8")
            text = re.sub(r"<script\b[^>]*>.*?</script>|<style\b[^>]*>.*?</style>", "", raw, flags=re.I | re.S)
            text = html.unescape(re.sub(r"<[^>]+>", " ", text))
            return " ".join(text.split()), "text/html"
        if suffix == ".pdf":
            if self.pdf_parser is None:
                raise AdapterUnavailableError("PDF parsing is unavailable; configure PaperQA, GROBID, or an injected parser.")
            return self.pdf_parser(source), "application/pdf"
        raise ValueError(f"Unsupported full-text format: {suffix or '<none>'}")

    @staticmethod
    def _mime(suffix: str) -> str:
        return {".md": "text/markdown", ".csv": "text/csv", ".json": "application/json"}.get(suffix, "text/plain")
