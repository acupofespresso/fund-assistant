# 📊 Fund-Assistant

[![Python Version](https://img.shields.io/badge/python-3.10%2B-blue.svg)](https://www.python.org/)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)
[![Tool](https://img.shields.io/badge/tool-uv-orange.svg)](https://github.com/astral-sh/uv)
[![UI](https://img.shields.io/badge/UI-Rich-magenta.svg)](https://github.com/Textualize/rich)

**通用基金投资助手 (Universal Fund Assistant)** - 一个基于 Python + uv 构建的现代化基金分析工具。它既可以作为独立的 CLI 工具使用，也支持集成到各种 AI Agent 框架（如 Openclaw, Agno 等）中作为扩展插件。支持实时估值查询、历史净值分析、定投收益模拟等功能。

---

## ✨ 核心特性 / Features

- 💰 **实时净值查询**：获取基金实时盘中估值及最新确认净值。
- 📅 **历史趋势分析**：快速拉取历史净值列表，分析涨跌变化。
- 🧮 **智能定投计算器**：支持多场景收益模拟（保守/中性/乐观），支持月/周/日频率。
- 🔥 **热门/分类筛选**：内置常用基金列表，支持按类型（股票、债券、混合、指数）快速筛选。
- 🔍 **智能搜索**：支持按名称或 6 位基金代码模糊匹配。
- 💼 **投资摘要**：一键生成全市场主流基金分类概览。
- 🎨 **专业终端 UI**：基于 Rich 打造，支持彩色表格、面板嵌套及 Markdown 渲染。
- ⚡ **极致性能**：采用 `uv` 包管理工具，安装与运行速度极快。

---

## 📸 运行预览 / Previews

### 1. 实时价格查询 (`price`)
```text
╭────────────────── 📈 易方达消费行业 (110022) ──────────────────╮
│                                                                 │
│ 实时估值 / Real-time Estimate                                   │
│   估算净值: ¥3.3388                                             │
│   估值时间: 2026-01-30 15:00                                    │
│   估算涨跌: -2.37% 📉                                           │
│                                                                 │
│ 确认净值 / Confirmed NAV                                        │
│   单位净值: ¥3.4200                                             │
│   净值日期: 2026-01-29                                          │
│                                                                 │
│ 💡 提示: 估值仅供参考，以当日确认净值为准                       │
╰─────────────────────────────────────────────────────────────────╯
```

### 2. 定投收益计算 (`calc`)
```text
╭────────────────── 🧮 定投模拟 - 110022 ──────────────────╮
│ 投资参数: 每月1000元 | 定投10年 | 总投入 ¥120,000.00      │
│                                                          │
│ [中性 8%]                                                │
│   预计价值: ¥182,946.04                                  │
│   预计收益: ¥62,946.04   收益率: 52.46%                  │
╰──────────────────────────────────────────────────────────╯
```

---

## 🛠️ 技术栈 / Tech Stack

- **Core**: Python 3.10+
- **CLI**: [Typer](https://typer.tiangolo.com/) - 现代化的命令行框架
- **UI**: [Rich](https://github.com/Textualize/rich) - 终端美化与排版
- **API**: [HTTPX](https://www.python-httpx.org/) - 高性能 HTTP 客户端
- **Data**: [Pydantic v2](https://docs.pydantic.dev/) - 类型安全与数据验证
- **Package Manager**: [uv](https://github.com/astral-sh/uv) - 极速 Python 工具链

---

## 🚀 快速开始 / Quick Start

### 1. 克隆与安装

推荐使用 `uv` 进行安装，如果您还没有安装 `uv`，可以通过 `curl -LsSf https://astral.sh/uv/install.sh | sh` 安装。

```bash
# 进入项目目录
cd fund-assistant

# 创建虚拟环境并安装依赖
uv venv
uv pip install -e .
```

### 2. 常用命令

```bash
# 查询行情
uv run fund-assistant price 110022

# 历史净值 (最近20条)
uv run fund-assistant history 110022 --limit 20

# 定投计算 (每月定投2000，定投5年)
uv run fund-assistant calc 110022 2000 5

# 搜索基金
uv run fund-assistant search 易方达

# 查看帮助
uv run fund-assistant --help
```

## 🔌 智能体集成 / Agent Integration

本工具遵循标准化 CLI 设计，可以轻松集成到各类 AI 智能体应用中：

### 1. Openclaw
作为 `Skill` 引入，将 `SKILL.md` 放置在 workspace 的 skills 目录下即可。

### 2. Agno (原 Phidata)
可以使用 `ShellTools` 直接调用，或者通过 Python 函数封装：
```python
from agno.agent import Agent
from agno.tools.shell import ShellTools

agent = Agent(
    tools=[ShellTools()],
    description="你是一个基金投资专家，可以使用 fund-assistant 工具查询数据。",
)
agent.print_response("查询基金 110022 的实时价格")
```

### 3. 通用 CLI / Universal CLI
任何支持命令行调用的智能体框架都可以通过 `uv run fund-assistant <command>` 来获取结构化或格式化的基金数据。

---

## 📂 项目结构 / Structure

```text
fund_assistant/
├── api/          # 接口层 (天天基金、东方财富 API)
├── models/       # 模型层 (Pydantic models, Enums)
├── services/     # 业务层 (定投算法、数据整合)
├── ui/           # 渲染层 (Rich Table/Panel 格式化)
├── data/         # 数据层 (基金静态列表)
└── cli.py        # 路由层 (Typer Commands)
```

---

## 📡 数据来源 / Data Sources

- **天天基金 (TianTian Fund)**: 提供盘中实时估值数据。
- **东方财富 (EastMoney)**: 提供历史净值、基金详情及评级数据。

---

## ⚠️ 免责声明 / Disclaimer

- 本工具仅供学习研究使用，不构成任何投资建议。
- 投资有风险，入市需谨慎。
- 历史业绩不预示其未来表现。

---

## 📄 开源协议 / License

本项目采用 [MIT License](LICENSE) 协议。
