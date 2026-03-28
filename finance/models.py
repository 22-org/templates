from datetime import datetime
from enum import Enum
from typing import List

from pydantic import BaseModel


class Sector(str, Enum):
    TECHNOLOGY = "technology"
    HEALTHCARE = "healthcare"
    FINANCE = "finance"
    ENERGY = "energy"
    CONSUMER = "consumer"
    INDUSTRIAL = "industrial"
    REAL_ESTATE = "real_estate"
    UTILITIES = "utilities"


class TrendType(str, Enum):
    POSITIVE = "positive"
    NEGATIVE = "negative"
    NEUTRAL = "neutral"


class Company(BaseModel):
    id: str
    name: str
    sector: Sector
    description: str
    founded_year: int
    employee_count: int
    market_cap: float
    revenue: float


class StockPrice(BaseModel):
    symbol: str
    timestamp: datetime
    price: float
    volume: int
    open_price: float
    high_price: float
    low_price: float
    change_percent: float


class NewsItem(BaseModel):
    id: str
    symbol: str
    timestamp: datetime
    headline: str
    summary: str
    sentiment: TrendType
    impact_score: float  # 0-1


class Product(BaseModel):
    id: str
    symbol: str
    name: str
    description: str
    launch_date: datetime
    success_score: float  # 0-1


class Trend(BaseModel):
    id: str
    symbol: str
    timestamp: datetime
    trend_type: TrendType
    description: str
    confidence: float  # 0-1


class Stock(BaseModel):
    symbol: str
    company: Company
    current_price: float
    last_month_orders: int = 0
    prices: List[StockPrice]
    news: List[NewsItem]
    products: List[Product]
    trends: List[Trend]

    @property
    def latest_price(self) -> StockPrice:
        return max(self.prices, key=lambda p: p.timestamp)


class Customer(BaseModel):
    id: str
    name: str
    description: str
    risk_tolerance: float  # 0-1
    preferred_sectors: List[Sector]
    investment_history: List[str]  # list of symbols


class PersonalizedRank(BaseModel):
    symbol: str
    rank_score: float
    rank_position: int
    reasoning: str
