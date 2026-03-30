"""
Test Case: Credit Card Recommendations
Suggest credit cards based on spending patterns and credit profile
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


def test_credit_card_recommendations(token_data: TokenData, project_id: str):
    """Test Credit Card Recommendations"""
    url = os.getenv("DODO_URL").rstrip("/")

    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {token_data['access_token']}",
    }

    sequence_data = {
        "credit_score": 750,
        "annual_income": 85000,
        "spending_pattern": {
            "groceries": 800,
            "dining": 400,
            "travel": 600,
            "gas": 200,
            "shopping": 300,
        },
        "lifestyle": "frequent_traveler",
        "preferred_benefits": ["cash_back", "travel_points", "no_annual_fee"],
    }

    template = (
        "Recommend credit cards for customer with credit score {credit_score}, "
        "annual income ${annual_income}, spending pattern {spending_pattern}, "
        "lifestyle {lifestyle}, seeking benefits {preferred_benefits}"
    )

    payload = {"sequence_data": sequence_data, "template": template}

    try:
        print("=== Testing Credit Card Recommendations ===")
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
                "model_key": "prag_v1"
            },
