# BitFun E2E Test Framework

BitFun 多平台桌面应用自动化测试框架（独立测试仓）。OH 基于 Hypium + hdc；Mac/Win 规划中。

## Prerequisites

- **Python 3.10.x**（推荐 3.10.11，见 `.python-version`）
- **OH 平台**：Windows 宿主机 + hdc + 鸿蒙 PC + 已安装 BitFun
- **Mac/Win 平台**：Phase 1 暂未实现（预期 skip）

## Quick start

```bash
# 创建虚拟环境
py -3.10 -m venv .venv
.venv\Scripts\activate          # Windows
# source .venv/bin/activate     # macOS/Linux

# 安装依赖
pip install -r requirements.txt

# OH — 确认设备连接
hdc list targets

# 运行测试
pytest testcases/ --platform=oh -m "oh or all" -v
```

> ⚠️ 首次运行前需用 UiViewer 确认控件选择器（见 Configuration）。

## Directory layout

```
bitfun_test/
├── pytest.ini                 # markers: oh, mac, win, all, smoke
├── conftest.py                # --platform option, app fixture, mark filtering
├── main.py                    # thin wrapper → pytest
├── config/
│   └── user_config.xml        # usb-hdc device config
├── testcases/                 # pytest cases (test_*.py, no platform subdirs)
│   └── test_s01_launch.py
├── aw/
│   ├── __init__.py            # get_app()
│   ├── base.py                # AppBase protocol
│   ├── oh.py                  # OhApp (Hypium + hdc)
│   └── desktop.py             # DesktopApp (mac/win stub, Phase 1 skip)
├── resource/
│   └── .gitkeep
├── reports/                   # gitignored
├── docs/
│   ├── AGENT-RULES.md
│   ├── REFACTOR-EXECUTION.md
│   ├── AI-EXECUTION-BRIEF.md
│   ├── smoke-intent-table.md
│   ├── e2e-change-rules.md
│   └── setup-windows-hdc.md
├── requirements.txt
├── .python-version
└── .gitignore
```

## Configuration

- **bundleName**：`aw/oh.py` 中 `BITFUN_BUNDLE = "com.huawei.BitFun"`（已通过 hdc 确认）
- **主界面选择器（OH）**：`aw/oh.py` 中 `MAIN_SHELL_SELECTOR = BY.textContains("欢迎使用")`（已通过 UiViewer 确认）
- **设备 SN**：`config/user_config.xml` 中 `<device sn="..." />`，单设备可留空

## Troubleshooting

| 问题 | 排查 |
|------|------|
| `hdc list targets` 无输出 | 检查 USB 连接、驱动、hdc 是否在 PATH；详见 [setup-windows-hdc.md](docs/setup-windows-hdc.md) |
| `pytest: error: --platform` | `--platform` 参数必填，值为 `oh`、`mac` 或 `win` |
| `ModuleNotFoundError: hypium` | 确认虚拟环境已激活，`pip install -r requirements.txt`；若 pip 找不到包，尝试华为 PyPI 镜像 |
| 用例启动应用失败 | 确认 `BITFUN_BUNDLE` 为真实值；确认 BitFun 已安装在鸿蒙 PC 上 |
| 控件定位失败 | 用 UiViewer 确认控件属性，更新 `aw/oh.py` 中的 `BY` 选择器 |
| Mac/Win 测试 skip | Phase 1 预期行为；DesktopApp 尚未实现 |

## Docs

| 文档 | 说明 |
|------|------|
| [docs/AGENT-RULES.md](docs/AGENT-RULES.md) | Agent 硬性规则（最高优先级） |
| [docs/REFACTOR-EXECUTION.md](docs/REFACTOR-EXECUTION.md) | 多平台重构任务书 |
| [docs/smoke-intent-table.md](docs/smoke-intent-table.md) | 冒烟意图与用例映射 |
| [docs/e2e-change-rules.md](docs/e2e-change-rules.md) | 改测试规则 |
| [docs/setup-windows-hdc.md](docs/setup-windows-hdc.md) | Windows 安装 hdc |
| [docs/AI-EXECUTION-BRIEF.md](docs/AI-EXECUTION-BRIEF.md) | 阶段 A 分步交付任务书 |

## Related

- BitFun 产品仓库（独立）— TODO: 补充仓库链接

---

## Phase A 完成检查清单

- [x] `pytest.ini` + `conftest.py` 多平台 mark 基础设施
- [x] `aw/base.py` + `aw/oh.py` + `aw/desktop.py` + `aw/__init__.py`
- [x] `testcases/test_s01_launch.py` 替代 `demo_001_launch`
- [x] `docs/AGENT-RULES.md` 与 pytest 入口一致
- [x] `BITFUN_BUNDLE` 与 selector 与迁移前一致
- [x] 未做禁止项（无 WebDriverIO、无平台子目录、无弱化断言）
