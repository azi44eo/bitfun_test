# E2E Change Rules

## 1. Do not weaken P0 assertions

- Never delete, comment out, or replace a P0 assertion with `assert True` to make a test pass.
- If an assertion fails due to UI change, update the selector — do not remove the check.

## 2. UI changes must sync selectors

- When BitFun UI changes (text, key, id), update the corresponding `BY` selector in `aw/`.
- OH selectors belong in `aw/oh.py`; desktop selectors (future) in `aw/desktop.py`.
- Do not hard-code selectors in `testcases/`; keep them in the aw layer.

## 3. PR / change description must reference smoke intent

- When modifying a test, note the affected smoke intent ID (e.g., **SMOKE-S01**) in the PR description.
- When adding a new smoke intent, add a row to `docs/smoke-intent-table.md`.
