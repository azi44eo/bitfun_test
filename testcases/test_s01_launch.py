"""SMOKE-S01: Launch BitFun and verify main shell is visible.

Do NOT extend: workspace, code session, settings, AI chat, git, terminal.
"""
import pytest


@pytest.mark.smoke
@pytest.mark.oh
def test_s01_launch(app):
    app.start()
    app.wait_main_shell(timeout=30)
    app.assert_main_visible()
