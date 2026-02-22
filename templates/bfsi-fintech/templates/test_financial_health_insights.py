"""
Test Case: Financial Health Insights
Personalized financial tips and product suggestions
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


def test_financial_health_insights(token_data: TokenData, project_id: str):
    """Test Financial Health Insights"""
    url = os.getenv("DODO_URL").rstrip("/")

    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {token_data['access_token']}",
    }

    sequence_data = {
        "spending_patterns": {
            "housing": 0.30,
            "food": 0.15,
            "transportation": 0.12,
            "entertainment": 0.08,
            "savings": 0.20
        },
        "income": 75000,
        "debt_levels": {
            "credit_card": 2000,
            "student_loans": 15000,
            "car_loan": 8000
        },
        "financial_goals": ["emergency_fund", "debt_reduction"],
        "credit_score": 680,
        "savings_rate": 0.15,
        "investment_participation": "minimal"
    }

    template = (
        "Provide financial health insights for spending patterns {spending_patterns}, "
        "annual income ${income}, debt levels {debt_levels}, goals {financial_goals}, "
        "credit score {credit_score}, {savings_rate} savings rate, "
        "{investment_participation} investment participation"
    )

    payload = {"sequence_data": sequence_data, "template": template}

    try:
        print("=== Testing Financial Health Insights ===")
        print(f"Template: {template}")
        print(f"Sequence Data: {sequence_data}")

        response = requests.post(
            url=f"{url}/api/recommend/recommend",
            params={
                "project_id": project_id,
                "model_key": "bert",
                "num_results": 10,
                "user_id": token_data["user_id"],
            },
            headers=headers,
            json=payload,
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


if __name__ == "__main__":
    email = "YOUR_EMAIL_ADDRESS"
    password = "YOUR_PASSWORD"
    project_id = "YOUR_PROJECT_ID"

    # Sign-in
    token_data = get_jwt_token(email, password)

    # Generate project
    project_id = generate_project(
        name="Financial Health Insights Test",
        description="Test project for financial health insights",
    )

    # Make recommendations
    test_financial_health_insights(token_data, project_id)
