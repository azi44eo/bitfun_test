# bitfun_test 重构任务书：pytest 平台标记 + 统一 App 封装（供 AI Agent 执行）

> **文档版本**：1.2  
> **日期**：2026-05-22  
> **目标仓库（只改此仓）**：`/Users/zhangtianxing/Documents/00_work/00_code/01_vcoder/bitfun_test`  
> **本文路径（规划说明，执行时复制要点到测试仓）**：`/Users/zhangtianxing/Documents/00_work/00_code/01_vcoder/note/bitfun_test-refactor-pytest-platforms-EXECUTION.md`  
> **前置状态**：已按 `docs/AI-EXECUTION-BRIEF.md` 完成步骤 1～3（阶段 A）。  
> **用户目标**：独立仓保留；**不按平台分子目录**；用例用 `@pytest.mark.oh|mac|win|all`；运行时传 `--platform`；用例只调 `app` 方法；平台实现放在 `aw/`。  
> **不要**：新建 `harmony/`、`e2e/`、`desktop/` 等平台目录；不要把 BitFun 产品仓 `tests/e2e` 整包拷入本仓。  
> **Agent 怎么执行**：本文是**完整细则**（偏长）。**请用分步 Prompt 主入口** → [`bitfun_test-refactor-STEP-PROMPTS.md`](bitfun_test-refactor-STEP-PROMPTS.md)（4 步，每步一轮对话）。不要一次性让 Agent 读完本文并全部做完。

---

## 零、分步执行（推荐）

| 步 | 对应章节 | 说明 |
|----|----------|------|
| 1 | R1 | pytest + conftest + aw/，**不删**旧用例 |
| 2 | R2 | `testcases/test_s01_launch.py`，OH 真机验收 |
| 3 | R3 | 删 `demo_001_launch.*`，改 `main.py` |
| 4 | R4 | 文档与 AGENT-RULES |

**可复制 Prompt**：见 [`bitfun_test-refactor-STEP-PROMPTS.md`](bitfun_test-refactor-STEP-PROMPTS.md)。

---

### 路径与目录树怎么读（避免误解）

- **仓库根目录** = 文件夹 `bitfun_test`（绝对路径：`…/01_vcoder/bitfun_test`）。
- 下文所有目录树 **第一行 `bitfun_test/` 表示「仓库根」**，不是 `01_vcoder` 下的一个普通子项。
- `testcases/`、`aw/`、`main.py` 等都在 **仓库根里面**，与 `main.py` 同级；**绝不是** `01_vcoder/testcases` 与 `01_vcoder/bitfun_test` 并列。

```text
01_vcoder/                          ← 工作区（可能同时含 BitFun、note，不是测试仓根）
└── bitfun_test/                    ← 【仓库根】以下所有路径均相对于此目录
    ├── main.py
    ├── testcases/                  ← 【保留目录名】pytest 用例放这里（与阶段 A 一致）
    ├── aw/
    └── docs/
```

文中写 `testcases/demo_001_launch.py` 时，完整路径为：`bitfun_test/testcases/demo_001_launch.py`。  
重构后用例路径示例：`bitfun_test/testcases/test_s01_launch.py`（**不是** `BitFun/tests/e2e/…`）。

---

## 一、背景与原则

### 1.1 为什么要改

当前仓库是 **Hypium 测试工程模式**（`main.py` + `testcases/*.py` 类用例 + `*.json`），与用户期望的 **pytest 收集 + 平台 mark + `--platform` 过滤** 不一致。

### 1.2 改完后的行为（验收口径）

```bash
cd /Users/zhangtianxing/Documents/00_work/00_code/01_vcoder/bitfun_test
.venv\Scripts\activate   # Windows；macOS 开发机仅做语法检查可 skip 真机

# 鸿蒙 PC（OH）— 必须能跑通 S01（与现 demo_001_launch 等价）
pytest testcases/ --platform=oh -m "oh or all" -v

# Mac / Win — 用例可收集；未实现的平台 App 应 pytest.skip，不得假 PASS
pytest testcases/ --platform=mac -m "mac or all" -v
pytest testcases/ --platform=win -m "win or all" -v
```

### 1.3 设计原则（Agent 必须遵守）

| # | 原则 |
|---|------|
| P1 | 用例目录 **仍为 `testcases/`**（与初版仓库一致），按业务场景加 `test_*.py`；禁止 `harmony/`、`oh/`、`mac/` 等平台子目录 |
| P2 | 平台差异只在 `aw/`（`OhApp`、`DesktopApp`） |
| P3 | OH 上 UI **必须**仍用 Hypium + hdc；Mac/Win 第一阶段 **允许 skip**，不得 mock 通过 |
| P4 | 保留并复用已验证的 `BITFUN_BUNDLE`、`MAIN_SHELL_SELECTOR`（来自现 `aw/bitfun_app.py`） |
| P5 | `config/user_config.xml` 保留，供 Hypium / hdc 使用 |
| P6 | 迁移完成后 **删除** `testcases/` 下旧 Hypium **类用例**与 `.json` 文件；**保留 `testcases/` 目录**，改放 pytest 用例 |
| P7 | 无真机时不得声称 OH 已 PASS；mac/win 可说明为「预期 skip」 |

---

## 二、当前仓库清单（执行前只读核对）

路径：`/Users/zhangtianxing/Documents/00_work/00_code/01_vcoder/bitfun_test`

### 2.1 现有文件树（2026-05-22 勘察）

> 下列缩进均相对于 **仓库根** `…/01_vcoder/bitfun_test/`。

```text
[仓库根] bitfun_test/
├── .cursor/rules/harmony-e2e.mdc
├── .gitignore
├── .python-version                 # 3.10.11
├── AGENTS.md
├── README.md
├── main.py                         # Hypium TestRunner 或降级 pytest testcases/
├── requirements.txt                # hypium, pytest
├── config/user_config.xml          # usb-hdc, testcases dir
├── aw/bitfun_app.py                # 已实现 OH：bundle + 欢迎使用 selector
├── testcases/                      # ← 子目录，不是与 bitfun_test 文件夹同级
│   ├── demo_001_launch.py          # Hypium 类用例 Demo001Launch
│   └── demo_001_launch.json
├── docs/
│   ├── AGENT-RULES.md              # 旧规则：main.py 为主、禁止 pytest 驱 UI
│   ├── AI-EXECUTION-BRIEF.md
│   ├── smoke-intent-table.md       # S01 → demo_001_launch
│   ├── e2e-change-rules.md
│   └── setup-windows-hdc.md
└── （无 conftest.py、无 pytest.ini、无 aw/__init__.py；testcases/ 内为旧 Hypium 格式）
```

### 2.2 必须保留的已验证常量（迁移时搬进 `aw/oh.py`）

来自 `aw/bitfun_app.py`：

- `BITFUN_BUNDLE = "com.huawei.BitFun"`
- `MAIN_SHELL_SELECTOR = BY.textContains("欢迎使用")`
- 函数逻辑：`start_app` / `wait_main_shell` / `is_main_shell_visible`

### 2.3 与旧文档的冲突（迁移后以本文 + 新 AGENT-RULES 为准）

| 旧规则（`docs/AGENT-RULES.md`） | 新规则 |
|--------------------------------|--------|
| 执行入口 `python main.py -l …` | **主入口** `pytest testcases/ --platform=…` |
| 禁止 pytest 驱动真机 UI | **允许**：pytest 收集用例，OH 的 UI 在 `OhApp` 内调 Hypium |
| 用例在 `testcases/` + Hypium 类 + `.json` | 用例仍在 **`testcases/test_*.py`**（pytest 函数），**不再新增** `.json` |
| 仅鸿蒙、禁止多平台 | **独立仓**，支持 oh/mac/win mark；mac/win 可先 skip |

---

## 三、目标文件树（重构完成后）

> 同样：第一行是 **仓库根**；**保留 `testcases/` 目录名**，仅替换其中文件格式（Hypium 类用例 → pytest `test_*.py`）。

```text
[仓库根] bitfun_test/
├── pytest.ini                      # markers: oh, mac, win, all, smoke
├── conftest.py                     # --platform、app fixture、mark 过滤
├── main.py                         # 【改】薄封装：转调 pytest（见 R3.1）
├── config/user_config.xml          # 【保留】<testcases dir="testcases" />
├── aw/
│   ├── __init__.py                 # get_app(platform, driver)
│   ├── base.py                     # AppBase 协议/抽象类
│   ├── oh.py                       # OhApp（Hypium，自 bitfun_app.py 迁入）
│   └── desktop.py                  # DesktopApp（mac/win，Phase 1 全 skip）
├── testcases/                      # 【保留目录名】pytest 用例
│   └── test_s01_launch.py          # 替代 demo_001_launch；@pytest.mark.oh
├── docs/
│   ├── AGENT-RULES.md              # 【重写】多平台 pytest 架构
│   ├── smoke-intent-table.md       # 【改】→ testcases/test_s01_launch.py
│   ├── e2e-change-rules.md         # 【改】
│   ├── REFACTOR-PLAN.md            # 【可选】
│   └── …（其余保留）
├── AGENTS.md                       # 【改】入口与命令
├── README.md                       # 【改】Quick start → pytest
└── .cursor/rules/bitfun-test.mdc   # 【新增/替换】harmony-e2e.mdc

# 以下文件在重构后删除（testcases/ 目录本身保留）：
#   testcases/demo_001_launch.py    ← 旧 Hypium 类用例
#   testcases/demo_001_launch.json
#   aw/bitfun_app.py                ← 逻辑在 aw/oh.py
```

**明确删除**（路径均相对于 **仓库根** `bitfun_test/`）：

- `testcases/demo_001_launch.py`（Hypium 类用例，非删整个 testcases/）
- `testcases/demo_001_launch.json`
- `aw/bitfun_app.py`（逻辑已迁入 `aw/oh.py`）

**保留**：`testcases/` 目录；新用例命名为 `testcases/test_*.py`。

**不要**在 `01_vcoder/` 下创建与 `bitfun_test` 同级的 `testcases/`。

---

## 四、变更总表（Agent 执行清单）

| 操作 | 路径 | 说明 |
|------|------|------|
| **新增** | `pytest.ini` | 注册 markers |
| **新增** | `conftest.py` | `--platform`、`app`、`oh_driver`、mark 过滤 |
| **新增** | `aw/__init__.py` | `get_app()` |
| **新增** | `aw/base.py` | 抽象方法 `start`, `wait_main_shell`, `assert_main_visible` |
| **新增** | `aw/oh.py` | 从 `bitfun_app.py` 迁入 |
| **新增** | `aw/desktop.py` | mac/win stub + skip |
| **新增** | `testcases/test_s01_launch.py` | S01，仅 `@pytest.mark.oh` |
| **新增** | `docs/REFACTOR-PLAN.md` | 可选：链到 note 本文 |
| **修改** | `main.py` | 转调 pytest，或 Deprecated 注释 |
| **修改** | `README.md` | 目录与命令 |
| **修改** | `AGENTS.md` | 必读顺序与 pytest 命令 |
| **修改** | `docs/AGENT-RULES.md` | 全文按第三节目标重写 |
| **修改** | `docs/smoke-intent-table.md` | 增加 Platforms 列 |
| **修改** | `docs/e2e-change-rules.md` | 路径用语更新 |
| **修改** | `config/user_config.xml` | 保持 `<testcases dir="testcases" />`（与目录名一致） |
| **修改** | `.cursor/rules/bitfun-test.mdc` | 替换 harmony-e2e.mdc |
| **删除** | `testcases/demo_001_launch.py`、`.json` | 旧 Hypium 类用例（非删 testcases/ 目录） |
| **删除** | `aw/bitfun_app.py` | 已迁移 |
| **删除** | `.cursor/rules/harmony-e2e.mdc` | 由 bitfun-test.mdc 替代 |

---

## 五、分步执行（Agent 按 R1→R6 顺序，不要跳步）

### R1 — 新增 pytest 基础设施（不删旧文件）

#### R1.1 创建 `pytest.ini`

```ini
[pytest]
testpaths = testcases
python_files = test_*.py
python_functions = test_*
markers =
    oh: OpenHarmony PC (Hypium + hdc)
    mac: macOS desktop (not implemented in phase 1)
    win: Windows desktop (not implemented in phase 1)
    all: runs on oh, mac, and win when implemented
    smoke: release smoke intent
addopts = -ra
```

#### R1.2 创建 `conftest.py`（核心）

必须实现：

1. `pytest_addoption`：`--platform`，`choices=["oh","mac","win"]`，**required=True**
2. `pytest_configure`：注册 markers（与 pytest.ini 一致）
3. `pytest_runtest_setup`：若用例 marks 含 `all` → 不 skip；否则当前 `--platform` 必须在 marks 中，否则 `pytest.skip`
4. `@pytest.fixture(scope="function")` **`oh_driver`**：仅 `platform=="oh"` 时创建 `UiDriver()`；yield 后 `stop_app(BITFUN_BUNDLE)`（与现 teardown 一致）
5. `@pytest.fixture` **`app`**：根据 `--platform` 返回 `OhApp(oh_driver)` 或 `DesktopApp(platform)`

**`oh_driver` 实现要点**：

- `from hypium import UiDriver`（及项目已用的 hypium 导入方式）
- 工作目录设为仓库根，确保能读到 `config/user_config.xml`（若 Hypium 需要，在 fixture 内 `os.chdir` 根目录）
- 若 `UiDriver()` 在无设备环境失败：让测试 **error/fail**，不要 catch 后 pass

**`app` fixture 要点**：

```python
# 伪代码 — Agent 写成可运行代码
if platform == "oh":
    return OhApp(oh_driver)
return DesktopApp(platform=platform)
```

#### R1.3 创建 `aw/base.py`

定义 `AppBase`（`typing.Protocol` 或 ABC），方法：

- `start() -> None`
- `wait_main_shell(timeout: int = 30) -> None`
- `assert_main_visible() -> None`（内部 assert，失败信息清晰）

#### R1.4 创建 `aw/oh.py`

- 将 `aw/bitfun_app.py` **原样逻辑**迁入 `OhApp` 类
- 类持有 `self._driver: UiDriver`
- 方法名与 `AppBase` 对齐（不要再暴露全局函数 `start_app(driver)`，除非内部私有）

#### R1.5 创建 `aw/desktop.py`

```python
class DesktopApp(AppBase):
    def __init__(self, platform: str):
        self._platform = platform  # "mac" | "win"

    def start(self):
        pytest.skip(f"DesktopApp ({self._platform}) not implemented; see docs/REFACTOR-PLAN.md phase B")
    # wait_main_shell, assert_main_visible 同样 skip
```

#### R1.6 创建 `aw/__init__.py`

```python
def get_app(platform: str, driver=None) -> AppBase:
    ...
```

**R1 验收**（`testcases/` 内尚无 `test_*.py` 时）：

```bash
pytest --collect-only testcases/ --platform=oh
# 应能加载 conftest 不报错；若无 test_*.py 则 collected 0 items
```

---

### R2 — 新增场景用例 S01（与 demo 等价）

#### R2.1 创建 `testcases/test_s01_launch.py`

```python
import pytest

@pytest.mark.smoke
@pytest.mark.oh
def test_s01_launch(app):
  """SMOKE-S01: Launch BitFun and verify main shell (OH)."""
  app.start()
  app.wait_main_shell(timeout=30)
  app.assert_main_visible()
```

**禁止**在本文件写 `UiDriver`、`BY`、`BITFUN_BUNDLE`。

**注意**：Phase 1 **不要**标 `@pytest.mark.all`，直到 DesktopApp 实现后再加。

#### R2.2 更新 `docs/smoke-intent-table.md`

| ID | Intent | Testcase | Platforms | Status |
|----|--------|----------|-----------|--------|
| S01 | Launch BitFun, verify main shell visible | `testcases/test_s01_launch.py` | oh | Implemented |
| S02 | TODO | TODO | TODO | TODO |

#### R2.3 更新 `docs/e2e-change-rules.md`

- 用例路径统一为 `testcases/test_*.py`（pytest）；**不再新增** `testcases/*.json`
- 将所有 `aw/bitfun_app.py` 改为 `aw/oh.py`（OH）或 `aw/desktop.py`（Mac/Win）

**R2 验收**（Windows + hdc + 已装 BitFun）：

```bash
pytest testcases/test_s01_launch.py --platform=oh -v
# 期望：与原先 demo_001_launch 同等 PASS
```

```bash
pytest testcases/test_s01_launch.py --platform=mac -v
# 期望：0 collected 或 skipped（因无 @pytest.mark.mac）
```

---

### R3 — 切换主入口，移除旧 Hypium 类用例（保留 testcases/ 目录）

#### R3.1 修改 `main.py`

改为薄封装（示例）：

```python
"""Deprecated entry: prefer pytest testcases/ --platform=oh"""
import sys
import pytest

def main():
    args = ["testcases", "-v"]
    if "--platform" not in sys.argv:
        args.extend(["--platform", "oh"])
    args.extend(sys.argv[1:])
    raise SystemExit(pytest.main(args))

if __name__ == "__main__":
    main()
```

或更简单：打印 deprecation 后 `pytest.main(...)`。

**不得**再依赖 `TestRunner` + `testcases/*.json` 作为默认路径。

#### R3.2 修改 `config/user_config.xml`

- **保持** `<testcases dir="testcases" />`（与仓库目录名一致；若官方模板为 `dir` 空则填 `testcases`）

#### R3.3 删除旧 Hypium 用例文件（勿删 testcases/ 目录）

- 删除 `testcases/demo_001_launch.py`、`testcases/demo_001_launch.json`（在 R2 已新增 `test_s01_launch.py` 并验证通过后）
- **不得**删除 `testcases/` 目录本身

**不要**删除 `config/`、`docs/setup-windows-hdc.md`。

**R3 验收**：

```bash
python main.py --platform=oh
# 应等价于 pytest testcases/ --platform=oh -v
```

---

### R4 — 更新文档与 Agent 规则

#### R4.1 重写 `docs/AGENT-RULES.md`（必须包含）

- 项目定位：**独立测试仓**，多平台通过 mark + `--platform`，**无平台子目录**
- 主入口：`pytest testcases/ --platform={oh|mac|win} -m "{platform} or all"`
- OH：Hypium + hdc；UI 只在 `aw/oh.py`
- Mac/Win：只在 `aw/desktop.py`；未实现必须 `pytest.skip`
- 禁止：WebDriverIO/TS 拷入、平台子目录、`testcases/*.json` 模式回潮
- 用例禁止直接使用 `UiDriver`/`BY`（必须经 `app`）

可将 `note/bitfun-harmony-e2e-agent-rules.md` 作参考，但**以本任务书第三节目标树为准**覆盖冲突条款。

#### R4.2 更新 `README.md`

- Directory layout 改为第三节目标树
- Quick start 改为 pytest 命令
- 保留 hdc、bundle、UiViewer 说明（引用 `aw/oh.py`）
- Troubleshooting 增加：`pytest: error: the following arguments are required: --platform`

#### R4.3 更新 `AGENTS.md`

- 验证命令改为 pytest
- 必读增加：本文 `docs/REFACTOR-PLAN.md`（若创建）

#### R4.4 替换 Cursor 规则

- 新增 `.cursor/rules/bitfun-test.mdc`（内容见第六节模板）
- 删除 `.cursor/rules/harmony-e2e.mdc`

**R4 验收**：文档中的命令与 `pytest.ini` / `conftest.py` 一致，无 `main.py -l demo_001_launch` 作为主路径描述。

---

### R5 — 可选增强（本阶段可不做的写入 TODO）

| 项 | 说明 |
|----|------|
| `@pytest.mark.all` 用于 S01 | 等 DesktopApp 实现后再标 |
| Desktop 实现 | 参考 BitFun 产品仓 `tests/e2e/`（**仅作对照，不拷贝 TS**）；可用 Python + 产品 WebDriver 协议或子进程调 wdio |
| `requirements.txt` | 可加 `pytest-xdist` 等，非必须 |
| CI | 不在本任务范围 |

产品仓 E2E 路径（只读参考）：  
`/Users/zhangtianxing/Documents/00_work/00_code/01_vcoder/BitFun/tests/e2e/`

---

### R6 — 自检与交付输出

Agent 结束时必须输出：

1. **变更文件列表**（新增/修改/删除）
2. **最终文件树**（`find . -type f -not -path './.git/*' | sort`）
3. **验证命令**（OH 真机 / mac 上 collect-only）
4. **已知 TODO**（DesktopApp、是否需调整 UiDriver 初始化）
5. **未执行** `git commit`（除非用户明确要求）

#### R6 完整验收清单

- [ ] `pytest testcases/ --platform=oh -m "oh or all" -v` 在 OH 环境 PASS（S01）
- [ ] `pytest testcases/ --platform=mac -m "mac or all"` 不失败（skip 或 0 collected）
- [ ] `testcases/` 存在且无 `demo_001_launch.*`、无 `aw/bitfun_app.py`
- [ ] `testcases/test_s01_launch.py` 无 Hypium/BY 直接调用
- [ ] `docs/AGENT-RULES.md` 与 pytest 入口一致
- [ ] `BITFUN_BUNDLE` 与 selector 与迁移前一致

---

## 六、`.cursor/rules/bitfun-test.mdc` 模板（复制到测试仓）

```markdown
---
description: bitfun_test — pytest platform marks + aw adapters (oh/mac/win)
alwaysApply: true
---

# bitfun_test Agent Rules

Read `docs/AGENT-RULES.md` before any edit.

## Entry

pytest testcases/ --platform={oh|mac|win} -m "{platform} or all"

## Structure

- testcases/ — pytest cases only (`test_*.py`); NO platform subdirs under testcases/
- aw/oh.py, aw/desktop.py — platform UI; case files use `app` fixture only
- OH UI: Hypium + hdc only

## Forbidden

- harmony/, e2e/, new testcases/*.json (Hypium 工程模式 json)
- WebDriverIO/TS copied from product repo
- UiDriver/BY inside testcases/test_*.py (belongs in aw/)
- Fake PASS without device on OH
```

---

## 七、给执行 Agent 的一次性 Prompt（整任务）

```markdown
请在本仓库执行重构任务书（用户 note 目录下的 bitfun_test-refactor-pytest-platforms-EXECUTION.md），按 R1→R6 顺序执行。

仓库路径：/Users/zhangtianxing/Documents/00_work/00_code/01_vcoder/bitfun_test

必读：
- 若测试仓内有 docs/REFACTOR-PLAN.md 则读；否则读用户提供的 note/bitfun_test-refactor-pytest-platforms-EXECUTION.md 全文
- 迁移前阅读 aw/bitfun_app.py、testcases/demo_001_launch.py，保留已验证 bundle 与 selector

硬性要求：
- 用例目录 testcases/（保留目录名），平台 mark + --platform
- aw/oh.py 承接现 OH 逻辑；aw/desktop.py Phase 1 skip
- 删除 demo_001_launch.* 与 aw/bitfun_app.py（迁移后）；**保留 testcases/**
- 更新 docs/AGENT-RULES.md、README.md、AGENTS.md
- 不要 git commit；不要声称 mac/win 已通过

完成后按 R6 输出交付物。
```

---

## 八、分步 Prompt（若用户希望拆多轮）

### Prompt R1 only

```markdown
在 bitfun_test 执行 REFACTOR 任务书 R1：新增 pytest.ini、conftest.py、aw/base.py、aw/oh.py（从 bitfun_app.py 迁入）、aw/desktop.py、aw/__init__.py。不要删 testcases/。不要 commit。
```

### Prompt R2 only

```markdown
在 bitfun_test 执行 REFACTOR 任务书 R2：新增 testcases/test_s01_launch.py，更新 smoke-intent-table 与 e2e-change-rules。R2 完成前可暂留 demo_001_launch.*。不要 commit。
```

### Prompt R3–R4

```markdown
在 bitfun_test 执行 REFACTOR 任务书 R3 与 R4：改 main.py、删 demo_001_launch.*（保留 testcases/ 目录）、删 aw/bitfun_app.py、重写 AGENT-RULES、README、AGENTS、替换 .cursor/rules。不要 commit。
```

---

## 九、风险与处理

| 风险 | 处理 |
|------|------|
| `UiDriver()` 在 pytest fixture 中初始化方式与 TestRunner 不同 | 查 Hypium 官方 pytest 示例；必要时在 `oh_driver` 中显式加载 `config/user_config.xml` |
| macOS 上无法跑 OH | 允许 `pytest --collect-only`；OH 真机验收在 Windows |
| 用户已习惯 `python main.py -l demo_001_launch` | `main.py` 转调 pytest 并 README 说明 deprecated |
| Hypium 类用例删除后无法回滚 | 依赖 git history；Agent 不要 force push |

---

## 十、修订记录

| 版本 | 日期 | 说明 |
|------|------|------|
| 1.0 | 2026-05-22 | 基于 bitfun_test 阶段 A 完成态编制 |
| 1.1 | 2026-05-22 | 用例目录曾改为 tests/（已废弃） |
| 1.2 | 2026-05-22 | **用例目录定为 `testcases/`**，与初版仓库一致；仅改文件格式，不删目录 |
| 1.3 | 2026-05-22 | 增加「零、分步执行」；拆出 `bitfun_test-refactor-STEP-PROMPTS.md` |
