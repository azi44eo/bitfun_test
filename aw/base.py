"""Abstract base for platform-specific BitFun app adapters."""
from abc import ABC, abstractmethod


class AppBase(ABC):
    """Protocol every platform adapter must fulfil."""

    @abstractmethod
    def start(self) -> None:
        """Launch the BitFun application."""
        ...

    @abstractmethod
    def wait_main_shell(self, timeout: int = 30) -> None:
        """Wait until the main shell is stable (or raise on timeout)."""
        ...

    @abstractmethod
    def assert_main_visible(self) -> None:
        """Assert the main shell is visible."""
        ...

    @abstractmethod
    def tap(self, selector_key: str) -> None:
        """Tap a control identified by registry key (OH: selectors_oh.yaml)."""
        ...

    @abstractmethod
    def wait_for_selector(self, selector_key: str, timeout: int = 30) -> None:
        """Wait until a registry selector matches a visible component."""
        ...

    @abstractmethod
    def assert_selector_visible(self, selector_key: str) -> None:
        """Assert a registry selector is currently visible."""
        ...

    @abstractmethod
    def input_text(self, selector_key: str, text: str) -> None:
        """Type *text* into the control identified by registry key."""
        ...

    @abstractmethod
    def press_enter(self) -> None:
        """Press Enter (e.g. send message in chat input)."""
        ...

    def type_and_send(
        self,
        input_selector_key: str,
        text: str,
        send_button_key: str = "chat_send_button",
    ) -> None:
        """Focus input, type text, tap send button (preferred on WebView)."""
        self.tap(input_selector_key)
        self.input_text(input_selector_key, text)
        self.tap(send_button_key)

    def type_and_send_via_enter(self, input_selector_key: str, text: str) -> None:
        """Type text then Enter (no second tap — placeholder text vanishes after input)."""
        self.tap(input_selector_key)
        self.input_text(input_selector_key, text)
        self.press_enter()
