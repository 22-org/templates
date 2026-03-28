"""
Load stock data from finance data generator to entities service
"""

import os
from typing import List

import requests
from constants import DODO_API_URL
from data_generator import DataGenerator
from dotenv import load_dotenv
from models import Stock

load_dotenv(dotenv_path=".env")


def stock_to_context(stock: Stock) -> str:
    """Convert stock object to context string for entities service"""
    c = stock.company
    parts = [
        f"Symbol: {stock.symbol}",
        f"Company: {c.name}",
        f"Sector: {c.sector.value}",
        f"Description: {c.description}",
        f"Price: ${stock.current_price:.2f}",
        f"Market Cap: ${c.market_cap}B",
        f"Revenue: ${c.revenue}B",
        f"Employees: {c.employee_count}",
        f"Founded: {c.founded_year}",
        f"Orders: {stock.last_month_orders}",
    ]

    return " | ".join(parts)


def ingest_stocks_to_entities(
    api_key: str,
    stocks: List[Stock],
    primary_key: str = "symbol",
):
    """Ingest stock data to entities service using direct input"""

    headers = {
        "Authorization": f"Bearer {api_key}",
    }

    # Convert stocks to direct input format
    stock_data = {}
    for stock in stocks:
        stock_data[stock.symbol] = stock_to_context(stock)

    try:
        print(f"Ingesting {len(stock_data)} stocks to entities service...")
        print("URL:", DODO_API_URL)

        response = requests.post(
            url=f"{DODO_API_URL}/api/entities/ingest",
            params={
                "source": "input",
                "primary_key": primary_key,
                "model_key": "prag_v1",
            },
            data={
                "direct_input": str(stock_data),
            },
            headers=headers,
        )
        response.raise_for_status()

        print("Stock ingestion successful!")
        print("Response:", response.json())

        return response.json()

    except Exception as e:
        print(f"Stock ingestion failed: {e}")
        if hasattr(e, "response") and e.response is not None:
            print(f"Response status: {e.response.status_code}")
            print(f"Response content: {e.response.text}")
        return None


if __name__ == "__main__":
    # Configuration
    email = os.getenv("EMAIL", "dat.ngo3246@gmail.com")
    password = os.getenv("PASSWORD", "password")
    api_key = os.getenv("API_KEY", "du_live_VvoFj-OAKx-J8-_U6sqVnIEt5s6pXUvn")
    primary_key = "symbol"

    print("=== Stock Data to Entities Loader ===")
    print(f"Using email: {email}")
    print(f"Primary key: {primary_key}")
    print()

    # Generate stock data
    print("Generating stock data...")
    data_generator = DataGenerator()
    stocks = data_generator.generate_stocks()

    print(f"Generated {len(stocks)} stocks:")
    for stock in stocks[:5]:  # Show first 5
        print(f"  - {stock.symbol}: {stock.company.name}")
    if len(stocks) > 5:
        print(f"  ... and {len(stocks) - 5} more")
    print()

    # Ingest stocks to entities
    print("\n" + "=" * 50 + "\n")
    ingest_stocks_to_entities(
        api_key=api_key,
        stocks=stocks,
        primary_key=primary_key,
    )
