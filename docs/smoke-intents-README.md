# 冒烟意图表（Excel 维护）

## 用哪个文件

| 文件 | 用途 |
|------|------|
| **`smoke-intents.csv`** | **唯一意图数据源**（用 Excel / WPS 打开编辑） |
| `resource/selectors_oh.yaml` | 控件 **text** 登记表（UiViewer → `confirmed: true`） |
| `testcases/test_s*.py` | 自动化用例（AI 生成，人审） |

不再维护单独的 `docs/intents/Sxx.md`；一行意图 = CSV 里一行。

## 如何用 Excel 编辑

1. 用 **Excel** 打开 `docs/smoke-intents.csv`（若中文乱码：数据 → 自文本/CSV → UTF-8）。
2. 或在 Excel 中 **另存为 `.xlsx` 本地编辑**，改完再 **另存回 CSV UTF-8** 提交仓库（团队约定其一即可）。
3. 新增意图：复制上一行，改 `id`（S04…），填 `summary` / `steps` / `expected` 等。
4. `selector_keys`：多个 key 用 **英文分号** `;` 分隔（如 `new_claw_session;claw_session_pane`），对应 `selectors_oh.yaml` 里的名字。

### 仅 Position、无 text/key 的控件

在 `selectors_oh.yaml` 使用 `by: position`，填写按钮中心坐标：

```yaml
chat_send_button:
  by: position
  x: 1234    # UiViewer 中心 X（像素）
  y: 890     # UiViewer 中心 Y（像素）
  confirmed: true
```

若 UiViewer 给的是 **bounds** `[left, top, right, bottom]`，中心为 `x=(left+right)/2`，`y=(top+bottom)/2`。

也可用 **0~1 屏幕比例**（如 `x: 0.91`, `y: 0.86`），Hypium 会按分辨率换算。

可选：相对某锚点控件点击（输入后占位符会消失，锚点宜用 `claw_session_pane`）：

```yaml
  by: offset_from
  anchor: claw_session_pane
  offset_x: 0.92
  offset_y: 0.88
```

## 列说明（不必每列都写满）

| 列 | 必填 | 说明 |
|----|------|------|
| id | ✅ | S01、S02… |
| summary | ✅ | 一句话意图（索引用） |
| preconditions | 建议 | 前置，如「S01 主壳已可见」 |
| steps | 建议 | 操作（自然语言） |
| expected | 建议 | P0 预期 |
| not_in_scope | 可选 | 不测什么 |
| selector_keys | 生成用例时需要 | 分号分隔，不在正文重复写 text |
| testcase | 有则填 | pytest 文件路径 |
| platforms | ✅ | 如 `oh` |
| status | 建议 | 已实现 / 待 UiViewer / 待补充 |

**不必**在意图里写 Hypium、BY、示例代码；也不必逐步绑 key——key 集中在本表 + YAML。

## 新增一条意图（最短流程）

1. Excel 加一行 + `selectors_oh.yaml` 加 key（先 `confirmed: false`）。
2. 用 `docs/AI-GENERATE-TESTCASE.md` 让 AI 根据 **本 CSV 对应行** 生成 `testcases/test_sxx_*.py`。
3. UiViewer 确认 text → YAML `confirmed: true` → `pytest … -v`。

## 执行

```powershell
pytest testcases/ --platform=oh -m "oh and smoke" -v
```
