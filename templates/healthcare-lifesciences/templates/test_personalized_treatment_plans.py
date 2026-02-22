"""
Test Case: Personalized Treatment Plans
Recommend treatment options based on patient profile and medical history
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


def test_personalized_treatment_plans(token_data: TokenData, project_id: str):
    """Test Personalized Treatment Plans"""
    url = os.getenv("DODO_URL").rstrip("/")

    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {token_data['access_token']}",
    }

    sequence_data = {
        "patient_age": 45,
        "gender": "female",
        "primary_condition": "type2_diabetes",
        "comorbidities": ["hypertension", "obesity"],
        "symptoms": ["fatigue", "increased_thirst", "frequent_urination"],
        "lab_results": {
            "blood_glucose": 180,
            "hba1c": 8.2,
            "blood_pressure": "145/90"
        },
        "medications": ["metformin"],
        "allergies": ["penicillin"],
        "lifestyle_factors": {
            "activity_level": "sedentary",
            "diet": "high_carb",
            "smoking": "non_smoker"
        }
    }

    template = (
        "Recommend treatment plan for {patient_age} year old {gender} with "
        "{primary_condition} and comorbidities {comorbidities}, "
        "symptoms {symptoms}, lab results {lab_results}, "
        "current medications {medications}, allergies {allergies}, "
        "lifestyle {lifestyle_factors}"
    )

    payload = {"sequence_data": sequence_data, "template": template}

    try:
        print("=== Testing Personalized Treatment Plans ===")
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
        name="Personalized Treatment Plans Test",
        description="Test project for personalized treatment plans",
    )

    # Make recommendations
    test_personalized_treatment_plans(token_data, project_id)
