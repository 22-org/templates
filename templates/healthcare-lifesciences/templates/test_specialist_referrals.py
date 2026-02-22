"""
Test Case: Specialist Referrals
Recommend appropriate specialists based on symptoms and history
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


def test_specialist_referrals(token_data: TokenData, project_id: str):
    """Test Specialist Referrals"""
    url = os.getenv("DODO_URL").rstrip("/")

    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {token_data['access_token']}",
    }

    sequence_data = {
        "primary_symptoms": ["chest_pain", "shortness_of_breath", "palpitations"],
        "symptom_duration": "2_weeks",
        "symptom_severity": "moderate",
        "medical_history": ["hypertension", "family_heart_disease"],
        "previous_specialists": ["cardiologist_3_years_ago"],
        "current_medications": ["blood_pressure_medication"],
        "diagnostic_tests": ["ecg_normal", "basic_labs_normal"],
        "location": "new_york_city",
        "insurance": "ppo_network",
        "urgency": "non_emergency",
        "preferences": ["female_doctor", "hospital_affiliation"]
    }

    template = (
        "Recommend specialist for symptoms {primary_symptoms} lasting {symptom_duration}, "
        "{symptom_severity} severity, history {medical_history}, "
        "previous specialists {previous_specialists}, medications {current_medications}, "
        "tests {diagnostic_tests}, location {location}, insurance {insurance}, "
        "{urgency} urgency, preferences {preferences}"
    )

    payload = {"sequence_data": sequence_data, "template": template}

    try:
        print("=== Testing Specialist Referrals ===")
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
        name="Specialist Referrals Test",
        description="Test project for specialist referrals",
    )

    # Make recommendations
    test_specialist_referrals(token_data, project_id)
