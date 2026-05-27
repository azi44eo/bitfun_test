"""SMOKE-S01: OH 端到端冒烟。

流程：启动 BitFun → 主壳 → 新建 Claw 会话 → 输入 Hello → 坐标点击发送
     → 断言「对话执行失败」（无 API 配置时的预期）。

Intent: docs/smoke-intents.csv (id=S01)
"""
import time

import pytest

from aw.registry import OhSelectorRegistry

_REGISTRY = OhSelectorRegistry()
_S01_KEYS = (
    "main_shell",
    "new_claw_session",
    "claw_session_pane",
    "chat_input",
    "chat_send_button",
    "toast_dialog_execution_failed",
)
_S01_READY = all(_REGISTRY.is_confirmed(k) for k in _S01_KEYS)


@pytest.mark.smoke
@pytest.mark.oh
@pytest.mark.skipif(
    not _S01_READY,
    reason="SMOKE-S01: confirm all selector keys in resource/selectors_oh.yaml",
)
def test_s01_claw_chat_smoke(app):
    app.start()
    app.wait_main_shell(timeout=30)
    app.tap("new_claw_session")
    app.wait_for_selector("claw_session_pane", timeout=30)

    app.type_and_send_smart("chat_input", "Hello")
    time.sleep(8)

    app.wait_for_selector("toast_dialog_execution_failed", timeout=60)
    app.assert_selector_visible("toast_dialog_execution_failed")
