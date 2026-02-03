"""Fund query and analysis service."""

import json
from decimal import Decimal
from pathlib import Path

from fund_assistant.api import TianTianAPI
from fund_assistant.models import (
    FundBasic, 
    FundPrice, 
    FundType, 
    HistoricalNav, 
    RiskLevel,
    FundDetail,
    FundHolding
)


class FundService:
    """基金查询服务 / Fund Query Service"""

    def __init__(self):
        """Initialize fund service."""
        self.api = TianTianAPI()
        self._load_fund_data()

    def get_fund_detail(self, code: str) -> FundDetail | None:
        """获取基金详细信息 / Get fund detail."""
        return self.api.get_fund_detail(code)

    def get_fund_holdings(self, code: str) -> FundHolding | None:
        """获取基金持仓 / Get fund holdings."""
        return self.api.get_fund_holdings(code)

    def compare_funds(self, codes: list[str]) -> list[FundDetail]:
        """对比基金 / Compare funds.
        
        Args:
            codes: List of fund codes

        Returns:
            List of FundDetail objects
        """
        results = []
        for code in codes:
            detail = self.get_fund_detail(code)
            if detail:
                results.append(detail)
        return results

    def _load_fund_data(self):
        """加载基金静态数据 / Load static fund data."""
        data_file = Path(__file__).parent.parent / "data" / "funds.json"
        with open(data_file, "r", encoding="utf-8") as f:
            self.fund_data = json.load(f)

    def get_fund_list(self, fund_type: str | None = None) -> list[FundBasic]:
        """获取基金列表 / Get fund list.

        Args:
            fund_type: Filter by fund type (stock/bond/hybrid/index/money)

        Returns:
            List of FundBasic objects
        """
        funds = []

        if fund_type:
            # Filter by specific type
            if fund_type in self.fund_data:
                for item in self.fund_data[fund_type]:
                    funds.append(
                        FundBasic(
                            code=item["code"],
                            name=item["name"],
                            fund_type=FundType(item["fund_type"]),
                            risk_level=RiskLevel(item["risk_level"]),
                        )
                    )
        else:
            # Return all funds
            for category in self.fund_data.values():
                for item in category:
                    funds.append(
                        FundBasic(
                            code=item["code"],
                            name=item["name"],
                            fund_type=FundType(item["fund_type"]),
                            risk_level=RiskLevel(item["risk_level"]),
                        )
                    )

        return funds

    def get_fund_price(self, code: str) -> FundPrice | None:
        """获取基金价格信息 / Get fund price information.

        Args:
            code: Fund code

        Returns:
            FundPrice object or None if not found
        """
        return self.api.get_realtime_estimate(code)

    def get_history(self, code: str, limit: int = 10) -> list[HistoricalNav]:
        """获取历史净值 / Get historical NAV.

        Args:
            code: Fund code
            limit: Number of records

        Returns:
            List of HistoricalNav objects
        """
        return self.api.get_historical_nav(code, limit)

    def get_hot_funds(self, fund_type: str | None = None) -> list[FundBasic]:
        """获取热门基金 / Get hot funds.

        Args:
            fund_type: Filter by fund type

        Returns:
            List of hot FundBasic objects
        """
        funds = []

        if fund_type:
            if fund_type in self.fund_data:
                for item in self.fund_data[fund_type]:
                    if item.get("hot", False):
                        funds.append(
                            FundBasic(
                                code=item["code"],
                                name=item["name"],
                                fund_type=FundType(item["fund_type"]),
                                risk_level=RiskLevel(item["risk_level"]),
                            )
                        )
        else:
            for category in self.fund_data.values():
                for item in category:
                    if item.get("hot", False):
                        funds.append(
                            FundBasic(
                                code=item["code"],
                                name=item["name"],
                                fund_type=FundType(item["fund_type"]),
                                risk_level=RiskLevel(item["risk_level"]),
                            )
                        )

        return funds

    def search_funds(self, keyword: str) -> list[FundBasic]:
        """搜索基金 / Search funds.

        Args:
            keyword: Search keyword (code or name)

        Returns:
            List of matching FundBasic objects
        """
        keyword_lower = keyword.lower()
        results = []

        for category in self.fund_data.values():
            for item in category:
                if (
                    keyword_lower in item["code"].lower()
                    or keyword_lower in item["name"].lower()
                ):
                    results.append(
                        FundBasic(
                            code=item["code"],
                            name=item["name"],
                            fund_type=FundType(item["fund_type"]),
                            risk_level=RiskLevel(item["risk_level"]),
                        )
                    )

        return results

    def calculate_dca(
        self, code: str, amount: float, years: int, frequency: str = "monthly"
    ) -> dict:
        """定投计算器 / DCA Calculator.

        Args:
            code: Fund code
            amount: Investment amount per period
            years: Investment period in years
            frequency: Investment frequency (monthly/weekly/daily)

        Returns:
            Dictionary with calculation results
        """
        # Calculate number of periods
        periods_map = {"monthly": 12, "weekly": 52, "daily": 250}
        periods = years * periods_map.get(frequency, 12)

        total_invest = amount * periods

        # Simple scenarios with different annual returns
        scenarios = {"conservative": 0.06, "neutral": 0.08, "optimistic": 0.10}

        results = {"code": code, "amount": amount, "years": years, "frequency": frequency}

        results["total_invest"] = total_invest
        results["scenarios"] = {}

        for scenario_name, annual_return in scenarios.items():
            period_return = annual_return / periods_map.get(frequency, 12)

            # Future value of annuity formula
            if period_return > 0:
                future_value = amount * ((1 + period_return) ** periods - 1) / period_return
            else:
                future_value = total_invest

            profit = future_value - total_invest

            results["scenarios"][scenario_name] = {
                "annual_return": annual_return,
                "future_value": round(future_value, 2),
                "profit": round(profit, 2),
                "return_rate": round((profit / total_invest) * 100, 2) if total_invest > 0 else 0,
            }

        return results
