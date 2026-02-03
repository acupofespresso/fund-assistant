"""Rich formatter for terminal output."""

from decimal import Decimal

from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.text import Text

from fund_assistant.models import (
    FundBasic, 
    FundPrice, 
    HistoricalNav, 
    FundDetail, 
    FundHolding
)


class FundFormatter:
    """格式化终端输出 / Terminal Output Formatter"""
    
    def __init__(self, console: Console | None = None):
        """Initialize formatter."""
        self.console = console or Console()

    def display_fund_detail(self, detail: FundDetail):
        """显示基金详细信息 / Display fund details."""
        if not detail:
            self.console.print("[red]❌ 无法获取基金详情 / Failed to fetch fund detail[/red]")
            return

        title = f"ℹ️ 基金详情 / Fund Details - {detail.name} ({detail.code})"
        
        content = []
        
        # Basic Info
        content.append(f"[bold]基本信息 / Basic Info[/bold]")
        content.append(f"  类型: {detail.fund_type}")
        content.append(f"  成立日期: {detail.establish_date}")
        content.append(f"  基金公司: {detail.company}")
        content.append(f"  基金经理: {detail.manager}")
        if detail.fund_size:
            size_yi = detail.fund_size / Decimal(100000000)
            content.append(f"  基金规模: {size_yi:.2f} 亿")
        
        # Fees & Risk
        content.append(f"\n[bold]费率与风险 / Fees & Risk[/bold]")
        content.append(f"  管理费率: {detail.management_fee}")
        content.append(f"  风险等级: {detail.risk_level}")
        
        # Performance
        content.append(f"\n[bold]阶段涨幅 / Performance[/bold]")
        
        def format_return(val):
            if val is None: return "---"
            color = "green" if val >= 0 else "red"
            return f"[{color}]{val:+.2f}%[/{color}]"
            
        content.append(f"  近1月: {format_return(detail.return_1m)}")
        content.append(f"  近6月: {format_return(detail.return_6m)}")
        content.append(f"  近1年: {format_return(detail.return_1y)}")
        content.append(f"  近3年: {format_return(detail.return_3y)}")
        content.append(f"  成立来: {format_return(detail.return_inception)}")

        panel = Panel("\n".join(content), title=title, border_style="blue")
        self.console.print(panel)

    def display_fund_holdings(self, holding: FundHolding):
        """显示基金持仓 / Display fund holdings."""
        if not holding:
            self.console.print("[red]❌ 无法获取持仓信息 / Failed to fetch holdings[/red]")
            return

        title = f"📊 持仓分析 / Holdings Analysis - {holding.code}"
        
        table = Table(title=title, show_header=True, header_style="bold magenta")
        table.add_column("股票代码\nCode", style="cyan", width=10)
        table.add_column("名称\nName", style="white", width=20)
        table.add_column("占比\n%", style="yellow", justify="right", width=10)

        for stock in holding.top_stocks:
            table.add_row(
                stock.code,
                stock.name,
                f"{stock.percentage:.2f}%"
            )
            
        self.console.print(table)
        self.console.print(f"[dim]报告期: {holding.report_date}[/dim]")

    def display_comparison(self, details: list[FundDetail]):
        """显示基金对比 / Display fund comparison."""
        if not details:
            self.console.print("[yellow]无数据对比 / No data to compare[/yellow]")
            return

        table = Table(title="🆚 基金对比 / Fund Comparison", show_header=True, header_style="bold green")
        
        # Columns: Metric, Fund A, Fund B ...
        table.add_column("指标\nMetric", style="white bold", width=15)
        
        for d in details:
            table.add_column(f"{d.name}\n{d.code}", justify="center", width=20)
            
        # Rows
        # Type
        row = ["类型"] + [d.fund_type for d in details]
        table.add_row(*row)
        
        # Size
        def format_size(d):
            if d.fund_size:
                return f"{d.fund_size / Decimal(100000000):.2f} 亿"
            return "---"
        row = ["规模"] + [format_size(d) for d in details]
        table.add_row(*row)
        
        # Manager
        row = ["经理"] + [d.manager or "---" for d in details]
        table.add_row(*row)

        # Risk
        row = ["风险"] + [str(d.risk_level) for d in details]
        table.add_row(*row)

        # Returns
        def format_ret(val):
            if val is None: return "---"
            color = "green" if val >= 0 else "red"
            return f"[{color}]{val:+.2f}%[/{color}]"

        row = ["近1年"] + [format_ret(d.return_1y) for d in details]
        table.add_row(*row)

        row = ["近3年"] + [format_ret(d.return_3y) for d in details]
        table.add_row(*row)
        
        row = ["成立来"] + [format_ret(d.return_inception) for d in details]
        table.add_row(*row)

        self.console.print(table)

    def display_fund_list(self, funds: list[FundBasic]):
        """显示基金列表 / Display fund list.

        Args:
            funds: List of FundBasic objects
        """
        if not funds:
            self.console.print("[yellow]未找到基金 / No funds found[/yellow]")
            return

        table = Table(title="📋 基金列表 / Fund List", show_header=True, header_style="bold cyan")
        table.add_column("代码\nCode", style="cyan", width=8)
        table.add_column("名称\nName", style="white", width=25)
        table.add_column("类型\nType", style="blue", width=10)
        table.add_column("风险\nRisk", style="yellow", width=10)

        for fund in funds:
            # Map type to Chinese
            type_map = {
                "stock": "股票型",
                "hybrid": "混合型",
                "bond": "债券型",
                "index": "指数型",
                "money": "货币型",
            }
            table.add_row(
                fund.code, fund.name, type_map.get(fund.fund_type, fund.fund_type), fund.risk_level
            )

        self.console.print(table)

    def display_fund_price(self, fund_price: FundPrice | None):
        """显示基金价格 / Display fund price.

        Args:
            fund_price: FundPrice object
        """
        if not fund_price:
            self.console.print("[red]❌ 无法获取基金数据 / Failed to fetch fund data[/red]")
            return

        # Build panel content
        content = []

        # Title
        title = f"📈 {fund_price.name} ({fund_price.code})"

        # Real-time estimate section
        if fund_price.estimate_value is not None:
            content.append("\n[bold]实时估值 / Real-time Estimate[/bold]")
            content.append(f"  估算净值: [green]¥{fund_price.estimate_value:.4f}[/green]")

            if fund_price.estimate_time:
                content.append(
                    f"  估值时间: {fund_price.estimate_time.strftime('%Y-%m-%d %H:%M')}"
                )

            if fund_price.estimate_change is not None:
                change_color = "green" if fund_price.estimate_change >= 0 else "red"
                change_symbol = "📈" if fund_price.estimate_change >= 0 else "📉"
                content.append(
                    f"  估算涨跌: [{change_color}]{fund_price.estimate_change:+.2f}%[/{change_color}] {change_symbol}"
                )

        # Confirmed NAV section
        if fund_price.nav is not None:
            content.append("\n[bold]确认净值 / Confirmed NAV[/bold]")
            content.append(f"  单位净值: [cyan]¥{fund_price.nav:.4f}[/cyan]")

            if fund_price.accumulated_nav:
                content.append(f"  累计净值: ¥{fund_price.accumulated_nav:.4f}")

            if fund_price.nav_date:
                content.append(f"  净值日期: {fund_price.nav_date}")

        # Add note
        content.append(
            "\n[dim]💡 提示: 估值仅供参考，以当日确认净值为准[/dim]"
        )
        content.append("[dim]   Note: Estimate is for reference only[/dim]")

        panel = Panel("\n".join(content), title=title, border_style="blue")
        self.console.print(panel)

    def display_history(self, history: list[HistoricalNav], code: str = ""):
        """显示历史净值 / Display historical NAV.

        Args:
            history: List of HistoricalNav objects
            code: Fund code for title
        """
        if not history:
            self.console.print("[yellow]未找到历史数据 / No historical data found[/yellow]")
            return

        title = f"📅 历史净值 / Historical NAV"
        if code:
            title += f" ({code})"

        table = Table(title=title, show_header=True, header_style="bold cyan")
        table.add_column("日期\nDate", style="cyan", width=12)
        table.add_column("单位净值\nNAV", style="white", justify="right", width=10)
        table.add_column("累计净值\nAcc NAV", style="white", justify="right", width=10)
        table.add_column("日增长率\nDaily Change", style="yellow", justify="right", width=12)

        for record in history:
            # Format daily change with color
            if record.daily_change is not None:
                change_color = "green" if record.daily_change >= 0 else "red"
                change_str = f"[{change_color}]{record.daily_change:+.2f}%[/{change_color}]"
            else:
                change_str = "---"

            table.add_row(
                str(record.date),
                f"{record.nav:.4f}",
                f"{record.accumulated_nav:.4f}",
                change_str,
            )

        self.console.print(table)

    def display_hot_funds(self, funds: list[FundBasic]):
        """显示热门基金 / Display hot funds.

        Args:
            funds: List of hot FundBasic objects
        """
        if not funds:
            self.console.print("[yellow]未找到热门基金 / No hot funds found[/yellow]")
            return

        table = Table(
            title="🔥 热门基金 / Hot Funds", show_header=True, header_style="bold red"
        )
        table.add_column("代码\nCode", style="cyan", width=8)
        table.add_column("名称\nName", style="white", width=25)
        table.add_column("类型\nType", style="blue", width=10)
        table.add_column("风险\nRisk", style="yellow", width=10)

        type_map = {
            "stock": "股票型",
            "hybrid": "混合型",
            "bond": "债券型",
            "index": "指数型",
            "money": "货币型",
        }

        for fund in funds:
            table.add_row(
                fund.code, fund.name, type_map.get(fund.fund_type, fund.fund_type), fund.risk_level
            )

        self.console.print(table)

    def display_search_results(self, results: list[FundBasic], keyword: str = ""):
        """显示搜索结果 / Display search results.

        Args:
            results: List of matching FundBasic objects
            keyword: Search keyword
        """
        if not results:
            self.console.print(
                f'[yellow]未找到匹配 "{keyword}" 的基金 / No funds found matching "{keyword}"[/yellow]'
            )
            return

        title = f"🔍 搜索结果 / Search Results"
        if keyword:
            title += f' - "{keyword}"'

        table = Table(title=title, show_header=True, header_style="bold cyan")
        table.add_column("代码\nCode", style="cyan", width=8)
        table.add_column("名称\nName", style="white", width=25)
        table.add_column("类型\nType", style="blue", width=10)
        table.add_column("风险\nRisk", style="yellow", width=10)

        type_map = {
            "stock": "股票型",
            "hybrid": "混合型",
            "bond": "债券型",
            "index": "指数型",
            "money": "货币型",
        }

        for fund in results:
            table.add_row(
                fund.code, fund.name, type_map.get(fund.fund_type, fund.fund_type), fund.risk_level
            )

        self.console.print(table)
        self.console.print(f"\n找到 [bold]{len(results)}[/bold] 个结果 / Found {len(results)} results")

    def display_calculator(self, result: dict):
        """显示定投计算结果 / Display DCA calculation result.

        Args:
            result: Calculation result dictionary
        """
        title = f"🧮 定投计算器 / DCA Calculator - {result['code']}"

        content = []
        content.append(f"[bold]投资参数 / Investment Parameters[/bold]")
        content.append(f"  每期金额: ¥{result['amount']:.2f}")
        content.append(f"  定投年限: {result['years']} 年")
        content.append(f"  定投频率: {result['frequency']}")
        content.append(f"  总投入: [cyan]¥{result['total_invest']:.2f}[/cyan]")
        content.append("")

        content.append("[bold]收益预测 / Profit Forecast[/bold]")

        scenario_names = {
            "conservative": "保守 6%",
            "neutral": "中性 8%",
            "optimistic": "乐观 10%",
        }

        for scenario_key, scenario_data in result["scenarios"].items():
            scenario_name = scenario_names.get(scenario_key, scenario_key)
            content.append(f"\n  [{scenario_name}]")
            content.append(f"    预计价值: [green]¥{scenario_data['future_value']:,.2f}[/green]")
            content.append(f"    预计收益: [yellow]¥{scenario_data['profit']:,.2f}[/yellow]")
            content.append(
                f"    收益率: [blue]{scenario_data['return_rate']:.2f}%[/blue]"
            )

        content.append("\n[dim]💡 提示: 实际收益取决于市场表现[/dim]")
        content.append("[dim]   Note: Actual returns depend on market performance[/dim]")

        panel = Panel("\n".join(content), title=title, border_style="green")
        self.console.print(panel)
