"""Rich formatter for terminal output."""

from decimal import Decimal

from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.text import Text

from fund_assistant.models import FundBasic, FundPrice, HistoricalNav


class FundFormatter:
    """格式化终端输出 / Terminal Output Formatter"""

    def __init__(self, console: Console | None = None):
        """Initialize formatter.

        Args:
            console: Rich console instance
        """
        self.console = console or Console()

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
