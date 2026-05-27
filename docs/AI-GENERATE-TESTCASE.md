# AI 从意图生成 pytest 用例（Hypium）

将下面 Prompt 交给 Agent，并 `@docs/smoke-intents.csv` 中对应 **id 行**（及 `resource/selectors_oh.yaml`）。

---

## Prompt（复制使用）

```markdown
请根据 @docs/smoke-intents.csv 中 id=<Sxx> 那一行生成 OH 冒烟用例。

必读：
- @docs/AGENT-RULES.md
- @resource/selectors_oh.yaml（仅使用该行的 selector_keys 列，分号分隔）
- @docs/intent-driven-hypium.md

要求：
1. 新建或更新 testcase 列中的文件（如 test_s01_...py）。
2. 仅使用 app：start, wait_main_shell, tap(key), wait_for_selector(key), assert_selector_visible(key),
   input_text(key, text), press_enter(), type_and_send(key, text)（按需）。
3. 禁止 UiDriver, BY, hypium import。
4. docstring：SMOKE id、CSV 行摘要、selector keys。
5. @pytest.mark.smoke + @pytest.mark.oh。
6. selector_keys 中任一 key 在 YAML 为 confirmed: false 时，加 skipif（参考 test_s01_claw_chat_smoke.py）。
7. 更新 CSV 的 status、testcase 列（若新建文件）。

执行：pytest testcases/test_<file>.py --platform=oh -m "oh" -v
```

---

## 检查清单

- [ ] selector_keys 均在 selectors_oh.yaml
- [ ] 用例无 BY / UiDriver
- [ ] CSV status 已更新
