---
name: fund-assistant
description: "通用基金投资工具 / Universal Fund Assistant - 查询净值、筛选基金、对比分析、定投计算。支持作为独立 CLI 运行或集成至各类 AI Agent 系统。"
---

一个专业的基金投资工具，可作为独立命令行应用运行，也支持集成到 Openclaw、Agno 等多种 AI Agent 框架中，帮助你查询基金净值、筛选投资标的、对比分析、计算定投收益。

A professional fund investment tool that can run as a standalone CLI application or be integrated into various AI Agent frameworks like Openclaw, Agno, etc., for querying fund prices, screening investment targets, comparative analysis, and DCA calculation.

## 功能特性 / Features

- 📋 **基金列表 / Fund List** - 常用基金代码速查
  - Quick reference for commonly used fund codes

- 💰 **净值查询 / NAV Query** - 查询基金实时估值和确认净值
  - Query real-time estimates and confirmed NAV

- 📅 **历史净值 / Historical NAV** - 查看基金历史净值走势
  - View historical NAV trends

- 🔥 **热门基金 / Hot Funds** - 推荐热门投资标的
  - Recommend popular investment targets

- 🔍 **搜索基金 / Search Funds** - 按名称或代码搜索
  - Search by name or code

- 🧮 **定投计算器 / DCA Calculator** - 计算定投收益（支持多场景）
  - Calculate Dollar-Cost Averaging returns (multiple scenarios)

- 💼 **投资摘要 / Summary** - 主流基金分类介绍
  - Introduction to mainstream fund categories

## 安装 / Installation

### 使用 uv (推荐 / Recommended)

```bash
# 进入 skill 目录
cd fund-assistant

# 创建虚拟环境并安装依赖
uv venv
uv pip install -e .

# 验证安装
uv run fund-assistant --help
```

### 使用 pip (备选 / Alternative)

```bash
cd fund-assistant

# 创建虚拟环境
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate

# 安装依赖
pip install -e .

# 验证安装
fund-assistant --help
```

## 使用方法 / Usage

### 1. 查看基金列表 / View Fund List

```bash
# 查看所有基金
fund-assistant list

# 查看特定类型基金
fund-assistant list --type stock    # 股票型
fund-assistant list --type bond     # 债券型
fund-assistant list --type hybrid   # 混合型
fund-assistant list --type index    # 指数型
fund-assistant list --type money    # 货币型
```

### 2. 查询净值 / Query NAV

```bash
# 查询易方达消费行业
fund-assistant price 110022

# 查询招商中证白酒
fund-assistant price 161725
```

**输出示例:**
```
╭──────── 📈 易方达消费行业 (110022) ────────╮
│                                             │
│ 实时估值 / Real-time Estimate               │
│   估算净值: ¥3.8910                         │
│   估值时间: 2024-01-30 15:00                │
│   估算涨跌: +0.96% 📈                        │
│                                             │
│ 确认净值 / Confirmed NAV                    │
│   单位净值: ¥3.8540                         │
│   累计净值: ¥3.8540                         │
│   净值日期: 2024-01-29                      │
│                                             │
│ 💡 提示: 估值仅供参考，以当日确认净值为准    │
╰─────────────────────────────────────────────╯
```

### 3. 历史净值 / Historical NAV

```bash
# 查询最近 10 条净值记录
fund-assistant history 110022

# 查询最近 30 条记录
fund-assistant history 110022 --limit 30
fund-assistant history 110022 -n 30
```

### 4. 热门基金推荐 / Hot Fund Recommendations

```bash
# 查看所有热门基金
fund-assistant hot

# 查看特定类型热门基金
fund-assistant hot --type stock
```

### 5. 搜索基金 / Search Funds

```bash
# 按名称搜索
fund-assistant search 易方达

# 按代码搜索
fund-assistant search 110022

# 搜索公司
fund-assistant search 天弘
```

### 6. 定投计算 / DCA Calculation

```bash
# 每月定投 1000 元，定投 10 年
fund-assistant calc 110022 1000 10

# 每周定投 500 元，定投 5 年
fund-assistant calc 110022 500 5 --freq weekly
fund-assistant calc 110022 500 5 -f weekly
```

**输出包含三种场景:**
- 保守 6% 年化收益
- 中性 8% 年化收益
- 乐观 10% 年化收益

### 7. 投资摘要 / Investment Summary

```bash
fund-assistant summary
```

## 常用基金代码 / Common Fund Codes

### 股票型基金 / Stock Funds

| 代码 / Code | 名称 / Name | 风险 / Risk |
|------------|-------------|-------------|
| 110022 | 易方达消费行业 | 高风险 |
| 161725 | 招商中证白酒 | 高风险 |
| 005827 | 易方达蓝筹精选 | 中高风险 |
| 110011 | 易方达中小盘 | 高风险 |

### 混合型基金 / Hybrid Funds

| 代码 / Code | 名称 / Name | 风险 / Risk |
|------------|-------------|-------------|
| 163406 | 兴全合润 | 中高风险 |
| 519772 | 交银成长30 | 中高风险 |
| 001595 | 天弘中证500 | 中风险 |

### 债券型基金 / Bond Funds

| 代码 / Code | 名称 / Name | 风险 / Risk |
|------------|-------------|-------------|
| 110051 | 易方达纯债债券A | 低风险 |
| 000914 | 中加纯债债券A | 低风险 |
| 003376 | 易方达安悦超短债A | 极低风险 |

### 指数型基金 / Index Funds

| 代码 / Code | 名称 / Name | 风险 / Risk |
|------------|-------------|-------------|
| 110026 | 易方达创业板ETF联接 | 高风险 |
| 000478 | 建信中证500 | 中高风险 |
| 001550 | 天弘中证50AH优选 | 中风险 |

### 货币基金 / Money Market Funds

| 代码 / Code | 名称 / Name | 风险 / Risk |
|------------|-------------|-------------|
| 000198 | 天弘余额宝 | 极低风险 |
| 000638 | 富国富钱包 | 极低风险 |

## 投资建议 / Investment Tips

1. **新手入门 / Beginners**: 推荐指数型基金或货币基金
   - Recommend index funds or money market funds

2. **稳健投资 / Stable Investment**: 关注债券型基金或混合型基金
   - Focus on bond funds or hybrid funds

3. **分散投资 / Diversification**: 组合配置不同类型基金
   - Portfolio allocation with different fund types

4. **长期持有 / Long-term Holding**: 基金投资适合长期持有（3年以上）
   - Fund investment suits long-term holding (3+ years)

5. **定投策略 / DCA Strategy**: 通过定投平滑市场波动
   - Smooth market volatility through DCA

## 数据来源 / Data Source

- 天天基金 (1234567.com.cn) - 实时估值
- 东方财富 (eastmoney.com) - 历史净值
- Free API, no API Key required

## 技术栈 / Tech Stack

- **Python 3.10+** - 主语言
- **uv** - 包管理器
- **Typer** - CLI 框架
- **Rich** - 终端美化
- **httpx** - HTTP 客户端
- **Pydantic** - 数据验证

## 开发 / Development

```bash
# 安装开发依赖
uv pip install -e ".[dev]"

# 运行测试
uv run pytest

# 代码检查
uv run ruff check .

# 格式化代码
uv run ruff format .
```

## 注意事项 / Notes

⚠️ **投资有风险，入市需谨慎**  
⚠️ **Investment involves risk, invest cautiously**

⚠️ **历史收益不代表未来表现**  
⚠️ **Past performance does not guarantee future results**

⚠️ **仅供参考，不构成投资建议**  
⚠️ **For reference only, not investment advice**

## License

MIT License
