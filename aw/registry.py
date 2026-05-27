"""Load OH selector registry from resource/selectors_oh.yaml."""
from __future__ import annotations

from pathlib import Path
from typing import Any

import yaml

_REGISTRY_PATH = Path(__file__).resolve().parent.parent / "resource" / "selectors_oh.yaml"


class OhSelectorRegistry:
    """Selector specs keyed by stable names used in intents and aw methods."""

    def __init__(self, path: Path | None = None) -> None:
        self._path = path or _REGISTRY_PATH
        raw = yaml.safe_load(self._path.read_text(encoding="utf-8"))
        if not isinstance(raw, dict) or "selectors" not in raw:
            raise ValueError(f"Invalid registry format: {self._path}")
        selectors = raw["selectors"]
        if not isinstance(selectors, dict):
            raise ValueError(f"'selectors' must be a mapping in {self._path}")
        self._selectors: dict[str, dict[str, Any]] = selectors

    @property
    def path(self) -> Path:
        return self._path

    def get(self, key: str) -> dict[str, Any]:
        if key not in self._selectors:
            known = ", ".join(sorted(self._selectors))
            raise KeyError(
                f"Unknown selector key {key!r}. "
                f"Add it to {self._path} or fix the intent/test. Known: {known}"
            )
        return self._selectors[key]

    def is_confirmed(self, key: str) -> bool:
        return bool(self.get(key).get("confirmed", False))

    def require_confirmed(self, key: str) -> None:
        if not self.is_confirmed(key):
            raise RuntimeError(
                f"Selector {key!r} is not confirmed in {self._path}. "
                "Update value/match via UiViewer, set confirmed: true, then re-run."
            )

    def keys(self) -> list[str]:
        return sorted(self._selectors)
