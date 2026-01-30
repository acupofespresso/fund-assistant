"""Enumeration types for fund assistant."""

from enum import Enum


class FundType(str, Enum):
    """基金类型 / Fund Type"""

    STOCK = "stock"  # 股票型
    HYBRID = "hybrid"  # 混合型
    BOND = "bond"  # 债券型
    INDEX = "index"  # 指数型
    MONEY = "money"  # 货币型
    QDII = "qdii"  # QDII


class RiskLevel(str, Enum):
    """风险等级 / Risk Level"""

    VERY_LOW = "极低风险"  # Very Low Risk
    LOW = "低风险"  # Low Risk
    MEDIUM = "中风险"  # Medium Risk
    MEDIUM_HIGH = "中高风险"  # Medium-High Risk
    HIGH = "高风险"  # High Risk


class Frequency(str, Enum):
    """定投频率 / DCA Frequency"""

    DAILY = "daily"  # 每日
    WEEKLY = "weekly"  # 每周
    MONTHLY = "monthly"  # 每月
