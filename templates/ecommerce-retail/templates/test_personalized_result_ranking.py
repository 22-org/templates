"""
Test Case: 'Personalized Result Ranking' Reorder search results based on user behavior
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


def test_personalized_result_ranking_(token_data: TokenData, project_id: str):
    """Test 'Personalized Result Ranking'"""
    url = os.getenv("DODO_URL").rstrip("/")
    
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {token_data['access_token']}",
    }

    sequence_data = {"search_query": "laptop", "user_history": ["electronics", "computers", "gaming"], "purchase_history": ["dell_xps", "macbook_pro"], "price_sensitivity": "medium"}
    
    template = "Rank search results for '{search_query}' based on user's history with {user_history} and purchases of {purchase_history}"  # noqa

    payload = {"sequence_data": sequence_data, "template": template}

    try:
        print("=== Testing Personalized Result Ranking ===")
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
        name="Personalized Result Ranking  Test",
        description="Test project for test personalized result ranking  recommendations",
    )

    # Make recommendations
    test_personalized_result_ranking_(token_data, project_id)
