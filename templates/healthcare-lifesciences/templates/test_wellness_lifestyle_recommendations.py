"""
Test Case: Wellness and Lifestyle Recommendations
Personalized diet, exercise, and lifestyle suggestions
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


def test_wellness_lifestyle_recommendations(token_data: TokenData, project_id: str):
    """Test Wellness and Lifestyle Recommendations"""
    url = os.getenv("DODO_URL").rstrip("/")

    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {token_data['access_token']}",
    }

    sequence_data = {
        "age": 38,
        "gender": "female",
        "health_goals": ["weight_loss", "stress_reduction", "better_sleep"],
        "current_activity_level": "sedentary",
        "activity_preferences": ["yoga", "walking", "swimming"],
        "dietary_restrictions": ["vegetarian", "gluten_intolerant"],
        "food_preferences": ["mediterranean", "low_sugar"],
        "sleep_patterns": {
            "average_hours": 6,
            "quality": "poor",
            "issues": ["difficulty_falling_asleep"]
        },
        "stress_level": "high",
        "work_schedule": "desk_job_9_to_5",
        "available_time": "30_minutes_daily"
    }

    template = (
        "Recommend wellness plan for {age} year old {gender} with goals {health_goals}, "
        "{current_activity_level} activity level, prefers {activity_preferences}, "
        "dietary restrictions {dietary_restrictions}, food preferences {food_preferences}, "
        "sleep patterns {sleep_patterns}, {stress_level} stress level, "
        "{work_schedule} work schedule, {available_time} available time"
    )

    payload = {"sequence_data": sequence_data, "template": template}

    try:
        print("=== Testing Wellness and Lifestyle Recommendations ===")
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
        name="Wellness Lifestyle Recommendations Test",
        description="Test project for wellness lifestyle recommendations",
    )

    # Make recommendations
    test_wellness_lifestyle_recommendations(token_data, project_id)
