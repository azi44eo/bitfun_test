"""
OpenHarmony PC adapter — Hypium + hdc.

Selectors: resource/selectors_oh.yaml (UiViewer-confirmed text / position / offset).
"""
from __future__ import annotations

from typing import Any

from hypium import *
from hypium.model import KeyCode

from aw.base import AppBase
from aw.registry import OhSelectorRegistry


BITFUN_BUNDLE = "com.huawei.BitFun"
BITFUN_ABILITY = "EntryAbility"

_MAIN_SHELL_KEY = "main_shell"

def build_by_from_spec(spec: dict[str, Any]):
    """Build Hypium BY from a registry entry (text / key / type)."""
    by_type = spec.get("by", "text")
    value = spec["value"]
    match = (spec.get("match") or "EQUALS").upper()

    if by_type == "text":
        selector = BY.text(value)
    elif by_type == "key":
        selector = BY.key(value)
    elif by_type == "type":
        selector = BY.type(value)
    else:
        raise NotImplementedError(f"Unsupported by type {by_type!r} in selector registry")

    if by_type == "text":
        if match == "CONTAINS":
            selector.match_pattern = MatchPattern.CONTAINS
        elif match == "STARTS_WITH":
            selector.match_pattern = MatchPattern.STARTS_WITH
        elif match == "ENDS_WITH":
            selector.match_pattern = MatchPattern.ENDS_WITH
        elif match not in ("EQUALS", "EQUAL"):
            raise ValueError(f"Unknown match mode {match!r}")
    return selector


class OhApp(AppBase):
    """Hypium-driven BitFun on HarmonyOS PC."""

    def __init__(self, driver: UiDriver, registry: OhSelectorRegistry | None = None) -> None:
        self._driver = driver
        self._registry = registry or OhSelectorRegistry()

    def _touch(self, selector_key: str) -> None:
        spec = self._registry.get(selector_key)
        by_type = spec.get("by", "text")
        if by_type == "position":
            self._driver.touch((float(spec["x"]), float(spec["y"])))
            return
        if by_type == "offset_from":
            anchor_spec = self._registry.get(spec["anchor"])
            offset = (
                float(spec.get("offset_x", 0.5)),
                float(spec.get("offset_y", 0.5)),
            )
            self._driver.touch(build_by_from_spec(anchor_spec), offset=offset)
            return
        self._driver.touch(build_by_from_spec(spec))

    def start(self) -> None:
        self._driver.start_app(BITFUN_BUNDLE, BITFUN_ABILITY)

    def wait_main_shell(self, timeout: int = 30) -> None:
        self.wait_for_selector(_MAIN_SHELL_KEY, timeout=timeout)

    def assert_main_visible(self) -> None:
        self.assert_selector_visible(_MAIN_SHELL_KEY)

    def tap(self, selector_key: str) -> None:
        self._registry.require_confirmed(selector_key)
        self._touch(selector_key)

    def wait_for_selector(self, selector_key: str, timeout: int = 30) -> None:
        self._registry.require_confirmed(selector_key)
        spec = self._registry.get(selector_key)
        if spec.get("by") in ("position", "offset_from"):
            raise NotImplementedError(
                f"wait_for_selector does not support by={spec.get('by')!r} for {selector_key!r}"
            )
        component = self._driver.wait_for_component(build_by_from_spec(spec), timeout=timeout)
        assert component is not None, (
            f"Selector {selector_key!r} did not appear within {timeout}s — "
            f"check resource/selectors_oh.yaml"
        )

    def assert_selector_visible(self, selector_key: str) -> None:
        self._registry.require_confirmed(selector_key)
        spec = self._registry.get(selector_key)
        if spec.get("by") in ("position", "offset_from"):
            raise NotImplementedError(
                f"assert_selector_visible does not support by={spec.get('by')!r} for {selector_key!r}"
            )
        assert self._driver.check_component_exist(build_by_from_spec(spec)), (
            f"Selector {selector_key!r} not visible — check resource/selectors_oh.yaml"
        )

    def input_text(self, selector_key: str, text: str) -> None:
        self._registry.require_confirmed(selector_key)
        self._driver.input_text(build_by_from_spec(self._registry.get(selector_key)), text)

    def press_enter(self) -> None:
        self._driver.press_key(KeyCode.ENTER)

    def type_and_send_smart(
        self,
        input_selector_key: str,
        text: str,
        send_button_key: str = "chat_send_button",
    ) -> None:
        """Type in chat input, then tap send (position/BY) if confirmed, else Enter."""
        self.tap(input_selector_key)
        self.input_text(input_selector_key, text)
        if self._registry.is_confirmed(send_button_key):
            self.tap(send_button_key)
            return
        self.press_enter()
