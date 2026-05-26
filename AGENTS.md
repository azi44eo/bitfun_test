# AGENTS.md — bitfun_test

BitFun 多平台发版冒烟自动化（独立测试仓）。**Agent 必须先读规则再写代码。**

## 必读（按顺序）

1. [`docs/AGENT-RULES.md`](docs/AGENT-RULES.md) — 技术栈与禁止项（**最高优先级**）
2. [`docs/REFACTOR-EXECUTION.md`](docs/REFACTOR-EXECUTION.md) — 重构任务书
3. [`docs/AI-EXECUTION-BRIEF.md`](docs/AI-EXECUTION-BRIEF.md) — 阶段 A 分步交付
4. [`docs/smoke-intent-table.md`](docs/smoke-intent-table.md) — 冒烟意图
5. [`docs/e2e-change-rules.md`](docs/e2e-change-rules.md) — 改测试规则

## 技术栈

| 项 | 要求 |
|----|------|
| Python | 3.10.x |
| 测试框架 | **pytest** + platform marks |
| OH UI | **Hypium** + **hdc**（`usb-hdc`） |
| 宿主机 | Windows（OH） / macOS / Windows |

## 入口

```bash
# OH（鸿蒙 PC，需 Windows + hdc + 已装 BitFun）
pytest testcases/ --platform=oh -m "oh or all" -v

# Mac / Win（Phase 1: skip）
pytest testcases/ --platform=mac -m "mac or all" -v
pytest testcases/ --platform=win -m "win or all" -v
```

## 禁止

WebDriverIO、混用产品仓源码、无真机声称 PASS、`testcases/` 下平台子目录、用例直接使用 `UiDriver`/`BY`。

## 验证（Windows + 鸿蒙 PC）

```bash
hdc list targets
pytest testcases/ --platform=oh -m "oh or all" -v
```
