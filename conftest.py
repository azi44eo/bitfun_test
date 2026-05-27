"""pytest configuration: --platform, app fixture, platform mark filtering."""
import pytest


# ---------------------------------------------------------------------------
# Option & markers
# ---------------------------------------------------------------------------

def pytest_addoption(parser):
    parser.addoption(
        "--platform",
        choices=["oh", "mac", "win"],
        required=True,
        help="Target platform: oh (OpenHarmony), mac, or win",
    )


def pytest_configure(config):
    config.addinivalue_line("markers", "oh: OpenHarmony PC (Hypium + hdc)")
    config.addinivalue_line("markers", "mac: macOS desktop (not implemented in phase 1)")
    config.addinivalue_line("markers", "win: Windows desktop (not implemented in phase 1)")
    config.addinivalue_line("markers", "all: runs on oh, mac, and win when implemented")
    config.addinivalue_line("markers", "smoke: release smoke intent")


# ---------------------------------------------------------------------------
# Mark-based filtering
# ---------------------------------------------------------------------------

PLATFORM_MARKS = {"oh", "mac", "win"}


def pytest_runtest_setup(item):
    platform = item.config.getoption("--platform")
    item_marks = {m.name for m in item.own_markers}

    if "all" in item_marks:
        return
    if platform in item_marks:
        return
    # Only skip when the item has explicit platform marks that don't match
    if item_marks & PLATFORM_MARKS:
        matched = ", ".join(sorted(item_marks & PLATFORM_MARKS))
        pytest.skip(f"test requires platform(s) {matched}, current platform is {platform}")


# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------

_BITFUN_BUNDLE = "com.huawei.BitFun"


@pytest.fixture(scope="function")
def oh_driver(request):
    """Create a Hypium UiDriver for OH platform.  Returns None otherwise."""
    platform = request.config.getoption("--platform")
    if platform != "oh":
        yield None
        return

    from hypium import UiDriver
    driver = UiDriver.connect(connector="hdc")
    yield driver
    driver.stop_app(_BITFUN_BUNDLE)


@pytest.fixture
def app(request, oh_driver):
    """Return the platform-appropriate AppBase instance."""
    platform = request.config.getoption("--platform")
    if platform == "oh":
        from aw.oh import OhApp
        return OhApp(oh_driver)
    from aw.desktop import DesktopApp
    return DesktopApp(platform=platform)
