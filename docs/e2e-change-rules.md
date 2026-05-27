# E2E Change Rules

## 1. Do not weaken P0 assertions

- Never delete, comment out, or replace a P0 assertion with `assert True` to make a test pass.
- If an assertion fails due to UI change, update the selector — do not remove the check.

## 2. UI changes must sync selectors

- OH 控件文案变更时，更新 `resource/selectors_oh.yaml` 中对应 key 的 `value` / `match`（UiViewer 确认）。
- `aw/oh.py` 通过登记表构建 `BY`；不要在 `testcases/` 硬编码选择器。
- Desktop selectors (future) use a separate registry under `resource/`.
- Do not hard-code selectors in `testcases/`; reference stable **selector keys** only.

## 3. PR / change description must reference smoke intent

- When modifying a test, note the affected smoke intent ID (e.g., **SMOKE-S01**) in the PR description.
- When adding a new smoke intent, add a row to `docs/smoke-intent-table.md`.
