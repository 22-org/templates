import random
from datetime import datetime, timedelta
from enum import Enum
from typing import Dict, List

from models import Customer, Stock

# Specific customer holdings configuration
CUSTOMER_HOLDINGS = {
    "customer1": [  # conservative
        {"symbol": "STRIPE", "quantity": 50, "avg_cost": 120.50},
        {"symbol": "CHIME", "quantity": 25, "avg_cost": 85.30},
        {"symbol": "PLAID", "quantity": 30, "avg_cost": 95.75},
        {"symbol": "BREX", "quantity": 20, "avg_cost": 65.25},
        {"symbol": "A16Z", "quantity": 15, "avg_cost": 180.00},
    ],
    "customer2": [  # aggressive
        {"symbol": "OPENAI", "quantity": 30, "avg_cost": 180.75},
        {"symbol": "XAI", "quantity": 20, "avg_cost": 95.25},
        {"symbol": "ANTHROPIC", "quantity": 25, "avg_cost": 145.50},
        {"symbol": "SCALEAI", "quantity": 35, "avg_cost": 125.00},
        {"symbol": "PROMETHEUS", "quantity": 15, "avg_cost": 220.75},
    ],
    "customer3": [  # balanced
        {"symbol": "SPACEX", "quantity": 40, "avg_cost": 150.00},
        {"symbol": "ANDURIL", "quantity": 35, "avg_cost": 75.50},
        {"symbol": "DATABRICKS", "quantity": 30, "avg_cost": 110.25},
        {"symbol": "RIPPLE", "quantity": 25, "avg_cost": 55.75},
        {"symbol": "LIGHTSPEED", "quantity": 20, "avg_cost": 90.00},
    ],
}


class TransactionType(str, Enum):
    BUY = "buy"
    SELL = "sell"


class TransactionStatus(str, Enum):
    PENDING = "pending"
    COMPLETED = "completed"
    CANCELLED = "cancelled"


class Transaction:
    def __init__(
        self,
        id: str,
        customer_id: str,
        symbol: str,
        transaction_type: TransactionType,
        quantity: int,
        price: float,
        timestamp: datetime,
        status: TransactionStatus = TransactionStatus.COMPLETED,
    ):
        self.id = id
        self.customer_id = customer_id
        self.symbol = symbol
        self.transaction_type = transaction_type
        self.quantity = quantity
        self.price = price
        self.timestamp = timestamp
        self.status = status
        self.total_value = quantity * price


class Portfolio:
    def __init__(self, customer_id: str, initial_cash: float = 50000.0):
        self.customer_id = customer_id
        self.cash = initial_cash
        self.holdings: Dict[str, int] = {}  # symbol -> quantity
        self.avg_cost_basis: Dict[str, float] = {}  # symbol -> avg price

    def add_shares(self, symbol: str, quantity: int, price: float):
        current_qty = self.holdings.get(symbol, 0)
        current_cost = self.avg_cost_basis.get(symbol, 0)

        new_qty = current_qty + quantity
        # Avoid division by zero and format for line length
        total_cost = (current_cost * current_qty) + (price * quantity)
        new_avg_cost = total_cost / new_qty if new_qty > 0 else 0

        self.holdings[symbol] = new_qty
        self.avg_cost_basis[symbol] = new_avg_cost

        # Deduct cash for purchase
        cost = quantity * price
        self.cash -= cost

    def remove_shares(self, symbol: str, quantity: int, price: float):
        if symbol in self.holdings:
            self.holdings[symbol] -= quantity
            if self.holdings[symbol] <= 0:
                del self.holdings[symbol]
                if symbol in self.avg_cost_basis:
                    del self.avg_cost_basis[symbol]

            # Add cash from sale
            proceeds = quantity * price
            self.cash += proceeds

    def get_total_value(self, current_prices: Dict[str, float]) -> float:
        total = self.cash  # Start with cash
        for symbol, quantity in self.holdings.items():
            if symbol in current_prices:
                total += quantity * current_prices[symbol]
        return total

    def get_total_cost(self) -> float:
        total = 0.0
        for symbol, quantity in self.holdings.items():
            if symbol in self.avg_cost_basis:
                total += quantity * self.avg_cost_basis[symbol]
        return total

    def get_unrealized_pnl(self, current_prices: Dict[str, float]) -> float:
        return self.get_total_value(current_prices) - self.get_total_cost()


class TradingEngine:
    def __init__(self):
        self.transactions: List[Transaction] = []
        self.portfolios: Dict[str, Portfolio] = {}
        self.transaction_counter = 0

    def generate_historical_trades(self, custs: List[Customer], stks: List[Stock]):
        """Generate fake historical trading data from specific holdings"""
        for customer in custs:
            portfolio = Portfolio(customer.id)
            self.portfolios[customer.id] = portfolio

            # Get specific holdings for this customer
            customer_holdings = CUSTOMER_HOLDINGS.get(customer.id, [])

            for holding in customer_holdings:
                symbol = holding["symbol"]
                quantity = holding["quantity"]
                avg_cost = holding["avg_cost"]

                # Find the stock in available stocks
                stock = next(
                    (s for s in stks if s.symbol.upper() == symbol.upper()), None
                )
                if not stock:
                    continue

                # Create historical transaction (buy from 30-90 days ago)
                days_ago = random.randint(30, 90)
                ts = datetime.now() - timedelta(days=days_ago)

                transaction = Transaction(
                    id=f"txn_{customer.id}_{self.transaction_counter}",
                    customer_id=customer.id,
                    symbol=symbol,
                    transaction_type=TransactionType.BUY,
                    quantity=quantity,
                    price=avg_cost,
                    timestamp=ts,
                )
                self.transactions.append(transaction)
                self.transaction_counter += 1

                # Add shares to portfolio using configured avg cost
                portfolio.holdings[symbol] = quantity
                portfolio.avg_cost_basis[symbol] = avg_cost
                portfolio.cash -= quantity * avg_cost

        # Sort transactions by timestamp
        self.transactions.sort(key=lambda x: x.timestamp)

    def _get_historical_price(self, stock: Stock, target_date: datetime) -> float:
        """Get stock price for a specific historical date"""
        # Find the closest price to the target date
        closest_price = None
        min_diff = float("inf")

        for price in stock.prices:
            diff = abs((price.timestamp - target_date).days)
            if diff < min_diff:
                min_diff = diff
                closest_price = price

        return closest_price.price if closest_price else stock.current_price

    def get_customer_transactions(self, customer_id: str) -> List[Transaction]:
        """Get all transactions for a customer"""
        return [t for t in self.transactions if t.customer_id == customer_id]

    def get_customer_portfolio(self, c_id: str) -> Portfolio:
        """Get customer's current portfolio"""
        return self.portfolios.get(c_id, Portfolio(c_id))

    def execute_trade(
        self,
        c_id: str,
        symbol: str,
        t_type: TransactionType,
        qty: int,
        p: float,
    ) -> Transaction:
        """Execute a new trade"""
        ts = datetime.now()
        transaction = Transaction(
            id=f"txn_{c_id}_{self.transaction_counter}",
            customer_id=c_id,
            symbol=symbol,
            transaction_type=t_type,
            quantity=qty,
            price=p,
            timestamp=ts,
        )
        self.transactions.append(transaction)
        self.transaction_counter += 1

        # Update portfolio
        portfolio = self.portfolios.get(c_id)
        if portfolio:
            if t_type == TransactionType.BUY:
                is_new = symbol not in portfolio.holdings
                if is_new and len(portfolio.holdings) >= 5:
                    raise ValueError("Portfolio limit reached (5 stocks)")
                portfolio.add_shares(symbol, qty, p)
            else:
                portfolio.remove_shares(symbol, qty, p)
        return transaction

    def get_portfolio_summary(self, c_id: str, stks: List[Stock]) -> Dict:
        """Get detailed portfolio summary"""
        portfolio = self.get_customer_portfolio(c_id)
        cur_prices = {s.symbol: s.current_price for s in stks}

        holdings = []
        for symbol, quantity in portfolio.holdings.items():
            avg_cost = portfolio.avg_cost_basis.get(symbol, 0)
            cur_price = cur_prices.get(symbol, 0)
            mkt_val = quantity * cur_price
            cost_basis = quantity * avg_cost
            pnl = mkt_val - cost_basis
            pnl_pct = ((cur_price - avg_cost) / avg_cost * 100) if avg_cost > 0 else 0

            holdings.append(
                {
                    "symbol": symbol,
                    "quantity": quantity,
                    "avg_cost": round(avg_cost, 2),
                    "current_price": round(cur_price, 2),
                    "market_value": round(mkt_val, 2),
                    "cost_basis": round(cost_basis, 2),
                    "unrealized_pnl": round(pnl, 2),
                    "unrealized_pnl_percent": round(pnl_pct, 2),
                }
            )

        total_mkt_val = portfolio.get_total_value(cur_prices)
        total_cost = portfolio.get_total_cost()
        total_pnl = total_mkt_val - total_cost - portfolio.cash

        return {
            "holdings": holdings,
            "cash": round(portfolio.cash, 2),
            "total_market_value": round(total_mkt_val, 2),
            "total_cost": round(total_cost, 2),
            "total_unrealized_pnl": round(total_pnl, 2),
            "total_unrealized_pnl_percent": round(
                (total_pnl / total_cost * 100) if total_cost > 0 else 0, 2
            ),
        }
