"""
macOS / Windows desktop adapter — stub with pytest.skip.

Phase 1: no desktop implementation.  All methods skip so that
mac/win test collection doesn't fail.
"""
import pytest

from aw.base import AppBase


def _skip_desktop(platform: str) -> None:
    pytest.skip(f"DesktopApp ({platform}) not implemented; see docs/REFACTOR-EXECUTION.md R5")


class DesktopApp(AppBase):
    """Stub desktop adapter; implementation pending (see docs/REFACTOR-EXECUTION.md R5)."""

    def __init__(self, platform: str) -> None:
        self._platform = platform  # "mac" | "win"

    def start(self) -> None:
        _skip_desktop(self._platform)

    def wait_main_shell(self, timeout: int = 30) -> None:
        _skip_desktop(self._platform)

    def assert_main_visible(self) -> None:
        _skip_desktop(self._platform)

    def tap(self, selector_key: str) -> None:
        _skip_desktop(self._platform)

    def wait_for_selector(self, selector_key: str, timeout: int = 30) -> None:
        _skip_desktop(self._platform)

    def assert_selector_visible(self, selector_key: str) -> None:
        _skip_desktop(self._platform)

    def input_text(self, selector_key: str, text: str) -> None:
        _skip_desktop(self._platform)

    def press_enter(self) -> None:
        _skip_desktop(self._platform)
