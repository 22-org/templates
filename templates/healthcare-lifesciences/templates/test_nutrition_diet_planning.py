"""
Test Case: Nutrition and Diet Planning
Personalized nutrition plans based on health profile
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


def test_nutrition_diet_planning(token_data: TokenData, project_id: str):
    """Test Nutrition and Diet Planning"""
    url = os.getenv("DODO_URL").rstrip("/")

    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {token_data['access_token']}",
    }

    sequence_data = {
        "age": 42,
        "gender": "male",
        "height": 178,
        "weight": 95,
        "activity_level": "moderate",
        "health_conditions": ["prediabetes", "hypertension", "acid_reflux"],
        "allergies": ["shellfish", "nuts"],
        "dietary_restrictions": ["low_sodium", "low_sugar"],
        "food_preferences": ["mediterranean", "grilled", "fresh_vegetables"],
        "nutritional_goals": ["weight_loss", "blood_sugar_control", "heart_health"],
        "current_diet": {
            "breakfast": "cereal_with_sugar",
            "lunch": "fast_food",
            "dinner": "processed_meals",
            "snacks": "chips_cookies"
        },
        "cooking_skills": "basic",
        "budget": "moderate",
        "time_constraints": "limited_cooking_time"
    }

    template = (
        "Create nutrition plan for {age} year old {gender}, {height}cm, {weight}kg, "
        "{activity_level} activity, conditions {health_conditions}, allergies {allergies}, "
        "restrictions {dietary_restrictions}, preferences {food_preferences}, "
        "goals {nutritional_goals}, current diet {current_diet}, "
        "{cooking_skills} cooking skills, {budget} budget, {time_constraints}"
    )

    payload = {"sequence_data": sequence_data, "template": template}

    try:
        print("=== Testing Nutrition and Diet Planning ===")
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
        name="Nutrition Diet Planning Test",
        description="Test project for nutrition diet planning",
    )

    # Make recommendations
    test_nutrition_diet_planning(token_data, project_id)
