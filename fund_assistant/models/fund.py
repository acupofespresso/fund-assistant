"""Fund data models."""

from datetime import date, datetime
from decimal import Decimal

from pydantic import BaseModel, Field

from fund_assistant.models.enums import FundType, RiskLevel


class FundBasic(BaseModel):
    """基金基本信息 / Fund Basic Information"""

    code: str = Field(..., description="基金代码")
    name: str = Field(..., description="基金名称")
    fund_type: FundType = Field(..., description="基金类型")
    risk_level: RiskLevel = Field(..., description="风险等级")

    class Config:
        use_enum_values = True


class FundPrice(BaseModel):
    """基金净值信息 / Fund Price Information"""

    code: str
    name: str

    # 实时估值 / Real-time Estimate
    estimate_value: Decimal | None = Field(None, description="估算净值")
    estimate_time: datetime | None = Field(None, description="估值时间")
    estimate_change: Decimal | None = Field(None, description="估算涨跌幅 %")

    # 确认净值 / Confirmed NAV
    nav: Decimal | None = Field(None, description="单位净值")
    nav_date: date | None = Field(None, description="净值日期")
    accumulated_nav: Decimal | None = Field(None, description="累计净值")

    # 基金信息 / Fund Information
    fund_type: FundType | None = None
    risk_level: RiskLevel | None = None
    scale: Decimal | None = Field(None, description="基金规模(亿)")
    manager_name: str | None = Field(None, description="基金经理")


class HistoricalNav(BaseModel):
    """历史净值 / Historical NAV"""

    date: date
    nav: Decimal
    accumulated_nav: Decimal
    daily_change: Decimal | None = Field(None, description="日涨跌幅 %")


class FundManager(BaseModel):
    """基金经理信息 / Fund Manager Information"""

    name: str
    years_of_service: float | None = Field(None, description="从业年限")
    managed_funds_count: int | None = Field(None, description="管理基金数量")
    total_return: Decimal | None = Field(None, description="任职总回报 %")

    # 管理的基金列表 / Managed Funds
    managed_funds: list[FundBasic] = Field(default_factory=list)

    # 历史业绩 / Historical Performance
    return_1y: Decimal | None = None
    return_3y: Decimal | None = None
    return_5y: Decimal | None = None


class HoldingStock(BaseModel):
    """持仓股票 / Holding Stock"""

    code: str
    name: str
    percentage: Decimal = Field(..., description="占净值比例 %")


class FundHolding(BaseModel):
    """基金持仓 / Fund Holding"""

    code: str
    name: str
    report_date: date = Field(..., description="报告期")

    # 十大重仓股 / Top 10 Holdings
    top_stocks: list[HoldingStock] = Field(default_factory=list)

    # 资产配置 / Asset Allocation
    stock_percentage: Decimal | None = Field(None, description="股票占比 %")
    bond_percentage: Decimal | None = Field(None, description="债券占比 %")
    cash_percentage: Decimal | None = Field(None, description="现金占比 %")


class FundDetail(BaseModel):
    """基金详细信息 / Fund Detail"""
    
    code: str
    name: str
    fund_type: str
    
    # 基本信息
    establish_date: date | None = None
    company: str | None = None
    manager: str | None = None
    fund_size: Decimal | None = Field(None, description="基金规模(元)")
    
    # 费率
    management_fee: str | None = None # 费率可能带%
    
    # 评级/风险
    risk_level: str | None = None
    rating: str | None = None
    
    # 业绩表现 (Returns)
    return_1m: Decimal | None = None
    return_6m: Decimal | None = None
    return_1y: Decimal | None = None
    return_3y: Decimal | None = None
    return_inception: Decimal | None = None
