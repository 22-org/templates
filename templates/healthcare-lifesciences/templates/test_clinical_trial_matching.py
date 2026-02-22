"""
Test Case: Clinical Trial Matching
Match patients with relevant clinical trials
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


def test_clinical_trial_matching(token_data: TokenData, project_id: str):
    """Test Clinical Trial Matching"""
    url = os.getenv("DODO_URL").rstrip("/")

    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {token_data['access_token']}",
    }

    sequence_data = {
        "primary_diagnosis": "metastatic_breast_cancer",
        "cancer_stage": "stage_4",
        "biomarkers": ["HER2_positive", "BRCA1_mutation"],
        "previous_treatments": ["chemotherapy", "radiation", "hormone_therapy"],
        "current_medications": ["palliative_care"],
        "age": 47,
        "gender": "female",
        "performance_status": "ECOG_1",
        "comorbidities": ["mild_diabetes"],
        "location": "boston_massachusetts",
        "travel_radius": "100_miles",
        "trial_preferences": ["phase_2", "targeted_therapy"],
        "exclusion_criteria": ["pregnant", "severe_heart_disease"]
    }

    template = (
        "Match clinical trials for {primary_diagnosis} {cancer_stage}, "
        "biomarkers {biomarkers}, previous treatments {previous_treatments}, "
        "current medications {current_medications}, {age} year old {gender}, "
        "{performance_status} performance status, comorbidities {comorbidities}, "
        "location {location}, {travel_radius} travel radius, preferences {trial_preferences}, "
        "exclusions {exclusion_criteria}"
    )

    payload = {"sequence_data": sequence_data, "template": template}

    try:
        print("=== Testing Clinical Trial Matching ===")
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
        name="Clinical Trial Matching Test",
        description="Test project for clinical trial matching",
    )

    # Make recommendations
    test_clinical_trial_matching(token_data, project_id)
