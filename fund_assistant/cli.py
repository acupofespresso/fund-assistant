"""CLI commands for fund assistant."""

from typing import List
from typing_extensions import Annotated

import typer
from rich.console import Console

from fund_assistant.services import FundService
from fund_assistant.ui import FundFormatter

app = typer.Typer(
    name="fund-assistant",
    help="📊 基金投资助理 / Fund Investment Assistant",
    add_completion=False,
    no_args_is_help=True,
)

console = Console()
fund_service = FundService()
formatter = FundFormatter(console)


@app.command()
def info(code: Annotated[str, typer.Argument(help="基金代码 / Fund code")]):
    """ℹ️ 基金详情 (规模/费率/业绩) / Fund Details"""
    detail = fund_service.get_fund_detail(code)
    formatter.display_fund_detail(detail)


@app.command()
def holding(code: Annotated[str, typer.Argument(help="基金代码 / Fund code")]):
    """📊 持仓分析 (前十大重仓) / Holdings Analysis"""
    holding = fund_service.get_fund_holdings(code)
    formatter.display_fund_holdings(holding)


@app.command()
def compare(
    codes: Annotated[List[str], typer.Argument(help="基金代码列表 (空格分隔) / Fund codes")]
):
    """🆚 基金对比 (2-4只) / Compare Funds"""
    if len(codes) < 2:
        console.print("[red]⚠️ 请至少输入2个基金代码进行对比 / Please input at least 2 fund codes[/red]")
        raise typer.Exit(1)
    
    details = fund_service.compare_funds(codes)
    formatter.display_comparison(details)


@app.command()
def manager(code: Annotated[str, typer.Argument(help="基金代码 / Fund code")]):
    """🧑‍💼 基金经理 (姓名/公司) / Fund Manager"""
    # Currently reusing basic detail to get manager name
    detail = fund_service.get_fund_detail(code)
    if detail:
        console.print(f"🧑‍💼 基金经理: [bold cyan]{detail.manager}[/bold cyan]")
        console.print(f"🏢 基金公司: {detail.company}")
        console.print("[dim]更多经理数据接入中... / More manager data coming soon...[/dim]")
    else:
        console.print("[red]❌ 无法获取信息 / Failed to fetch info[/red]")


@app.command()
def list(
    type: Annotated[
        str | None, typer.Option("--type", "-t", help="基金类型: stock/bond/hybrid/index/money")
    ] = None,
):
    """📋 显示常用基金列表 / Show fund list"""
    funds = fund_service.get_fund_list(fund_type=type)
    formatter.display_fund_list(funds)


@app.command()
def price(code: Annotated[str, typer.Argument(help="基金代码 / Fund code")]):
    """💰 查询基金实时估值和净值 / Query fund price"""
    fund_data = fund_service.get_fund_price(code)
    formatter.display_fund_price(fund_data)


@app.command()
def history(
    code: Annotated[str, typer.Argument(help="基金代码 / Fund code")],
    limit: Annotated[int, typer.Option("--limit", "-n", help="显示条数 / Number of records")] = 10,
):
    """📅 查询历史净值 / Query historical NAV"""
    history_data = fund_service.get_history(code, limit)
    formatter.display_history(history_data, code)


@app.command()
def hot(
    type: Annotated[
        str | None, typer.Option("--type", "-t", help="基金类型 / Fund type")
    ] = None,
):
    """🔥 显示热门基金 / Show hot funds"""
    hot_funds = fund_service.get_hot_funds(fund_type=type)
    formatter.display_hot_funds(hot_funds)


@app.command()
def search(keyword: Annotated[str, typer.Argument(help="搜索关键词 / Search keyword")]):
    """🔍 搜索基金 (支持名称/代码) / Search funds"""
    results = fund_service.search_funds(keyword)
    formatter.display_search_results(results, keyword)


@app.command()
def calc(
    code: Annotated[str, typer.Argument(help="基金代码 / Fund code")],
    amount: Annotated[float, typer.Argument(help="每期金额 / Amount per period")],
    years: Annotated[int, typer.Argument(help="定投年限 / Years")],
    frequency: Annotated[
        str, typer.Option("--freq", "-f", help="定投频率: monthly/weekly / Frequency")
    ] = "monthly",
):
    """🧮 定投计算器 / DCA Calculator"""
    if frequency not in ["monthly", "weekly", "daily"]:
        console.print(
            "[red]❌ 频率必须是 monthly/weekly/daily / Frequency must be monthly/weekly/daily[/red]"
        )
        raise typer.Exit(1)

    result = fund_service.calculate_dca(code, amount, years, frequency)
    formatter.display_calculator(result)


@app.command()
def summary():
    """💼 基金投资摘要 / Investment summary"""
    from rich.markdown import Markdown

    summary_text = """
# 💼 基金投资摘要 / Fund Investment Summary

## 📌 主流基金分类 / Main Fund Categories

### 【股票型基金 / Stock Funds】
- **易方达消费行业 (110022)** - 消费龙头
- **招商中证白酒 (161725)** - 白酒行业
- **易方达蓝筹精选 (005827)** - 蓝筹成长

### 【混合型基金 / Hybrid Funds】
- **兴全合润 (163406)** - 灵活配置
- **交银成长30 (519772)** - 成长精选

### 【债券型基金 / Bond Funds】
- **易方达纯债债券A (110051)** - 稳健收益
- **中加纯债债券A (000914)** - 低风险

### 【指数型基金 / Index Funds】
- **易方达创业板ETF联接 (110026)** - 创业板
- **建信中证500 (000478)** - 中证500

### 【货币基金 / Money Market Funds】
- **天弘余额宝 (000198)** - 流动性最佳
- **富国富钱包 (000638)** - 稳健选择

---

## ⚠️ 风险提示 / Risk Warning

- 投资有风险，入市需谨慎 / Investment involves risk
- 历史收益不代表未来表现 / Past performance ≠ future results
- 仅供参考，不构成投资建议 / For reference only, not investment advice

"""
    md = Markdown(summary_text)
    console.print(md)


if __name__ == "__main__":
    app()
