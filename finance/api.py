import json
from datetime import datetime
from typing import Dict, List

from data_generator import DataGenerator
from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from models import Customer, Sector, Stock
from pydantic import BaseModel
from ranking_engine import RankingEngine
from trading_engine import TradingEngine, TransactionType


class TradeRequest(BaseModel):
    customer_id: str
    symbol: str
    transaction_type: str
    quantity: int


app = FastAPI(title="Private Stock Exchange API", version="1.0.0")

# Initialize data
data_generator = DataGenerator()
ranking_engine = RankingEngine()
trading_engine = TradingEngine()
stocks = data_generator.generate_stocks()

# Sample customers
customers = [
    Customer(
        id="customer1",
        name="Conservative Investor",
        description=(
            "conservative investor who prioritizes capital preservation "
            "over high returns. Typically invests in blue-chip stocks with "
            "stable dividends, avoids high-volatility technology stocks, "
            "maintains diversified portfolio with 60% bonds/40% stocks "
            "allocation, and prefers companies with strong balance sheets "
            "and consistent earnings growth. Risk-averse, often sells "
            "positions quickly if they drop more than 5% from purchase "
            "price."
        ),
        risk_tolerance=0.2,
        preferred_sectors=[Sector.FINANCE, Sector.UTILITIES],
        investment_history=["STRIPE", "CHIME"],
    ),
    Customer(
        id="customer2",
        name="Aggressive Investor",
        description=(
            "aggressive growth investor seeking maximum returns through "
            "high-risk, high-reward strategies. Regularly invests in "
            "emerging technologies, startup IPOs, and volatile growth "
            "stocks. Willing to allocate 80-90% of portfolio to equities, "
            "frequently trades on momentum, uses leverage to amplify "
            "returns, and holds positions through significant drawdowns "
            "(20%+) expecting eventual recovery. Actively seeks disruptive "
            "companies with potential for 10x returns."
        ),
        risk_tolerance=0.8,
        preferred_sectors=[Sector.TECHNOLOGY, Sector.CONSUMER],
        investment_history=["OPENAI", "XAI"],
    ),
    Customer(
        id="customer3",
        name="Balanced Investor",
        description=(
            "balanced investor seeking moderate growth with controlled "
            "risk through diversified strategies. Maintains 60% stocks/40% "
            "bonds allocation, invests in both growth and value stocks, "
            "practices dollar-cost averaging, and holds investments for "
            "3-5 year time horizons. Willing to take calculated risks on "
            "established companies with strong fundamentals but avoids "
            "speculative investments. Rebalances portfolio quarterly and "
            "typically limits individual stock positions to 5% of total "
            "portfolio value."
        ),
        risk_tolerance=0.5,
        preferred_sectors=[Sector.INDUSTRIAL, Sector.FINANCE],
        investment_history=["SPACEX", "ANDURIL"],
    ),
]

# Generate historical trading data
trading_engine.generate_historical_trades(customers, stocks)


@app.get("/")
async def root():
    return {"message": "Private Stock Exchange API"}


@app.get("/stocks", response_model=List[Dict])
async def get_all_stocks():
    """Get all stocks with basic information"""
    stock_data = []
    for stock in stocks:
        stock_data.append(
            {
                "symbol": stock.symbol,
                "company_name": stock.company.name,
                "sector": stock.company.sector.value,
                "current_price": stock.current_price,
                "change_percent": stock.latest_price.change_percent,
                "volume": stock.latest_price.volume,
                "market_cap": stock.company.market_cap,
            }
        )
    return stock_data


@app.get("/stocks/{symbol}", response_model=Dict)
async def get_stock_details(symbol: str):
    """Get detailed information for a specific stock"""
    stock = next((s for s in stocks if s.symbol.upper() == symbol.upper()), None)
    if not stock:
        raise HTTPException(status_code=404, detail="Stock not found")

    return {
        "symbol": stock.symbol,
        "company": {
            "name": stock.company.name,
            "sector": stock.company.sector.value,
            "description": stock.company.description,
            "founded_year": stock.company.founded_year,
            "employee_count": stock.company.employee_count,
            "market_cap": stock.company.market_cap,
            "revenue": stock.company.revenue,
        },
        "current_price": stock.current_price,
        "latest_price": {
            "price": stock.latest_price.price,
            "change_percent": stock.latest_price.change_percent,
            "volume": stock.latest_price.volume,
            "open_price": stock.latest_price.open_price,
            "high_price": stock.latest_price.high_price,
            "low_price": stock.latest_price.low_price,
        },
        "recent_news": [
            {
                "headline": news.headline,
                "summary": news.summary,
                "sentiment": news.sentiment.value,
                "impact_score": news.impact_score,
                "timestamp": news.timestamp.isoformat(),
            }
            for news in stock.news[:5]  # Last 5 news items
        ],
        "products": [
            {
                "name": product.name,
                "description": product.description,
                "success_score": product.success_score,
                "launch_date": product.launch_date.isoformat(),
            }
            for product in stock.products
        ],
        "trends": [
            {
                "trend_type": trend.trend_type.value,
                "description": trend.description,
                "confidence": trend.confidence,
                "timestamp": trend.timestamp.isoformat(),
            }
            for trend in stock.trends[:5]  # Last 5 trends
        ],
    }


@app.get("/customers", response_model=List[Dict])
async def get_customers():
    """Get all customers"""
    return [
        {
            "id": customer.id,
            "name": customer.name,
            "risk_tolerance": customer.risk_tolerance,
            "preferred_sectors": [s.value for s in customer.preferred_sectors],
            "investment_history": customer.investment_history,
        }
        for customer in customers
    ]


@app.get("/rankings/{customer_id}", response_model=List[Dict])
async def get_personalized_rankings(customer_id: str, use_dodo: bool = False):
    """Get personalized stock rankings for a customer"""
    customer = next((c for c in customers if c.id == customer_id), None)
    if not customer:
        raise HTTPException(status_code=404, detail="Customer not found")

    rankings = ranking_engine.rank_stocks(stocks, customer, use_dodo, trading_engine)

    # Combine ranking with stock data
    ranked_stocks = []
    for ranking in rankings:
        stock = next((s for s in stocks if s.symbol == ranking.symbol), None)
        if stock:
            ranked_stocks.append(
                {
                    "rank_position": ranking.rank_position,
                    "rank_score": ranking.rank_score,
                    "reasoning": ranking.reasoning,
                    "symbol": stock.symbol,
                    "company_name": stock.company.name,
                    "sector": stock.company.sector.value,
                    "description": stock.company.description,
                    "current_price": stock.current_price,
                    "change_percent": stock.latest_price.change_percent,
                    "market_cap": stock.company.market_cap,
                    "last_month_orders": stock.last_month_orders,
                }
            )

    return ranked_stocks


@app.get("/stocks/{symbol}/prices")
async def get_stock_prices(symbol: str, days: int = 30):
    """Get historical price data for a stock"""
    stock = next((s for s in stocks if s.symbol.upper() == symbol.upper()), None)
    if not stock:
        raise HTTPException(status_code=404, detail="Stock not found")

    # Filter prices by requested days
    cutoff_date = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
    cutoff_date = cutoff_date.replace(day=cutoff_date.day - days)

    recent_prices = [
        {
            "timestamp": price.timestamp.isoformat(),
            "price": price.price,
            "volume": price.volume,
            "change_percent": price.change_percent,
        }
        for price in stock.prices
        if price.timestamp >= cutoff_date
    ]

    return {"symbol": stock.symbol, "prices": recent_prices}


@app.get("/portfolio/{customer_id}")
async def get_customer_portfolio(customer_id: str):
    """Get customer's current portfolio"""
    portfolio_summary = trading_engine.get_portfolio_summary(customer_id, stocks)
    return portfolio_summary


@app.get("/transactions/{customer_id}")
async def get_customer_transactions(customer_id: str):
    """Get customer's transaction history"""
    transactions = trading_engine.get_customer_transactions(customer_id)

    transaction_data = []
    for transaction in transactions:
        transaction_data.append(
            {
                "id": transaction.id,
                "symbol": transaction.symbol,
                "type": transaction.transaction_type.value,
                "quantity": transaction.quantity,
                "price": transaction.price,
                "total_value": transaction.total_value,
                "timestamp": transaction.timestamp.isoformat(),
                "status": transaction.status.value,
            }
        )

    return {"transactions": transaction_data}


@app.post("/trade")
async def execute_trade(trade_request: TradeRequest):
    """Execute a new trade"""
    try:
        # Extract data from request
        customer_id = trade_request.customer_id
        symbol = trade_request.symbol
        transaction_type = trade_request.transaction_type
        quantity = trade_request.quantity

        # Validate customer
        customer = next((c for c in customers if c.id == customer_id), None)
        if not customer:
            raise HTTPException(status_code=404, detail="Customer not found")

        # Validate stock
        stock = next((s for s in stocks if s.symbol.upper() == symbol.upper()), None)
        if not stock:
            raise HTTPException(status_code=404, detail="Stock not found")

        # Validate transaction type
        if transaction_type not in ["buy", "sell"]:
            raise HTTPException(status_code=400, detail="Invalid transaction type")

        # For sell orders, check if customer owns enough shares
        if transaction_type == "sell":
            portfolio = trading_engine.get_customer_portfolio(customer_id)
            current_holding = portfolio.holdings.get(symbol, 0)
            if current_holding < quantity:
                raise HTTPException(
                    status_code=400,
                    detail=f"Insufficient shares. You own {current_holding} shares of {symbol}, trying to sell {quantity}",
                )

        # Get current price
        current_price = stock.current_price

        # Execute trade
        trade_type = (
            TransactionType.BUY if transaction_type == "buy" else TransactionType.SELL
        )
        transaction = trading_engine.execute_trade(
            customer_id, symbol, trade_type, quantity, current_price
        )

        return {
            "success": True,
            "transaction": {
                "id": transaction.id,
                "symbol": transaction.symbol,
                "type": transaction.transaction_type.value,
                "quantity": transaction.quantity,
                "price": transaction.price,
                "total_value": transaction.total_value,
                "timestamp": transaction.timestamp.isoformat(),
            },
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# Serve static files and templates
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")


@app.get("/dashboard", response_class=HTMLResponse)
async def dashboard():
    """Serve the main dashboard HTML page"""
    return templates.TemplateResponse("dashboard.html", {"request": {}})


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
