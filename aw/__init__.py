"""Platform adapter factory."""
from aw.base import AppBase


def get_app(platform: str, driver=None) -> AppBase:
    """Return the AppBase instance for *platform*.

    ``driver`` must be a Hypium UiDriver when *platform* is ``"oh"``.
    """
    if platform == "oh":
        from aw.oh import OhApp
        return OhApp(driver)
    from aw.desktop import DesktopApp
    return DesktopApp(platform=platform)
