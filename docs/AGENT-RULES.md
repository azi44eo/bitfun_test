# BitFun 多平台测试仓 — AI / Agent 硬性规则

> **用途**：所有 Agent、Cursor、人工改代码均须遵守。  
> **与任务书关系**：`REFACTOR-EXECUTION.md` 定义重构目标；**本文管「必须怎么做、禁止什么」**。冲突时以本文为准。

---

## 一、项目定位

| 事实 | 说明 |
|------|------|
| 仓库性质 | **独立测试仓**，覆盖 OH / Mac / Win 三个平台 |
| 被测对象 | BitFun 桌面应用（OH → Hypium；Mac/Win → 后续实现） |
| 执行环境 | OH：**Windows 宿主机** → hdc → 鸿蒙 PC；Mac/Win：对应宿主机 |
| 平台区分 | `@pytest.mark.{oh,mac,win,all}` + `--platform` 命令行参数；**无平台子目录** |

---

## 二、技术栈

### 2.1 语言与运行时

- **Python 3.10.x only**（推荐 3.10.11）。`.python-version` 约束。
- 依赖：`requirements.txt`；虚拟环境 `.venv/` 不提交。

### 2.2 测试与 UI 驱动

| 组件 | 角色 | 硬性要求 |
|------|------|----------|
| **pytest** | 测试组织、收集、marker 过滤 | **主入口**：`pytest testcases/ --platform={oh\|mac\|win} -m "{platform} or all"` |
| **Hypium** | OH 真机上的 **唯一** UI 自动化手段 | 仅在 `aw/oh.py` 中使用；通过 `oh_driver` fixture 注入 |
| **hdc** | OH 宿主机与鸿蒙 PC 的**唯一**设备连接 | `config/user_config.xml` 中 `device type="usb-hdc"` |

### 2.3 执行入口

- **主入口**：`pytest testcases/ --platform={oh|mac|win} -m "{platform} or all" -v`
- **辅助入口**：`python main.py`（转发到 pytest，保留兼容）

### 2.4 明确禁止

- ❌ WebDriverIO、Selenium、Playwright、TypeScript E2E
- ❌ 在 `testcases/` 下创建 `harmony/`、`oh/`、`mac/`、`win/` 等平台子目录
- ❌ 在 `testcases/test_*.py` 中直接使用 `UiDriver`、`BY`（必须通过 `app` fixture）
- ❌ 新增 `testcases/*.json`（Hypium 工程模式 json）
- ❌ Mac/Win 上 mock 跳过并声称已通过
- ❌ 弱化 P0 断言（删断言、`assert True`）以换绿

---

## 三、目录与代码结构

```text
bitfun_test/
├── pytest.ini                 # markers: oh, mac, win, all, smoke
├── conftest.py                # --platform, app/oh_driver fixtures, mark 过滤
├── main.py                    # 薄封装 → pytest
├── config/user_config.xml     # usb-hdc（OH 设备配置）
├── testcases/                 # pytest 用例（test_*.py，无平台子目录）
├── aw/
│   ├── __init__.py            # get_app()
│   ├── base.py                # AppBase 协议/抽象类
│   ├── oh.py                  # OhApp（Hypium + hdc）
│   └── desktop.py             # DesktopApp（mac/win，Phase 1 skip）
├── resource/                  # 测试资源
├── docs/                      # 文档
└── reports/                   # gitignore
```

### 3.1 用例编写规则

1. 用例放在 `testcases/test_*.py`，使用 `pytest.mark.{oh,mac,win,all,smoke}`。
2. **testcases 里**：只调 `app` fixture 的方法（`start`、`wait_main_shell`、`assert_main_visible`）；禁止直接使用 `UiDriver`、`BY`、`BITFUN_BUNDLE`。
3. 平台实现集中在 `aw/`：OH → `aw/oh.py`；Mac/Win → `aw/desktop.py`。
4. 选择器与 bundle 常量集中管理，有变更需注释说明确认来源（UiViewer / hdc）。

### 3.2 断言与意图

- 不得弱化 P0 断言。UI 变更时更新选择器，不删除检查。
- 改测试时在 PR/变更中引用对应 `SMOKE-xx`。
- 详细流程见 `docs/e2e-change-rules.md`。

---

## 四、设备与环境

### 4.1 OH（鸿蒙 PC）

- Windows 宿主机执行 `hdc list targets` 确认设备。
- `config/user_config.xml` 配置 `usb-hdc`；多设备通过 `<sn>` 指定。

### 4.2 无真机时的 Agent 行为

- 允许：搭骨架、写文档、语法正确的占位断言。
- 禁止：声称「已在鸿蒙 PC 跑通」、编造 PASS 报告。

---

## 五、与 BitFun 产品仓的边界

| 允许 | 禁止 |
|------|------|
| 参考产品仓 E2E 结构（只读对照） | 复制 BitFun 源码或 TS E2E 到本仓 |
| 文档中引用产品仓链接 | 在产品仓内新增鸿蒙 Hypium 代码 |

---

## 六、Git 与交付物

- 不主动 `git commit`。
- 不提交：`.venv/`、`reports/`、`__pycache__/`、`*.hap`、`local_packages/`。

---

## 七、Agent 自检清单

- [ ] 仅 Python 3.10 + pytest + Hypium + hdc（OH），无禁选技术栈
- [ ] OH UI 操作均在 `aw/oh.py`；桌面 stub 在 `aw/desktop.py`
- [ ] `testcases/` 内为 `test_*.py` pytest 用例，无平台子目录，无 `.json`
- [ ] 用例不直接使用 `UiDriver` / `BY`
- [ ] 主入口为 `pytest testcases/ --platform=...`
- [ ] 未弱化 P0 断言；mac/win skip 说明为预期行为
- [ ] 未主动 commit

---

## 八、修订记录

| 版本 | 日期 | 说明 |
|------|------|------|
| 2.0 | 2026-05-26 | 重构：多平台 pytest mark + aw 适配层；替代 Hypium 工程模式入口 |
| 1.0 | 2026-05-22 | 初版 |
