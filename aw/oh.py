"""
OpenHarmony PC adapter — Hypium + hdc.

Migrated from aw/bitfun_app.py.  Preserves confirmed bundle name and
UiViewer-confirmed main-shell selector.
"""
from hypium import *

from aw.base import AppBase


# Confirmed bundle name from hdc query
BITFUN_BUNDLE = "com.huawei.BitFun"

# UiViewer confirmed: top title bar text contains "欢迎使用"
# Full text in UiViewer: "欢迎使用 Close 欢迎使用" — use textContains to avoid fragility
MAIN_SHELL_SELECTOR = BY.textContains("欢迎使用")


class OhApp(AppBase):
    """Hypium-driven BitFun on HarmonyOS PC."""

    def __init__(self, driver: UiDriver) -> None:
        self._driver = driver

    def start(self) -> None:
        """Launch BitFun on the connected HarmonyOS PC."""
        self._driver.start_app(BITFUN_BUNDLE)

    def wait_main_shell(self, timeout: int = 30) -> None:
        """Wait until the BitFun main shell is visible."""
        self._driver.wait_for_exists(MAIN_SHELL_SELECTOR, timeout=timeout)

    def assert_main_visible(self) -> None:
        """Assert the main shell is currently visible."""
        assert self._driver.exists(MAIN_SHELL_SELECTOR), \
            "BitFun main shell not visible — check BY selector in aw/oh.py"
