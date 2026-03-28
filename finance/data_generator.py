import random
from datetime import datetime, timedelta
from typing import List

import numpy as np
import pandas as pd
from models import (
    Company,
    NewsItem,
    Product,
    Sector,
    Stock,
    StockPrice,
    Trend,
    TrendType,
)


class DataGenerator:
    def __init__(self):
        self.companies = [
            {
                "id": "openai",
                "name": "OpenAI",
                "sector": Sector.TECHNOLOGY,
                "description": "Leading artificial intelligence research company developing advanced AI models and technologies",
                "founded_year": 2015,
                "employee_count": 1500,
                "market_cap": 80.0,
                "revenue": 4.0,
                "financial_fundamentals": {
                    "pe_ratio": 35.2,
                    "debt_to_equity": 0.15,
                    "roe": 18.5,
                    "revenue_growth_5y": "45%",
                },
                "analyst_ratings": {
                    "morningstar": 4.5,
                    "yahoo_finance": 4.2,
                    "zacks": "Strong Buy",
                },
                "pros": [
                    "Strong AI technology portfolio",
                    "Partnership with Microsoft",
                    "Leading research capabilities",
                ],
                "cons": [
                    "High valuation concerns",
                    "Regulatory scrutiny",
                    "Intense competition",
                ],
            },
            {
                "id": "spacex",
                "name": "SpaceX",
                "sector": Sector.INDUSTRIAL,
                "description": "Aerospace manufacturer and space transportation company revolutionizing space travel",
                "founded_year": 2002,
                "employee_count": 12000,
                "market_cap": 150.0,
                "revenue": 8.0,
                "financial_fundamentals": {
                    "pe_ratio": 45.8,
                    "debt_to_equity": 0.25,
                    "roe": 12.3,
                    "revenue_growth_5y": "35%",
                },
                "analyst_ratings": {
                    "morningstar": 4.2,
                    "yahoo_finance": 4.0,
                    "zacks": "Buy",
                },
                "pros": [
                    "Market leader in space transportation",
                    "Government contracts with NASA",
                    "Innovative Starship technology",
                ],
                "cons": [
                    "High operating costs",
                    "Technical challenges with Starship",
                    "Dependence on government contracts",
                ],
            },
            {
                "id": "anthropic",
                "name": "Anthropic",
                "sector": Sector.TECHNOLOGY,
                "description": "AI safety and research company focused on developing reliable AI systems",
                "founded_year": 2021,
                "employee_count": 500,
                "market_cap": 40.0,
                "revenue": 1.0,
            },
            {
                "id": "stripe",
                "name": "Stripe",
                "sector": Sector.FINANCE,
                "description": "Financial technology company building economic infrastructure for the internet",
                "founded_year": 2010,
                "employee_count": 7000,
                "market_cap": 95.0,
                "revenue": 14.0,
            },
            {
                "id": "databricks",
                "name": "Databricks",
                "sector": Sector.TECHNOLOGY,
                "description": "Data and AI platform helping organizations solve their biggest data challenges",
                "founded_year": 2013,
                "employee_count": 5000,
                "market_cap": 38.0,
                "revenue": 1.6,
            },
            {
                "id": "discord",
                "name": "Discord",
                "sector": Sector.TECHNOLOGY,
                "description": "Communication platform bringing people together through voice, video, and text",
                "founded_year": 2015,
                "employee_count": 800,
                "market_cap": 15.0,
                "revenue": 1.3,
            },
            {
                "id": "ripple",
                "name": "Ripple Labs",
                "sector": Sector.FINANCE,
                "description": "Blockchain technology company enabling global financial transactions",
                "founded_year": 2012,
                "employee_count": 800,
                "market_cap": 25.0,
                "revenue": 0.8,
            },
            {
                "id": "epic",
                "name": "Epic Games",
                "sector": Sector.CONSUMER,
                "description": "Interactive entertainment company and creator of Unreal Engine and Fortnite",
                "founded_year": 1991,
                "employee_count": 4000,
                "market_cap": 28.5,
                "revenue": 5.8,
            },
            {
                "id": "chime",
                "name": "Chime",
                "sector": Sector.FINANCE,
                "description": "Financial technology company providing mobile banking services",
                "founded_year": 2013,
                "employee_count": 1200,
                "market_cap": 25.0,
                "revenue": 2.0,
            },
            {
                "id": "instacart",
                "name": "Instacart",
                "sector": Sector.CONSUMER,
                "description": "Grocery delivery and pickup service bringing fresh food to customers",
                "founded_year": 2012,
                "employee_count": 3000,
                "market_cap": 10.0,
                "revenue": 2.5,
            },
            {
                "id": "plaid",
                "name": "Plaid",
                "sector": Sector.FINANCE,
                "description": "Financial technology platform enabling applications to connect with bank accounts",
                "founded_year": 2013,
                "employee_count": 800,
                "market_cap": 13.4,
                "revenue": 0.6,
            },
            {
                "id": "isomorphic",
                "name": "Isomorphic Labs",
                "sector": Sector.HEALTHCARE,
                "description": "AI-driven drug discovery company using AlphaFold technology to revolutionize medicine",
                "founded_year": 2021,
                "employee_count": 200,
                "market_cap": 3.0,
                "revenue": 0.1,
            },
            {
                "id": "anduril",
                "name": "Anduril Industries",
                "sector": Sector.INDUSTRIAL,
                "description": "Defense technology company building autonomous systems and software for national security",
                "founded_year": 2017,
                "employee_count": 2500,
                "market_cap": 14.0,
                "revenue": 0.5,
            },
            {
                "id": "neuralink",
                "name": "Neuralink",
                "sector": Sector.HEALTHCARE,
                "description": "Neurotechnology company developing implantable brain–computer interfaces",
                "founded_year": 2016,
                "employee_count": 400,
                "market_cap": 5.0,
                "revenue": 0.0,
            },
            {
                "id": "figma",
                "name": "Figma",
                "sector": Sector.TECHNOLOGY,
                "description": "Collaborative interface design tool building the future of design and development",
                "founded_year": 2012,
                "employee_count": 1300,
                "market_cap": 12.5,
                "revenue": 0.6,
            },
            {
                "id": "brex",
                "name": "Brex",
                "sector": Sector.FINANCE,
                "description": "Financial technology company providing corporate cards and spend management",
                "founded_year": 2017,
                "employee_count": 1000,
                "market_cap": 12.3,
                "revenue": 0.4,
            },
            {
                "id": "ami",
                "name": "AMI Labs",
                "sector": Sector.TECHNOLOGY,
                "description": (
                    "Advanced Machine Intelligence company founded by Yann LeCun to build "
                    "world models that understand the physical world. Departing from Meta's "
                    "LLM focus, AMI develops AI systems that create intuitive "
                    "understanding of environments through embodied intelligence. The company "
                    "aims to build universal world models for general intelligence, "
                    "prioritizing open source technology and democratic access to AI."
                ),
                "founded_year": 2025,
                "employee_count": 50,
                "market_cap": 10.3,
                "revenue": 0.0,
            },
            {
                "id": "quince",
                "name": "Quince",
                "sector": Sector.TECHNOLOGY,
                "description": (
                    "AI-powered design platform enabling creators to generate, refine, and "
                    "enhance visual content through advanced AI models. Serves over 20 "
                    "million users globally with tools for image generation, video enhancement, "
                    "and creative workflows. Recently raised $500M Series E at $10B "
                    "valuation, becoming one of the fastest-growing creative AI platforms."
                ),
                "founded_year": 2022,
                "employee_count": 146,
                "market_cap": 10.0,
                "revenue": 0.3,
            },
            {
                "id": "lovable",
                "name": "Lovable",
                "sector": Sector.TECHNOLOGY,
                "description": (
                    "AI development platform that enables rapid application building "
                    "through natural language interfaces. Reported adding $100M in revenue "
                    "in a single month with just 146 employees, demonstrating "
                    "exceptional capital efficiency. Platform helps developers create "
                    "and deploy software applications using AI-powered code generation."
                ),
                "founded_year": 2023,
                "employee_count": 146,
                "market_cap": 8.5,
                "revenue": 0.8,
            },
            {
                "id": "scaleai",
                "name": "Scale AI",
                "sector": Sector.TECHNOLOGY,
                "description": (
                    "Provider of training data and model evaluation for AI applications. "
                    "Raised $14.3B from Meta at $29B valuation. Founder "
                    "Alexander Wang joined Meta to work on AI efforts while maintaining "
                    "Scale's independence. Critical infrastructure for LLM training."
                ),
                "founded_year": 2016,
                "employee_count": 400,
                "market_cap": 29.0,
                "revenue": 1.2,
            },
            {
                "id": "prometheus",
                "name": "Project Prometheus",
                "sector": Sector.TECHNOLOGY,
                "description": (
                    "AI startup focused on applying AI technology to physical tasks. "
                    "Launched with $6.2B in initial funding, reportedly co-led "
                    "by Jeff Bezos and Vik Bajaj. Aims to bridge the gap "
                    "between digital AI and real-world physical applications."
                ),
                "founded_year": 2024,
                "employee_count": 75,
                "market_cap": 62.0,
                "revenue": 0.0,
            },
            {
                "id": "xai",
                "name": "xAI",
                "sector": Sector.TECHNOLOGY,
                "description": (
                    "Elon Musk's generative AI startup focused on understanding the "
                    "true nature of the universe. Raised $5.3B in funding and "
                    "has raised over $22B total in equity and debt financing. "
                    "Competing directly with OpenAI in the LLM space."
                ),
                "founded_year": 2023,
                "employee_count": 200,
                "market_cap": 50.0,
                "revenue": 0.5,
            },
            {
                "id": "prometheus",
                "name": "Project Prometheus",
                "sector": Sector.TECHNOLOGY,
                "description": (
                    "AI startup focused on applying AI technology to physical tasks. "
                    "Launched with $6.2B in initial funding, reportedly co-led "
                    "by Jeff Bezos and Vik Bajaj. Aims to bridge the gap "
                    "between digital AI and real-world physical applications."
                ),
                "founded_year": 2024,
                "employee_count": 75,
                "market_cap": 62.0,
                "revenue": 0.0,
            },
            {
                "id": "anduril",
                "name": "Anduril Industries",
                "sector": Sector.INDUSTRIAL,
                "description": (
                    "Defense technology startup specializing in autonomous systems and "
                    "counter-drone technology. Raised $2.5B Series G led by "
                    "Founders Fund, doubling valuation to $30.5B. Critical for "
                    "national defense and autonomous systems development."
                ),
                "founded_year": 2017,
                "employee_count": 500,
                "market_cap": 30.5,
                "revenue": 1.8,
            },
            {
                "id": "caddi",
                "name": "CADDi",
                "sector": Sector.HEALTHCARE,
                "description": (
                    "Tokyo-based AI-powered supply chain optimization platform. "
                    "Secured funding from Atomico to expand globally. Focuses on "
                    "life sciences AI applications and supply chain automation."
                ),
                "founded_year": 2020,
                "employee_count": 120,
                "market_cap": 4.2,
                "revenue": 0.15,
            },
            {
                "id": "coreweave",
                "name": "CoreWeave",
                "sector": Sector.TECHNOLOGY,
                "description": (
                    "AI agent infrastructure platform enabling autonomous AI workflows. "
                    "Provides specialized inboxes and tools for AI agent management. "
                    "Part of the emerging AI agent ecosystem with Meta acquisition."
                ),
                "founded_year": 2023,
                "employee_count": 25,
                "market_cap": 3.5,
                "revenue": 0.08,
            },
            {
                "id": "replit",
                "name": "Replit",
                "sector": Sector.TECHNOLOGY,
                "description": (
                    "Cloud-based development environment and coding platform. Snags $9B "
                    "valuation 6 months after hitting $3B valuation. Enables "
                    "collaborative coding and rapid application deployment."
                ),
                "founded_year": 2016,
                "employee_count": 300,
                "market_cap": 9.0,
                "revenue": 0.6,
            },
            {
                "id": "character",
                "name": "Character.AI",
                "sector": Sector.CONSUMER,
                "description": (
                    "AI chatbot platform allowing users to create and interact with "
                    "AI characters. Viral success among younger demographics. "
                    "Focuses on conversational AI and entertainment applications."
                ),
                "founded_year": 2021,
                "employee_count": 80,
                "market_cap": 5.0,
                "revenue": 0.25,
            },
            {
                "id": "midjourney",
                "name": "Midjourney",
                "sector": Sector.CONSUMER,
                "description": (
                    "Generative AI art platform specializing in image creation from "
                    "text prompts. Leader in AI-powered visual content creation "
                    "with strong community of artists and creators."
                ),
                "founded_year": 2021,
                "employee_count": 60,
                "market_cap": 7.5,
                "revenue": 0.4,
            },
            {
                "id": "runway",
                "name": "RunwayML",
                "sector": Sector.TECHNOLOGY,
                "description": (
                    "AI-powered video editing and generation platform. Enables creators "
                    "to produce professional video content using AI tools. Strong "
                    "adoption in content creation and marketing workflows."
                ),
                "founded_year": 2018,
                "employee_count": 200,
                "market_cap": 6.8,
                "revenue": 0.35,
            },
            {
                "id": "a16z",
                "name": "Andreessen Horowitz",
                "sector": Sector.FINANCE,
                "description": (
                    "Premier venture capital firm investing in technology startups. "
                    "Notable investments include AI, crypto, and consumer tech. "
                    "Manages billions in capital across multiple funds."
                ),
                "founded_year": 2009,
                "employee_count": 150,
                "market_cap": 45.0,
                "revenue": 2.1,
            },
            {
                "id": "lightspeed",
                "name": "Lightspeed Venture Partners",
                "sector": Sector.FINANCE,
                "description": (
                    "Global venture capital firm investing in technology and consumer "
                    "companies. Co-led Anthropic's $13B round. Focus on "
                    "early-stage startups with high growth potential."
                ),
                "founded_year": 2012,
                "employee_count": 80,
                "market_cap": 28.0,
                "revenue": 1.5,
            },
            {
                "id": "iconiq",
                "name": "Iconiq Growth",
                "sector": Sector.FINANCE,
                "description": (
                    "Growth equity firm managing over $100B in assets. Co-led "
                    "Quince's $500M Series E at $10B valuation. Focuses on "
                    "late-stage technology companies with proven business models."
                ),
                "founded_year": 2015,
                "employee_count": 40,
                "market_cap": 15.0,
                "revenue": 0.8,
            },
        ]

        self.news_templates = {
            TrendType.POSITIVE: [
                "{company} reports record quarterly earnings",
                "{company} announces breakthrough product launch",
                "{company} secures major partnership deal",
                "{company} receives regulatory approval for new product",
                "{company} expands into international markets",
            ],
            TrendType.NEGATIVE: [
                "{company} faces regulatory investigation",
                "{company} reports lower than expected earnings",
                "{company} experiences production delays",
                "{company} loses key executive",
                "{company} faces increased competition",
            ],
            TrendType.NEUTRAL: [
                "{company} announces organizational restructuring",
                "{company} completes routine share buyback",
                "{company} updates investor guidance",
                "{company} announces board changes",
                "{company} maintains current market position",
            ],
        }

        self.product_names = {
            Sector.HEALTHCARE: [
                "AlphaFold Drug Discovery",
                "IsoMorphic Platform",
                "Neuralink N1 Implant",
                "Telepathy Interface",
                "Biotech Research Suite",
            ],
            Sector.TECHNOLOGY: [
                "Mistral Large",
                "Mistral Medium",
                "Figma Design",
                "FigJam",
                "GPT-5 Model",
                "ChatGPT Enterprise",
                "DALL-E 4",
                "AI Platform",
                "Unreal Engine 6",
                "Fortnite",
                "Epic Games Store",
                "Discord Nitro",
                "Claude 4",
                "Anthropic AI Safety",
                "Data Intelligence Platform",
                "MLflow",
                "AMI World Model",
                "Quince Creator Tools",
                "Lovable Dev Platform",
                "Constitutional AI Framework",
                "Scale Data Engine",
                "Prometheus Interface",
                "Grok Truth System",
                "Databricks Runtime",
                "CoreWeave Agent Inbox",
                "Replit Codespace",
                "WordPress Workspace",
                "Character Creator Studio",
                "Midjourney Art Generator",
                "Runway Video Editor",
            ],
            Sector.FINANCE: [
                "Stripe Connect",
                "Stripe Atlas",
                "Stripe Terminal",
                "Stripe Radar",
                "RippleNet",
                "XRP Ledger",
                "Chime Credit Builder",
                "Chime Spend Account",
                "Plaid Exchange",
                "Plaid Auth",
                "Brex Corporate Card",
                "Brex Treasury",
                "A16Z Fund I",
                "Lightspeed Venture Fund",
                "Iconiq Growth Fund",
            ],
            Sector.CONSUMER: [
                "Instacart+",
                "Instacart Business",
                "Fortnite Mobile",
                "Epic Games Publishing",
                "Discord Server Boosting",
                "Discord Voice Channels",
                "Character.AI Subscriptions",
                "Midjourney Pro",
                "Runway Unlimited",
            ],
            Sector.INDUSTRIAL: [
                "Lattice OS",
                "Anduril Sentry",
                "Dive-LD",
                "Starship Rocket",
                "Falcon 9",
                "Starlink Internet",
                "Dragon Spacecraft",
                "SpaceX Starbase",
                "Mars Colony Technology",
            ],
        }

    def generate_stock_prices(self, symbol: str, days: int = 30) -> List[StockPrice]:
        prices = []
        base_price = random.uniform(10, 200)
        current_price = base_price

        for i in range(days):
            timestamp = datetime.now() - timedelta(days=days - i)

            # Generate realistic price movements
            daily_change = np.random.normal(0, 0.02)  # 2% daily volatility
            current_price *= 1 + daily_change

            # Generate intraday prices
            open_price = current_price * random.uniform(0.98, 1.02)
            high_price = current_price * random.uniform(1.0, 1.05)
            low_price = current_price * random.uniform(0.95, 1.0)
            volume = random.randint(10000, 1000000)

            change_percent = ((current_price - open_price) / open_price) * 100

            prices.append(
                StockPrice(
                    symbol=symbol,
                    timestamp=timestamp,
                    price=round(current_price, 2),
                    volume=volume,
                    open_price=round(open_price, 2),
                    high_price=round(high_price, 2),
                    low_price=round(low_price, 2),
                    change_percent=round(change_percent, 2),
                )
            )

        return prices

    def generate_news(
        self, symbol: str, company_name: str, days: int = 30
    ) -> List[NewsItem]:
        news_items = []
        news_per_day = random.randint(1, 3)

        for i in range(days):
            for j in range(random.randint(0, news_per_day)):
                timestamp = datetime.now() - timedelta(
                    days=days - i, hours=random.randint(0, 23)
                )
                trend_type = random.choice(list(TrendType))

                headline = random.choice(self.news_templates[trend_type]).format(
                    company=company_name
                )

                # Generate summary based on trend type
                if trend_type == TrendType.POSITIVE:
                    summary = f"Strong performance indicators suggest positive outlook for {company_name}"
                    impact_score = random.uniform(0.7, 1.0)
                elif trend_type == TrendType.NEGATIVE:
                    summary = (
                        f"Challenges ahead may impact {company_name}'s market position"
                    )
                    impact_score = random.uniform(0.5, 0.9)
                else:
                    summary = f"Neutral developments at {company_name} as company continues operations"
                    impact_score = random.uniform(0.1, 0.4)

                news_items.append(
                    NewsItem(
                        id=f"news_{symbol}_{i}_{j}",
                        symbol=symbol,
                        timestamp=timestamp,
                        headline=headline,
                        summary=summary,
                        sentiment=trend_type,
                        impact_score=round(impact_score, 2),
                    )
                )

        return sorted(news_items, key=lambda x: x.timestamp, reverse=True)

    def generate_products(self, symbol: str, sector: Sector) -> List[Product]:
        products = []
        product_count = random.randint(2, 5)
        sector_products = self.product_names.get(sector, ["Product A", "Product B"])

        for i in range(product_count):
            product_name = random.choice(sector_products)
            launch_date = datetime.now() - timedelta(days=random.randint(30, 1000))
            success_score = random.uniform(0.3, 1.0)

            products.append(
                Product(
                    id=f"product_{symbol}_{i}",
                    symbol=symbol,
                    name=product_name,
                    description=f"Advanced {product_name} solution with cutting-edge technology",
                    launch_date=launch_date,
                    success_score=round(success_score, 2),
                )
            )

        return products

    def generate_trends(self, symbol: str, days: int = 30) -> List[Trend]:
        trends = []
        trend_count = random.randint(5, 15)

        for i in range(trend_count):
            timestamp = datetime.now() - timedelta(days=random.randint(0, days))
            trend_type = random.choice(list(TrendType))
            confidence = random.uniform(0.5, 1.0)

            trend_descriptions = {
                TrendType.POSITIVE: [
                    "Increasing market share",
                    "Strong technical indicators",
                    "Positive analyst coverage",
                    "Growing customer base",
                ],
                TrendType.NEGATIVE: [
                    "Declining sales figures",
                    "Technical resistance levels",
                    "Negative market sentiment",
                    "Competitive pressures",
                ],
                TrendType.NEUTRAL: [
                    "Stable market position",
                    "Awaiting quarterly results",
                    "Consolidation phase",
                    "Market uncertainty",
                ],
            }

            description = random.choice(trend_descriptions[trend_type])

            trends.append(
                Trend(
                    id=f"trend_{symbol}_{i}",
                    symbol=symbol,
                    timestamp=timestamp,
                    trend_type=trend_type,
                    description=description,
                    confidence=round(confidence, 2),
                )
            )

        return sorted(trends, key=lambda x: x.timestamp, reverse=True)

    def generate_stocks(self) -> List[Stock]:
        stocks = []

        for company_data in self.companies:
            symbol = company_data["id"].upper()
            company = Company(**company_data)

            prices = self.generate_stock_prices(symbol)
            current_price = prices[-1].price if prices else 100.0

            # Generate fake order count for the last month (100 to 10000 orders)
            last_month_orders = random.randint(100, 10000)

            news = self.generate_news(symbol, company.name)
            products = self.generate_products(symbol, company.sector)
            trends = self.generate_trends(symbol)

            stock = Stock(
                symbol=symbol,
                company=company,
                current_price=current_price,
                last_month_orders=last_month_orders,
                prices=prices,
                news=news,
                products=products,
                trends=trends,
            )

            stocks.append(stock)

        return stocks
