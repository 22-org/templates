import os
from datetime import datetime, timedelta
from typing import List

import requests
from constants import DODO_API_URL
from dotenv import load_dotenv
from models import Customer, PersonalizedRank, Sector, Stock, TrendType

load_dotenv(".env")


class RankingEngine:
    def __init__(self):
        self.sector_weights = {
            Sector.TECHNOLOGY: 1.2,
            Sector.HEALTHCARE: 1.1,
            Sector.FINANCE: 1.0,
            Sector.ENERGY: 0.9,
            Sector.CONSUMER: 1.0,
            Sector.INDUSTRIAL: 0.8,
            Sector.REAL_ESTATE: 0.7,
            Sector.UTILITIES: 0.6,
        }

    def calculate_momentum_score(self, stock: Stock) -> float:
        """Calculate price momentum based on recent price changes"""
        if len(stock.prices) < 7:
            return 0.5

        recent_prices = stock.prices[-7:]
        price_changes = [p.change_percent for p in recent_prices]
        avg_change = sum(price_changes) / len(price_changes)

        # Normalize to 0-1 range
        momentum_score = max(0, min(1, (avg_change + 5) / 10))
        return momentum_score

    def calculate_news_sentiment_score(self, stock: Stock) -> float:
        """Calculate sentiment score based on recent news"""
        if not stock.news:
            return 0.5

        # Get news from last 7 days
        cutoff_date = datetime.now() - timedelta(days=7)
        recent_news = [n for n in stock.news if n.timestamp > cutoff_date]

        if not recent_news:
            return 0.5

        sentiment_scores = []
        for news_item in recent_news:
            if news_item.sentiment == TrendType.POSITIVE:
                score = 0.7 + (news_item.impact_score * 0.3)
            elif news_item.sentiment == TrendType.NEGATIVE:
                score = 0.3 - (news_item.impact_score * 0.2)
            else:
                score = 0.5 + (news_item.impact_score * 0.1)
            sentiment_scores.append(score)

        return sum(sentiment_scores) / len(sentiment_scores)

    def calculate_trend_score(self, stock: Stock) -> float:
        """Calculate trend score based on recent trends"""
        if not stock.trends:
            return 0.5

        # Get trends from last 7 days
        cutoff_date = datetime.now() - timedelta(days=7)
        recent_trends = [t for t in stock.trends if t.timestamp > cutoff_date]

        if not recent_trends:
            return 0.5

        trend_scores = []
        for trend in recent_trends:
            if trend.trend_type == TrendType.POSITIVE:
                score = 0.6 + (trend.confidence * 0.4)
            elif trend.trend_type == TrendType.NEGATIVE:
                score = 0.4 - (trend.confidence * 0.3)
            else:
                score = 0.5
            trend_scores.append(score)

        return sum(trend_scores) / len(trend_scores)

    def calculate_order_score(self, stock: Stock) -> float:
        """Calculate score based on number of orders (primary ranking factor)"""  # noqa
        # Normalize order count to a 0-1 score
        # Assuming max orders in our data is around 10000 for normalization
        max_orders = 10000.0
        return min(1.0, stock.last_month_orders / max_orders)

    def calculate_smart_ranking_placeholder(
        self, stock: Stock, customer: Customer
    ) -> float:
        """
        PLACEHOLDER: Future AI/Smart ranking API hook.
        This will be replaced with a real recommendation engine API call.
        """
        # Currently returns a neutral score so it doesn't affect order ranking
        return 0.5

    def rank_stocks(
        self,
        stocks: List[Stock],
        customer: Customer,
        use_dodo: bool = False,
        trading_engine=None,
    ) -> List[PersonalizedRank]:
        """Generate rankings based on order count with placeholders for smart ranking"""  # noqa
        rankings = []
        if use_dodo:
            # Get customer info
            # Remove id from customer info
            customer_info = customer.model_dump()
            customer_info.pop("id", None)

            # Get API endpoint from environment variable
            api_endpoint = f"{DODO_API_URL}/api/recommend/recommend"
            try:
                # Prepare catalog from stocks
                catalog = {}
                for stock in stocks:
                    catalog[stock.symbol] = {
                        "company name": stock.company.name,
                        "sector": stock.company.sector.value,
                        "price": stock.current_price,
                        "description": stock.company.description,
                    }

                # Prepare context with customer's current portfolio
                context = {
                    "previous_purchases": [],
                    "budget": 100000.0,  # Default budget
                }

                # Add current portfolio holdings if trading engine is available
                if trading_engine:
                    try:
                        portfolio = trading_engine.get_customer_portfolio(
                            customer.id
                        )  # noqa
                        for symbol, quantity in portfolio.holdings.items():
                            stock = next(
                                (s for s in stocks if s.symbol == symbol), None
                            )
                            if stock:
                                context["previous_purchases"].append(
                                    {
                                        "product_name": stock.company.name,
                                        "price": stock.current_price,
                                        "category": stock.company.sector.value,
                                        "quantity": quantity,
                                        "market_value": quantity
                                        * stock.current_price,  # noqa
                                    }
                                )
                    except Exception as e:
                        print(f"Error getting portfolio: {e}")
                        # Fallback to investment history if portfolio fails
                        for symbol in customer.investment_history:
                            stock = next(
                                (s for s in stocks if s.symbol == symbol), None
                            )
                            if stock:
                                context["previous_purchases"].append(
                                    {
                                        "product_name": stock.company.name,
                                        "price": stock.current_price,
                                        "category": stock.company.sector.value,
                                    }
                                )
                else:
                    # Fallback to investment history if no trading engine
                    for symbol in customer.investment_history:  # noqa
                        stock = next(
                            (s for s in stocks if s.symbol == symbol),
                            None,
                        )
                        if stock:
                            context["previous_purchases"].append(
                                {
                                    "product_name": stock.company.name,
                                    "price": stock.current_price,
                                    "category": stock.company.sector.value,
                                }
                            )

                # Make API request
                API_KEY = os.getenv("API_KEY")
                response = requests.post(  # noqa
                    f"{api_endpoint}?model_key=prag_v1&num_results=10&customer_id={customer.id}",  # noqa
                    headers={
                        "Authorization": f"Bearer {API_KEY}",
                        "Content-Type": "application/json",
                    },
                    json={
                        "context": context,
                        # "catalog": catalog,
                        "template": f"Recommend stocks for customer with risk tolerance {customer.description}, interest in {', '.join([s.value for s in customer.preferred_sectors])}, and current portfolio holdings {{previous_purchases}}",  # noqa
                    },
                )

                if response.status_code == 200:
                    api_result = response.json()
                    print(
                        f"API Response: {api_result}"
                    )  # already sorted by score. First element is the best

                    # Process API results and return rankings
                    if api_result and "results" in api_result:
                        print(
                            f"Found {len(api_result['results'])} recommendations"  # noqa
                        )
                        # Convert API recommendations to PersonalizedRank objects  # noqa
                        for i, rec in enumerate(api_result["results"]):
                            rankings.append(
                                PersonalizedRank(
                                    symbol=rec,
                                    rank_score=i,
                                    rank_position=i
                                    + 1,  # Will be assigned after sorting
                                    reasoning=f"Dodo AI recommendation: {rec}",
                                )
                            )

                        print(
                            f"Returning {len(rankings), rankings} Dodo rankings"  # noqa
                        )
                        return rankings  # Return Dodo rankings directly
                    else:
                        print(
                            "No recommendations found in response, falling back"  # noqa
                        )
                        # Invalid response format, fall back to current ranking
                        pass
                else:
                    # API call failed, fall back to current ranking
                    pass

            except Exception as e:
                # Error occurred, fall back to current ranking
                print(f"Error calling Dodo API: {e}")
                pass
        else:

            # Current ranking logic (will be used if use_dodo is False or dodo API fails)  # noqa
            for stock in stocks:
                # Primary ranking by number of orders
                order_score = self.calculate_order_score(stock)

                # Placeholder for future smart ranking  # noqa
                # smart_score = self.calculate_smart_ranking_placeholder(stock, customer)# noqa

                # For now, we only use order_score for actual ranking
                # but we keep smart_score logic ready for integration
                final_score = order_score

                reasoning = f"Ranked by popularity: {stock.last_month_orders} orders in the last month."  # noqa

                rankings.append(
                    PersonalizedRank(
                        symbol=stock.symbol,
                        rank_score=round(final_score, 3),
                        rank_position=0,
                        reasoning=reasoning,
                    )
                )

            # Sort by score (orders) and assign positions
            rankings.sort(key=lambda x: x.rank_score, reverse=True)
            for i, ranking in enumerate(rankings):
                ranking.rank_position = i + 1

        return rankings
