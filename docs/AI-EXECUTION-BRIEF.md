# AI 执行任务书：搭建 BitFun 鸿蒙 PC 测试框架（独立空仓库）

> **用途**：在新 Cursor 窗口打开**测试工程空 Git 仓库**后，将本文全文作为 Prompt，或 `@本文件` 让 Agent 按步骤执行。  
> **阶段目标**：仅 **阶段 A** — 搭框架骨架 + 1 条 Demo 用例（代码可运行结构；真机通过需 hdc + 鸿蒙包）。  
> **不要做的事**：不要实现 Mac/Win WebDriverIO；不要往 BitFun 产品仓加代码。  
> **推荐执行方式**：**分 3 步**（见下文「零、分步执行」），不要一次性让 AI 做完第三节全部交付物。

---

## 零、分步执行（推荐：新 Cursor 窗口用 3 条 Prompt）

先把本文复制到测试仓：`docs/AI-EXECUTION-BRIEF.md`。每步**单独开一轮 Agent 对话**，上一步完成并验收后再进行下一步。

### 使用方式

1. Cursor **Open Folder** → 打开测试工程空 Git 仓  
2. 将 `bitfun-harmony-e2e-AI-EXECUTION-BRIEF.md` 复制为仓库内 `docs/AI-EXECUTION-BRIEF.md`  
3. 依次粘贴 **步骤 1 → 2 → 3** 的 Prompt（每步结束看「本步验收」）

若有团队现有 Hypium 项目，在**步骤 1** Prompt 末尾加上参考路径，让 AI 复制 `main.py` / `user_config.xml` 再改。

---

### 步骤 1：工程骨架 + 配置（不含 Demo 用例）

**复制以下 Prompt：**

```markdown
请在本仓库执行【步骤 1/3】，严格范围如下。

必读：@docs/AI-EXECUTION-BRIEF.md（第一节背景、第二节约束、第八节禁止项）

本步只创建以下文件，不要创建 testcases/、aw/ 下业务代码：

- .python-version（3.10.11）
- requirements.txt（hypium、pytest，注明需 Python 3.10）
- .gitignore（venv、reports、__pycache__、*.hap 等，见任务书第三节）
- README.md（含：用途、Python 3.10、hdc、目录说明、Quick start 占位、TODO bundleName）
- main.py（Hypium 测试工程入口；若无法确认 API，用官方测试工程最小模板并注释 TODO）
- config/user_config.xml（usb-hdc、testcases 目录、loglevel）
- docs/setup-windows-hdc.md（Windows 安装 hdc、hdc list targets 验证）
- resource/.gitkeep
- reports/ 目录不提交内容，仅在 .gitignore 忽略

不要：testcases、aw/bitfun_app.py、git commit、WebDriverIO、声称真机已跑通。

完成后输出：① 已创建文件列表 ② 步骤 2 前的本地 TODO（安装 Python 3.10、hdc）
```

**本步验收（你自行检查）：**

- [ ] 根目录有 `main.py`、`config/user_config.xml`、`requirements.txt`  
- [ ] README 写明 Python 3.10  
- [ ] 尚无 `testcases/demo_001_launch.*`

---

### 步骤 2：Demo 用例 + aw 封装

**复制以下 Prompt（需步骤 1 已完成）：**

```markdown
请在本仓库执行【步骤 2/3】。步骤 1 的骨架已存在，不要重复创建或删除。

必读：@docs/AI-EXECUTION-BRIEF.md 第四节（demo_001_launch 行为定义）

本步只添加：

- aw/__init__.py
- aw/bitfun_app.py（BITFUN_BUNDLE = "com.bitfun.desktop" 或明确 TODO 常量；start、wait_main_shell）
- testcases/demo_001_launch.py（启动 + 等待 + 占位断言，注释说明需 UiViewer 改 BY）
- testcases/demo_001_launch.json（与 py 同名，Hypium 工程模式配置）

不要：其他 smoke 用例、git commit、弱化断言、工作区/设置/AI 相关流程。

完成后输出：① 新增文件列表 ② 需在 UiViewer 中确认的控件属性 ③ 建议的 python main.py -l demo_001_launch 命令
```

**本步验收：**

- [ ] `aw/bitfun_app.py` 与 `testcases/demo_001_launch.py` 存在  
- [ ] Demo 仅覆盖「启动 + 主界面」，无多余场景  
- [ ] bundle 与选择器处有 TODO/注释  

---

### 步骤 3：治理文档 + 全文自检

**复制以下 Prompt（需步骤 1、2 已完成）：**

```markdown
请在本仓库执行【步骤 3/3】。不要改动 demo 用例核心逻辑，除非发现明显语法错误。

必读：@docs/AI-EXECUTION-BRIEF.md 第五节、第十节

本步添加/更新：

- docs/smoke-intent-table.md（表头 + S01 一行对应 demo_001_launch，其余标 TODO）
- docs/e2e-change-rules.md（简短：不得弱化 P0 断言、改 UI 同步 key、PR 注明 SMOKE-xx）
- 更新 README.md：补充 docs 索引、Related repos 占位、Troubleshooting 与任务书第五节对齐
- 在 README 或 docs/ 增加「阶段 A 完成检查清单」（对应任务书第十节，可勾选格式）

不要：新增大量用例、CI、git commit。

完成后输出：① 本步修改/新增文件 ② 阶段 A 整体文件树 ③ 我在 Windows 测试机上的完整验证步骤（从 venv 到 main.py）
```

**本步验收（阶段 A 整体）：**

- [ ] 文件树与任务书第三节一致  
- [ ] `docs/smoke-intent-table.md`、`e2e-change-rules.md` 存在  
- [ ] 三节 Prompt 跑完后可开始本地：Python 3.10 → pip install → hdc → 填 bundle → 跑 Demo  

---

### 三步都做完之后（你在 Windows 测试机）

```bash
py -3.10 -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
hdc list targets
python main.py -l demo_001_launch
```

真机 PASS 依赖：鸿蒙 PC 已连接、BitFun 已安装、bundle/选择器已从 TODO 改为真实值。

---

## 一、背景（给 AI 的上下文）

- BitFun 是桌面 Agent 产品；**鸿蒙 PC 版**与 Mac/Win 版技术栈不同。
- 测试在 **独立 Git 仓库**（当前可能只有 README + .gitignore，几乎为空）。
- 自动化方案：**Windows 宿主机** 上跑 **Python 3.10 + pytest + Hypium**，通过 **hdc** 连接 **鸿蒙 PC**，驱动已安装的 BitFun 应用。
- 团队其它项目已用 **Hypium 测试工程模式**（`config/user_config.xml` + `testcases/*.py` + `main.py`）。若执行环境能访问参考项目，应优先对齐其结构与 hypium 版本。

**业务目标（后续，本次仅留扩展位）**：

1. 发版前减少人工点关键路径的时间（冒烟自动化）。
2. UI 常变：测试分「意图」与「实现」，不得为跑绿而弱化断言。

---

## 二、技术约束（必须遵守）

| 项 | 要求 |
|----|------|
| Python | **3.10.x only**（推荐 3.10.11）；写 `.python-version` |
| UI 框架 | **Hypium**（`pip install hypium`） |
| 测试 | **pytest** 可安装并用于目录结构；执行入口以 **Hypium `main.py`** 为主 |
| 设备 | **hdc**；`user_config.xml` 中 `device type="usb-hdc"` |
| Hypium 模式 | **测试工程模式**；不要与 Driver 模式混用 |
| 平台 | 仅鸿蒙 PC；**不要**创建 WebDriverIO / TypeScript E2E |

---

## 三、交付物清单（必须全部创建）

在**仓库根目录**创建：

```text
.python-version                 # 3.10.11
requirements.txt                # hypium, pytest（版本写范围）
.gitignore                      # 补充见下
README.md                       # 完整说明：环境、hdc、跑 Demo、TODO
main.py                         # Hypium 测试工程入口（可参考官方示例）
config/
  user_config.xml               # hdc、testcases 目录、日志级别
testcases/
  demo_001_launch.json          # 与 py 同名的 Hypium 用例配置
  demo_001_launch.py            # Demo：启动应用 + 主界面断言（占位可运行）
aw/
  __init__.py
  bitfun_app.py                 # BitFunApp：bundle 常量、start、wait_main_shell
resource/
  .gitkeep
docs/
  setup-windows-hdc.md          # Windows 安装 hdc、验证连接
  smoke-intent-table.md         # 表头 + S01 Demo 一行（其余 TODO）
  e2e-change-rules.md           # 改测试勿偏离意图的简短规则
reports/                        # 仅 .gitignore，不提交内容
```

### `.gitignore` 必须包含

`.venv/`, `venv/`, `reports/`, `output/`, `__pycache__/`, `*.pyc`, `.pytest_cache/`, `.idea/`, `.vscode/`, `*.hap`, `*.app`, `local_packages/`

### `requirements.txt` 示例

```text
# Requires Python 3.10.x
hypium>=6.0.7,<7
pytest>=7.4,<9
```

### 占位常量（集中 TODO）

在 `aw/bitfun_app.py` 顶部：

```python
BITFUN_BUNDLE = "com.bitfun.desktop"  # TODO: replace with real HarmonyOS PC bundle name
```

在 `demo_001_launch.py` 断言处用注释标明：**需 UiViewer 替换 BY 选择器**。

---

## 四、`demo_001_launch` 行为定义（意图，不是实现细节）

| 步骤 | 意图 |
|------|------|
| 1 | 启动 BitFun（`start_app(BUNDLE)` 或等价） |
| 2 | 等待主界面稳定（超时 30s，可轮询） |
| 3 | 断言：主壳存在（占位：某 text/key；失败时日志说明需 UiViewer） |

**不要**在本 Demo 中包含：工作区、Code 会话、设置、AI 对话。

---

## 五、README.md 必须包含的章节

1. Project purpose  
2. Prerequisites：Windows, Python 3.10, hdc, hypium, HarmonyOS PC connected  
3. Quick start：`venv` → `pip install -r requirements.txt` → `hdc list targets` → `python main.py -l demo_001_launch`  
4. Directory layout（树状说明）  
5. Configuration：`BITFUN_BUNDLE` TODO、`user_config.xml` SN  
6. Related：BitFun product repo is separate; this repo is test-only  
7. Troubleshooting：hdc 找不到设备、hypium 导入失败  

---

## 六、执行步骤（Agent 按序做）

**默认按「零、分步执行」三步完成；仅当用户明确要求「一次性交付」时，才合并执行下面 1～5。**

1. 列出当前仓库已有文件（可能仅有 README/.gitignore）。  
2. 创建第三节全部文件；内容完整、可语法检查（Python 无明显错误）。  
3. `main.py` / `user_config.xml` 若不确定，按 [Hypium 官方 Python 指南](https://developer.huawei.com/consumer/cn/doc/harmonyos-guides/hypium-python-guidelines) 最小可运行模板填写。  
4. 不要 `git commit`，除非用户明确要求。  
5. 结束时输出：
   - 已创建文件列表  
   - 用户本地待办：安装 Python 3.10、hdc、填 bundleName、UiViewer 改选择器  
   - 建议验证命令  

---

## 七、若环境允许的可选验证

仅在执行机为 **Windows** 且已配置 hdc + 设备时：

```bash
py -3.10 -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
hdc list targets
python main.py -l demo_001_launch
```

Mac/Linux 开发机无法连鸿蒙 PC 时：**只搭代码结构，不声称真机已跑通**。

---

## 八、禁止项

- 不要创建 `tests/e2e` WebDriverIO 工程  
- 不要复制 BitFun 产品仓 Rust/前端代码  
- 不要提交 `.venv`、`reports`、`*.hap`  
- 不要编造已通过的真机报告（无设备时）  
- 不要过度设计 CI、大量冒烟用例（阶段 A 仅 Demo）

---

## 九、参考文档路径（若在 monorepo 另一目录）

用户可能在 `01_vcoder/note/` 下有：

- `bitfun-harmony-pc-e2e-framework-plan.md` — 总体方案  
- `bitfun-harmony-e2e-github-setup.md` — GitHub 配置  

执行时以**本文任务书**为准；冲突时以本文「阶段 A 范围」优先。

---

## 十、完成定义（Agent 自检）

- [ ] 目录结构与第三节一致  
- [ ] Python 3.10 约束写入 `.python-version` 与 README  
- [ ] `demo_001_launch.py` + `.json` + `aw/bitfun_app.py` 存在且逻辑清晰  
- [ ] `docs/setup-windows-hdc.md` 可让他人复现 hdc 检查  
- [ ] README 说明 TODO（bundle、选择器）  
- [ ] 未做禁止项  

---

## 修订记录

| 版本 | 日期 | 说明 |
|------|------|------|
| 1.0 | 2026-05-22 | 初版 |
| 1.1 | 2026-05-22 | 新增「零、分步执行」三节 Prompt + 每步验收清单 |
