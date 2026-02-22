"""
Test Case: Mental Health Support
Personalized mental health resources and therapy recommendations
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


def test_mental_health_support(token_data: TokenData, project_id: str):
    """Test Mental Health Support"""
    url = os.getenv("DODO_URL").rstrip("/")

    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {token_data['access_token']}",
    }

    sequence_data = {
        "primary_concerns": ["anxiety", "work_stress", "sleep_difficulties"],
        "severity_level": "moderate",
        "duration": "6_months",
        "previous_therapy": "none",
        "medications": ["none"],
        "symptoms": ["racing_thoughts", "irritability", "fatigue"],
        "triggers": ["work_deadlines", "social_situations"],
        "coping_mechanisms": ["avoidance", "overeating"],
        "support_system": "limited",
        "preferences": {
            "therapy_type": ["cbt", "mindfulness"],
            "format": ["online", "evening_sessions"],
            "gender_preference": "no_preference"
        },
        "insurance_coverage": "mental_health_included",
        "urgency": "moderate"
    }

    template = (
        "Recommend mental health support for concerns {primary_concerns}, "
        "{severity_level} severity, duration {duration}, previous therapy {previous_therapy}, "
        "medications {medications}, symptoms {symptoms}, triggers {triggers}, "
        "coping mechanisms {coping_mechanisms}, support system {support_system}, "
        "preferences {preferences}, insurance {insurance_coverage}, {urgency} urgency"
    )

    payload = {"sequence_data": sequence_data, "template": template}

    try:
        print("=== Testing Mental Health Support ===")
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
        name="Mental Health Support Test",
        description="Test project for mental health support",
    )

    # Make recommendations
    test_mental_health_support(token_data, project_id)
