"""
macOS / Windows desktop adapter — stub with pytest.skip.

Phase 1: no desktop implementation.  All methods skip so that
mac/win test collection doesn't fail.
"""
import pytest

from aw.base import AppBase


class DesktopApp(AppBase):
    """Stub desktop adapter; implementation pending (see docs/REFACTOR-EXECUTION.md R5)."""

    def __init__(self, platform: str) -> None:
        self._platform = platform  # "mac" | "win"

    def start(self) -> None:
        pytest.skip(f"DesktopApp ({self._platform}) not implemented; see docs/REFACTOR-EXECUTION.md R5")

    def wait_main_shell(self, timeout: int = 30) -> None:
        pytest.skip(f"DesktopApp ({self._platform}) not implemented; see docs/REFACTOR-EXECUTION.md R5")

    def assert_main_visible(self) -> None:
        pytest.skip(f"DesktopApp ({self._platform}) not implemented; see docs/REFACTOR-EXECUTION.md R5")
