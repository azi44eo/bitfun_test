# 意图驱动 + Hypium 冒烟（登记表方案）

## 三层分工

| 层 | 位置 | 谁维护 | 内容 |
|----|------|--------|------|
| 1 意图 | **`docs/smoke-intents.csv`**（Excel） | 人 | summary、前置、步骤、预期、selector_keys |
| 2 用例 | `testcases/test_s*.py` | AI 生成 + 人审 | 只调 `app` 方法 |
| 3 选择器 | `resource/selectors_oh.yaml` | 人（UiViewer） | 控件 text / match |

**禁止**：在 `testcases/` 里写 `BY` / `UiDriver`。

## 新增一条冒烟

1. **Excel** — 在 `smoke-intents.csv` 加一行（见 `smoke-intents-README.md`）。
2. **YAML** — `selectors_oh.yaml` 增加 key，`confirmed: false`。
3. **AI** — `docs/AI-GENERATE-TESTCASE.md` 生成 pytest。
4. **UiViewer** — 确认 text → `confirmed: true`。
5. **执行** — `pytest testcases/ --platform=oh -m "oh and smoke" -v`。

## 执行

```powershell
hdc list targets
pytest testcases/ --platform=oh -m "oh and smoke" -v
```

## runtime-calibration

自然语言探路 → 通过后把 text 写入 `selectors_oh.yaml`；回归仍用本表 + Hypium。
