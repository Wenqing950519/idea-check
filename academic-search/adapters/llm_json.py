from __future__ import annotations

import json
from collections.abc import Callable
from typing import Any


class LLMJsonAdapter:
    """Small provider-neutral boundary for structured LLM calls."""

    def __init__(self, complete: Callable[[str], str | dict[str, Any]]) -> None:
        self.complete = complete

    def invoke(self, prompt: str, required_keys: set[str]) -> dict[str, Any]:
        raw = self.complete(prompt)
        data = raw if isinstance(raw, dict) else json.loads(raw)
        missing = required_keys - set(data)
        if missing:
            raise ValueError(f"Structured LLM response is missing keys: {sorted(missing)}")
        return data
