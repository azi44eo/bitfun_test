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
