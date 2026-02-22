"""
Test Case: 'Because You Viewed' Session-based Recommendations
Real-time suggestions based on current browsing session
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


def test_because_you_viewed(token_data: TokenData, project_id: str):
    """Test 'Because You Viewed' Session-based Recommendations"""
    url = os.getenv("DODO_URL").rstrip("/")

    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {token_data['access_token']}",
    }

    sequence_data = {
        "current_session_views": ["smartphone_001", "laptop_001", "headphones_001"],
        "session_duration": "15_minutes",
        "view_time": "evening",
        "user_preferences": {
            "preferred_brands": ["TechCorp", "AudioPro", "TechBrand"],
            "price_sensitivity": "medium",
            "desired_categories": ["electronics"],
        },
    }

    template = (
        "Since you viewed {current_session_views} in {view_time} for {session_duration}, "
        "recommend related products considering your preferences: {user_preferences}. "
        "Focus on complementary items to your viewed products."
    )

    payload = {"sequence_data": sequence_data, "template": template}

    try:
        print("=== Testing Because You Viewed ===")
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


def upload_entities(project_id: str, token_data: dict):
    """Upload product entities to project using the entities service"""

    url = os.getenv("ENTITIES_URL", os.getenv("DODO_URL")).rstrip("/")

    headers = {
        "Authorization": f"Bearer {token_data['access_token']}",
    }

    try:
        print("=== Uploading Product Entities ===")

        with (
            open("product_catalog.csv", "rb") as catalog_file,
            open("entity_template.json", "rb") as template_file,
        ):

            files = {
                "files": ("entities.csv", catalog_file, "text/csv"),
                "template_file": (
                    "entity_template.json",
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
        name="Because You Viewed Test",
        description="Test project for session-based recommendations",
    )

    # Upload entities (aka products in e-commerce and retail contexts)
    upload_entities(project_id, token_data)

    # Make recommendations
    test_because_you_viewed(token_data, project_id)

    # Possible result:
    # {
    #   "status_code": 200,
    #   "results": [
    #     "tablet_001",
    #     "smartwatch_001",
    #     "camera_001",
    #     "mouse_001"
    #   ]
    # }
