# 意图驱动测试 — 端到端操作说明（Hypium）

> **适用**：鸿蒙 PC 冒烟（OH）。从「写意图」到「AI 生成用例」到「真机执行」的完整步骤。  
> **示例**：下文以 **S01**（当前唯一 OH 冒烟用例）为例。

---

## 一、涉及哪些文件

| 步骤 | 文件 | 谁维护 |
|------|------|--------|
| 写意图 | `docs/smoke-intents.csv`（Excel 打开） | 人 |
| 登记控件 text | `resource/selectors_oh.yaml` | 人（UiViewer） |
| 自动化用例 | `testcases/test_sxx_*.py` | AI 生成 + 人审 |
| 规则 | `docs/AGENT-RULES.md` | 团队 |

索引入口：[`smoke-intent-table.md`](smoke-intent-table.md) → 指向本流程与 CSV。

---

## 二、环境准备（首次）

```powershell
cd C:\Workspace\00_code\00_bitfun\bitfun_test
py -3.10 -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
hdc list targets          # 应看到鸿蒙 PC 设备
```

- BitFun 已安装在设备上（包名 `com.huawei.BitFun`）。
- 控件文案用 **UiViewer** 核对（见步骤 3）。

---

## 三、S01 完整流程（当前唯一冒烟用例）

### 步骤 1 — 在 Excel 写意图

打开 **`docs/smoke-intents.csv`**，维护 **S01** 行（覆盖启动、会话、发送）：

| 列 | S01 示例 |
|----|----------|
| id | S01 |
| summary | 启动 → Claw 会话 → 输入发送 → 失败提示 |
| preconditions | 无（用例内 start） |
| steps | 启动；新建 Claw 会话；输入 Hello；点发送 |
| expected | 出现「对话执行失败」类提示 |
| selector_keys | `main_shell;new_claw_session;claw_session_pane;chat_input;chat_send_button;toast_...` |
| testcase | `testcases/test_s01_claw_chat_smoke.py` |
| platforms | oh |
| status | 已实现 |

列说明详见 [`smoke-intents-README.md`](smoke-intents-README.md)。

**保存 CSV**（Excel 另存为 CSV UTF-8，避免中文乱码）。

---

### 步骤 2 — 在登记表填控件 text

编辑 **`resource/selectors_oh.yaml`**，为 `selector_keys` 里每个 key 增加一段，例如：

```yaml
  new_claw_session:
    by: text
    value: "新建 Claw 会话 1"    # UiViewer 看到的全文
    match: CONTAINS
    confirmed: false             # 确认前可先 false

  claw_session_pane:
    by: text
    value: "会话 新建 Claw 会话 1"
    match: CONTAINS
    confirmed: false
```

- `value` 必须与真机界面一致（空格、数字都要对）。
- **保存文件**（未保存会导致 pytest 仍读旧值）。

---

### 步骤 3 — UiViewer 确认并启用

1. 设备上打开 BitFun，走到要操作的界面。
2. UiViewer 查看控件的 **text**，改 YAML 里 `value`。
3. 两个 key 都确认后设 **`confirmed: true`**。
4. 再次 **保存** `selectors_oh.yaml`。

---

### 步骤 4 — 让 AI 生成用例

在 **Cursor**（或带 `@` 文件的 Agent）新建对话，复制 [`AI-GENERATE-TESTCASE.md`](AI-GENERATE-TESTCASE.md) 中的 Prompt，把 `Sxx` 换成 **S01**，并引用：

- `@docs/smoke-intents.csv`
- `@resource/selectors_oh.yaml`
- `@docs/AGENT-RULES.md`

AI 应生成/更新 **`testcases/test_s01_claw_chat_smoke.py`**（见仓库当前实现）。

**人审要点**：无 `BY` / `UiDriver`；`tap`/`wait` 的 key 与 CSV、`yaml` 一致。

若 selector 尚未 `confirmed: true`，可让 AI 加 `@pytest.mark.skipif`；确认后删除 skip。

---

### 步骤 5 — 执行用例

```powershell
.venv\Scripts\activate
hdc list targets

# OH 冒烟（S01）
pytest testcases/test_s01_claw_chat_smoke.py --platform=oh -m "oh" -v

# 或
pytest testcases/ --platform=oh -m "oh and smoke" -v
```

---

## 四、流程图（一览）

```text
smoke-intents.csv (意图)
        │
        ├──────────────────► selectors_oh.yaml (text + confirmed)
        │                              │
        ▼                              ▼
   AI 生成 test_sxx.py ◄─────── 仅引用 selector key
        │
        ▼
   pytest --platform=oh  (hdc + Hypium 真机)
```

---

## 五、常见问题

| 现象 | 处理 |
|------|------|
| `Selector 'xxx' is not confirmed` | 保存 YAML，且对应 key 的 `confirmed: true` |
| 点了控件无反应 / 找不到 | 改 YAML 的 `value`/`match`，UiViewer 重采 |
| 编辑器里改了 YAML 但 pytest 仍失败 | **磁盘未保存**；Ctrl+S 后重跑 |
| `pytest: error: --platform` | 必须加 `--platform=oh` |
| 想先探路再登记 | 可用 `runtime-calibration` 的 `verifyUI`，通过后把 text 写入 YAML |

---

## 六、相关文档

| 文档 | 内容 |
|------|------|
| **本文** | 端到端步骤 + S01 示例 |
| [`smoke-intents-README.md`](smoke-intents-README.md) | CSV 列说明、Excel 用法 |
| [`intent-driven-hypium.md`](intent-driven-hypium.md) | 三层分工（简版） |
| [`AI-GENERATE-TESTCASE.md`](AI-GENERATE-TESTCASE.md) | 给 AI 的 Prompt 模板 |
| [`e2e-change-rules.md`](e2e-change-rules.md) | 改测试不许弱化断言 |
| [`AGENT-RULES.md`](AGENT-RULES.md) | 技术栈与禁止项 |
