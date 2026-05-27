# Smoke Intent Table

**主表**：[`smoke-intents.csv`](smoke-intents.csv)（Excel 编辑）  
**端到端怎么做**：[`intent-driven-workflow.md`](intent-driven-workflow.md)

| ID | 意图 | 用例 | 平台 | 状态 |
|----|------|------|------|------|
| S01 | 启动 → 主壳 → 新建 Claw 会话 → 输入发送 → 失败提示 | `testcases/test_s01_claw_chat_smoke.py` | oh | ✅ 已实现 |

**选择器**：`resource/selectors_oh.yaml`  
**AI 生成用例**：`docs/AI-GENERATE-TESTCASE.md`
