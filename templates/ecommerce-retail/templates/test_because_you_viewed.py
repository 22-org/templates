"""
Test 'Because You Viewed' Session-based Recommendations using API Key
"""

import os

import requests
from dotenv import load_dotenv

load_dotenv(dotenv_path=".env")


def test_because_you_viewed(api_key: str):
    """Test 'Because You Viewed' Session-based Recommendations"""
    url = os.getenv("RECOMMEND_URL").rstrip("/")

    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api_key}",
    }

    sequence_data = {
        "current_session_views": [
            "smartphone_001",
            "laptop_001",
            "headphones_001",
        ],
        "session_duration": "15_minutes",
        "view_time": "evening",
        "user_preferences": {
            "preferred_brands": ["TechCorp", "AudioPro", "TechBrand"],
            "price_sensitivity": "medium",
            "desired_categories": ["electronics"],
        },
    }

    template = (
        "Since you viewed {current_session_views} in {view_time} "
        "for {session_duration}, "
        "recommend related products considering your preferences: "
        "{user_preferences}. "
        "Focus on complementary items to your viewed products."
    )

    payload = {
        "context": sequence_data,
        "template": template,
    }

    try:
        print("=== Testing Because You Viewed ===")
        print(f"Template: {template}")
        print(f"Sequence Data: {sequence_data}")

        response = requests.post(
            url=f"{url}/api/recommend/recommend",
            params={
                "model_key": "prag_v1",
                "num_results": 10,
                "user_id": "test_user",
            },
            headers=headers,
            json=payload,
        )
        print(response.text)
        response.raise_for_status()

        print(f"Recommendations: {response.json()}")

        return response.json()

    except Exception as e:
        print(f"Authenticated request failed: {e}")
        return None


if __name__ == "__main__":
    # Use your API key directly
    api_key = os.getenv("API_KEY", "YOUR_API_KEY_HERE")

    if api_key and api_key != "YOUR_API_KEY_HERE":
        print(f"Using API key: {api_key}")
        test_because_you_viewed(api_key=api_key)
    else:
        print("Please set your API_KEY in environment variables")
