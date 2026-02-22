"""
Test Case: Health Education Content
Personalized health education and information
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


def test_health_education_content(token_data: TokenData, project_id: str):
    """Test Health Education Content"""
    url = os.getenv("DODO_URL").rstrip("/")

    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {token_data['access_token']}",
    }

    sequence_data = {
        "health_conditions": ["newly_diagnosed_diabetes", "hypertension"],
        "health_literacy_level": "basic",
        "learning_preferences": ["visual", "step_by_step"],
        "preferred_content_types": ["videos", "infographics", "simple_articles"],
        "language": "english",
        "cultural_considerations": ["spanish_speaking_community"],
        "age_group": "middle_aged",
        "technology_access": "smartphone_only",
        "information_needs": ["diet_management", "exercise_benefits", "medication_understanding"],
        "concerns": ["complications", "lifestyle_changes", "cost"],
        "motivation_level": "moderate"
    }

    template = (
        "Recommend health education content for conditions {health_conditions}, "
        "{health_literacy_level} literacy, learning preferences {learning_preferences}, "
        "content types {preferred_content_types}, language {language}, "
        "cultural considerations {cultural_considerations}, {age_group} age group, "
        "{technology_access} technology access, needs {information_needs}, "
        "concerns {concerns}, {motivation_level} motivation"
    )

    payload = {"sequence_data": sequence_data, "template": template}

    try:
        print("=== Testing Health Education Content ===")
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
        name="Health Education Content Test",
        description="Test project for health education content",
    )

    # Make recommendations
    test_health_education_content(token_data, project_id)
