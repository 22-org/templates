"""
Test Case: Chronic Disease Management
Personalized care plans for chronic conditions
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


def test_chronic_disease_management(token_data: TokenData, project_id: str):
    """Test Chronic Disease Management"""
    url = os.getenv("DODO_URL").rstrip("/")

    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {token_data['access_token']}",
    }

    sequence_data = {
        "primary_condition": "type2_diabetes",
        "duration": "8_years",
        "current_medications": ["metformin", "lisinopril"],
        "blood_glucose_levels": {
            "fasting": 145,
            "post_meal": 200,
            "hba1c": 7.8
        },
        "complications": ["early_nephropathy"],
        "comorbidities": ["hypertension", "obesity"],
        "lifestyle_factors": {
            "diet": "high_carb",
            "exercise": "minimal",
            "smoking": "non_smoker",
            "alcohol": "occasional"
        },
        "monitoring_compliance": "inconsistent",
        "barriers": ["time_constraints", "motivation_issues"],
        "goals": ["improve_glucose_control", "weight_loss", "prevent_complications"],
        "support_system": "family_supportive"
    }

    template = (
        "Create chronic disease management plan for {primary_condition} duration {duration}, "
        "medications {current_medications}, glucose levels {blood_glucose_levels}, "
        "complications {complications}, comorbidities {comorbidities}, "
        "lifestyle {lifestyle_factors}, {monitoring_compliance} monitoring, "
        "barriers {barriers}, goals {goals}, support system {support_system}"
    )

    payload = {"sequence_data": sequence_data, "template": template}

    try:
        print("=== Testing Chronic Disease Management ===")
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
        name="Chronic Disease Management Test",
        description="Test project for chronic disease management",
    )

    # Make recommendations
    test_chronic_disease_management(token_data, project_id)
