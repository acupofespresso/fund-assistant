"""天天基金 API 客户端 / TianTian Fund API Client"""

import json
import re
from datetime import datetime
from decimal import Decimal

from fund_assistant.api.base import BaseClient
from fund_assistant.models import FundPrice, HistoricalNav


class TianTianAPI(BaseClient):
    """天天基金 API / TianTian Fund API"""

    ESTIMATE_URL = "http://fundgz.1234567.com.cn/js/{code}.js"
    HISTORY_URL = "https://fundf10.eastmoney.com/F10DataApi.aspx"

    def get_realtime_estimate(self, code: str) -> FundPrice | None:
        """获取实时估值 / Get real-time estimate.

        Args:
            code: Fund code (e.g., "110022")

        Returns:
            FundPrice object with estimate data, or None if failed
        """
        try:
            url = self.ESTIMATE_URL.format(code=code)
            response = self.get(url)
            response.raise_for_status()

            # Parse JSONP response: jsonpgz({"fundcode":"110022", ...});
            match = re.search(r"jsonpgz\((.*?)\)", response.text)
            if not match:
                return None

            data = json.loads(match.group(1))

            # Parse estimate time (format: "2024-01-30 15:00")
            estimate_time = None
            if data.get("gztime"):
                try:
                    estimate_time = datetime.strptime(data["gztime"], "%Y-%m-%d %H:%M")
                except ValueError:
                    pass

            # Parse NAV date
            nav_date = None
            if data.get("jzrq"):
                try:
                    nav_date = datetime.strptime(data["jzrq"], "%Y-%m-%d").date()
                except ValueError:
                    pass

            return FundPrice(
                code=data["fundcode"],
                name=data["name"],
                estimate_value=Decimal(data.get("gsz", "0")) if data.get("gsz") else None,
                estimate_time=estimate_time,
                estimate_change=(
                    Decimal(data.get("gszzl", "0")) if data.get("gszzl") else None
                ),
                nav=Decimal(data.get("dwjz", "0")) if data.get("dwjz") else None,
                nav_date=nav_date,
            )
        except Exception as e:
            print(f"Error fetching estimate for {code}: {e}")
            return None

    def get_historical_nav(self, code: str, limit: int = 10) -> list[HistoricalNav]:
        """获取历史净值 / Get historical NAV.

        Args:
            code: Fund code
            limit: Number of records to fetch

        Returns:
            List of HistoricalNav objects
        """
        try:
            url = f"{self.HISTORY_URL}?type=lsjz&code={code}&page=1&per={limit}"
            response = self.get(url)
            response.raise_for_status()

            # Parse JavaScript response containing HTML table
            # Format: var apidata={ content:"<table>...</table>",records:3736,pages:374,curpage:1};
            match = re.search(r'content:"(.*?)",records', response.text, re.DOTALL)
            if not match:
                return []

            html = match.group(1)
            rows = re.findall(r"<tr>(.*?)</tr>", html)

            results = []
            for row in rows[1:]:  # Skip header row
                cells = re.findall(r"<td[^>]*>(.*?)</td>", row)
                if len(cells) >= 4:
                    # Clean HTML tags
                    date_str = re.sub(r"<[^>]+>", "", cells[0])
                    nav_str = re.sub(r"<[^>]+>", "", cells[1])
                    acc_str = re.sub(r"<[^>]+>", "", cells[2])
                    change_str = re.sub(r"<[^>]+>", "", cells[3])

                    try:
                        results.append(
                            HistoricalNav(
                                date=datetime.strptime(date_str, "%Y-%m-%d").date(),
                                nav=Decimal(nav_str),
                                accumulated_nav=Decimal(acc_str),
                                daily_change=(
                                    Decimal(change_str.replace("%", ""))
                                    if change_str != "---"
                                    else None
                                ),
                            )
                        )
                    except (ValueError, IndexError):
                        continue

            return results
        except Exception as e:
            print(f"Error fetching history for {code}: {e}")
            return []
