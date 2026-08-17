from __future__ import annotations

from collections.abc import Callable
from pathlib import Path

from .base import AdapterUnavailableError


class GrobidAdapter:
    """Optional parser boundary; return TEI XML without vendoring GROBID."""

    def __init__(self, parser: Callable[[Path], str] | None = None) -> None:
        self.parser = parser

    def available(self) -> bool:
        return self.parser is not None

    def parse_pdf(self, path: str | Path) -> str:
        if self.parser is None:
            raise AdapterUnavailableError("No GROBID client/service parser was configured.")
        tei = self.parser(Path(path))
        if "<TEI" not in tei and "<tei" not in tei:
            raise ValueError("GROBID adapter did not return TEI XML.")
        return tei
