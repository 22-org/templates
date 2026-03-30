"""
Test Case: Behavioral Targeting Ads
Ads based on user's browsing and purchase behavior
"""

import os

import requests
from dotenv import load_dotenv
from shared.auth import TokenData

load_dotenv(dotenv_path=".env")

DODO_URL = "https://api.trydodo.xyz"


def get_jwt_token(email: str, password: str):
    """Sign in and extract JWT token"""
    url = os.getenv("DODO_URL").rstrip("/")
    try:
        response = requests.post(
            f"{url}/api/users/login",
            json={"email": email, "password": password},
            headers={"Content-Type": "application/json"},
        )
        response.raise_for_status()
        response = response.json()
        return {
            "access_token": response["access_token"],
            "refresh_token": response["refresh_token"],
            "user_id": response["user_id"],
            "expires_in": response["expires_in"],
        }
    except Exception as e:
        print(f"Sign in failed: {e}")
        return None


def generate_project(
    project_name: str,
    project_description: str,
):
    """Generate a project"""
    url = os.getenv("DODO_URL").rstrip("/")
    try:
        response = requests.post(
            f"{url}/api/projects/create",
            headers={"Content-Type": "application/json"},
            json={
                "name": project_name,
                "description": project_description,
            },
        )
        response.raise_for_status()
        response = response.json()
        return response["project_id"]
    except Exception as e:
        print(f"Project generation failed: {e}")
        return None


def test_behavioral_targeting_ads(token_data: TokenData, project_id: str):
    """Test Behavioral Targeting Ads"""
    url = os.getenv("DODO_URL").rstrip("/")

    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {token_data['access_token']}",
    }

    sequence_data = {
        "browsing_history": ["electronics", "fashion", "sports"],
        "purchase_data": ["laptop", "running_shoes", "jeans"],
        "time_spent": {"electronics": "15_minutes", "fashion": "8_minutes"},
        "user_segments": ["tech_enthusiast", "fashion_conscious"],
    }

    template = (
        "Target ads for user with browsing history in {browsing_history} and "
        "purchases of {purchase_data}, focusing on {user_segments} segments"
    )

    payload = {"sequence_data": sequence_data, "template": template}

    try:
        print("=== Testing Behavioral Targeting Ads ===")
        print(f"Template: {template}")
        print(f"Sequence Data: {sequence_data}")

        response = requests.post(
            url="https://api.trydodo.xyz/api/recommend",
            headers={
                "Content-Type": "application/json",
                "Authorization": f"Bearer {token_data['access_token']}",
            },
            json={
                "context": sequence_data,
                "catalog": {},
                "template": template,
                "num_results": 10,
                "model_key": "prag_v1",
            },
        )

        print(f"Response Status: {response.status_code}")
        if response.status_code == 200:
            result = response.json()
            print(f"Recommendations: {result}")
            return result
        else:
            print(f"Error Response: {response.text}")
            return None

    except Exception as e:
        print(f"Request failed: {e}")
        return None


def upload_entities(project_id: str, token_data: dict):
    """Upload ad campaign entities to project using the entities service"""
    url = os.getenv("ENTITIES_URL", os.getenv("DODO_URL")).rstrip("/")

    headers = {
        "Authorization": f"Bearer {token_data['access_token']}",
    }

    # Create sample CSV data for ad campaigns
    import csv
    import io

    # Sample ad campaign data for behavioral targeting
    campaigns = [
        {
            "entity_id": "campaign_001",
            "name": "Summer Fashion Sale",
            "category": "fashion",
            "budget": 50000.00,
            "description": "Summer clothing collection promotion",
            "brand": "FashionBrand",
            "target_audience": "fashion_shoppers",
            "duration_days": 30,
            "behavioral_signals": "recent_fashion_browsing, cart_abandonment",
        },
        {
            "entity_id": "campaign_002",
            "name": "Tech Gadget Launch",
            "category": "electronics",
            "budget": 75000.00,
            "description": "New smartphone launch campaign",
            "brand": "TechCorp",
            "target_audience": "tech_enthusiasts",
            "duration_days": 45,
            "behavioral_signals": "tech_browsing, previous_purchases",
        },
        {
            "entity_id": "campaign_003",
            "name": "Home Decor Promotion",
            "category": "home_garden",
            "budget": 30000.00,
            "description": "Home furniture and decor sale",
            "brand": "HomeStyle",
            "target_audience": "home_owners",
            "duration_days": 21,
            "behavioral_signals": "home_browsing, furniture_searches",
        },
        {
            "entity_id": "campaign_004",
            "name": "Fitness Equipment Sale",
            "category": "sports",
            "budget": 40000.00,
            "description": "Exercise and fitness equipment promotion",
            "brand": "FitGear",
            "target_audience": "fitness_enthusiasts",
            "duration_days": 14,
            "behavioral_signals": "fitness_app_usage, gym_browsing",
        },
        {
            "entity_id": "campaign_005",
            "name": "Travel Deals Campaign",
            "category": "travel",
            "budget": 60000.00,
            "description": "Vacation package and hotel deals",
            "brand": "TravelPlus",
            "target_audience": "travel_seekers",
            "duration_days": 60,
            "behavioral_signals": "travel_browsing, destination_searches",
        },
    ]

    try:
        print("=== Uploading Ad Campaign Entities ===")

        # Create CSV content in memory
        output = io.StringIO()
        if campaigns:
            fieldnames = campaigns[0].keys()
            writer = csv.DictWriter(output, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(campaigns)

        csv_content = output.getvalue()
        csv_file = io.BytesIO(csv_content.encode("utf-8"))

        # Create recommendation template
        template_content = {
            "template": (
                "Target users showing {behavioral_signals} behavior with "
                "{campaign_category} ads matching their interests"
            ),
            "required_fields": ["behavioral_signals", "campaign_category"],
            "output_fields": ["recommended_campaigns", "targeting_score"],
        }

        import json

        template_json = json.dumps(template_content)
        template_file = io.BytesIO(template_json.encode("utf-8"))

        files = {
            "files": ("ad_campaigns.csv", csv_file, "text/csv"),
            "template_file": (
                "recommendation_template.json",
                template_file,
                "application/json",
            ),
        }

        response = requests.post(
            url=f"{url}/api/entities/ingest",
            params={
                "project_id": project_id,
                "user_id": token_data["user_id"],
                "source": "files",
                "primary_key": "entity_id",
                "model_key": "bert",
            },
            headers=headers,
            files=files,
        )

        if response.status_code == 200:
            result = response.json()
            print("✓ Entity ingestion successful!")
            print(f"Response: {result}")
            return result
        else:
            print(f"✗ Entity ingestion failed: {response.text}")
            return None

    except Exception as e:
        print(f"Entity ingestion failed: {e}")
        if hasattr(e, "response") and e.response is not None:
            print(f"Response status: {e.response.status_code}")
            print(f"Response content: {e.response.text}")
        return None


if __name__ == "__main__":
    email = "YOUR_EMAIL_ADDRESS"
    password = "YOUR_PASSWORD"
    project_id = "YOUR_PROJECT_ID"

    # Sign-in
    token_data = get_jwt_token(email, password)

    # Generate project
    project_id = generate_project(
        name="Behavioral Targeting Ads Test",
        description="Test project for behavioral targeting advertisements",
    )

    # Upload entities (aka ad campaigns in advertising contexts)
    upload_entities(project_id, token_data)

    # Make recommendations
    test_behavioral_targeting_ads(token_data, project_id)

    # Possible result:
    # {
    #   "status_code": 200,
    #   "results": [
    #     "campaign_001",
    #     "campaign_002",
    #     "campaign_003",
    #     "campaign_004"
    #   ]
    # }
