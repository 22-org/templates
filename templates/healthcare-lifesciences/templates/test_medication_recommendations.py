"""
Test Case: Medication Recommendations
Suggest medications and dosages based on patient profile
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


def test_medication_recommendations(token_data: TokenData, project_id: str):
    """Test Medication Recommendations"""
    url = os.getenv("DODO_URL").rstrip("/")

    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {token_data['access_token']}",
    }

    sequence_data = {
        "patient_age": 58,
        "weight": 85,
        "height": 175,
        "primary_condition": "hypertension",
        "secondary_conditions": ["type2_diabetes", "high_cholesterol"],
        "current_medications": ["lisinopril", "metformin"],
        "allergies": ["sulfa", "statins"],
        "renal_function": "mild_impairment",
        "liver_function": "normal",
        "genetic_factors": ["CYP2C19_poor_metabolizer"],
        "lifestyle": ["moderate_alcohol", "non_smoker"]
    }

    template = (
        "Recommend medications for {patient_age} year old, {weight}kg, {height}cm, "
        "with {primary_condition} and {secondary_conditions}, "
        "current medications {current_medications}, allergies {allergies}, "
        "{renal_function} renal function, {liver_function} liver function, "
        "genetic factors {genetic_factors}, lifestyle {lifestyle}"
    )

    payload = {"sequence_data": sequence_data, "template": template}

    try:
        print("=== Testing Medication Recommendations ===")
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
        name="Medication Recommendations Test",
        description="Test project for medication recommendations",
    )

    # Make recommendations
    test_medication_recommendations(token_data, project_id)
