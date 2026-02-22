"""
Script to generate all travel hospitality use case test files
"""

import os

# Define all travel use cases with their data
travel_use_cases = [
    {
        "filename": "test_flight_recommendations.py",
        "title": "Flight Recommendations",
        "description": "Suggest flights based on preferences, budget, and schedule",
        "sequence_data": {
            "travel_patterns": ["direct_flights", "morning_departures"],
            "airline_preferences": ["delta", "united", "emirates"],
            "price_history": "economy_premium",
            "schedule_preference": "non_stop",
            "booking_window": "advance"
        },
        "template": (
            "Recommend flights with {schedule_preference} and {booking_window} booking "
            "for traveler preferring {airline_preferences} with {price_history} history"
        )
    },
    {
        "filename": "test_activity_experience_suggestions.py",
        "title": "Activity and Experience Suggestions",
        "description": "Recommend activities, tours, and local experiences",
        "sequence_data": {
            "activity_history": ["water_sports", "cultural_tours", "hiking"],
            "interests": ["adventure", "culture", "nature"],
            "location": "tropical_destination",
            "time_constraints": "half_day",
            "group_size": "couple"
        },
        "template": (
            "Suggest {time_constraints} activities in {location} for {group_size} "
            "interested in {interests} based on {activity_history} experience"
        )
    },
    {
        "filename": "test_restaurant_dining_recommendations.py",
        "title": "Restaurant and Dining Recommendations",
        "description": "Suggest restaurants based on cuisine preferences and reviews",
        "sequence_data": {
            "dining_history": ["italian", "asian_fusion", "seafood"],
            "cuisine_preferences": ["mediterranean", "local_specialties"],
            "price_range": "mid_range",
            "reviews": "4_plus_stars",
            "dining_style": "fine_dining"
        },
        "template": (
            "Recommend {dining_style} restaurants with {reviews} in {price_range} "
            "for diner preferring {cuisine_preferences} with {dining_history} background"
        )
    },
    {
        "filename": "test_travel_package_recommendations.py",
        "title": "Travel Package Recommendations",
        "description": "Recommend complete travel packages and deals",
        "sequence_data": {
            "package_preferences": ["all_inclusive", "guided_tours"],
            "budget_constraints": "moderate_budget",
            "travel_dates": "summer_season",
            "group_composition": "family_with_kids",
            "duration": "7_days"
        },
        "template": (
            "Create {duration} {package_preferences} packages for {group_composition} "
            "in {travel_dates} with {budget_constraints} constraints"
        )
    },
    {
        "filename": "test_seasonal_event_recommendations.py",
        "title": "Seasonal and Event-based Recommendations",
        "description": "Suggest destinations based on seasons and events",
        "sequence_data": {
            "event_calendars": ["festivals", "sporting_events"],
            "seasonal_patterns": ["peak_season", "off_season"],
            "user_interests": ["cultural_events", "music_festivals"],
            "weather_preference": "warm_climate",
            "timing": "specific_dates"
        },
        "template": (
            "Recommend destinations for {timing} with {event_calendars} during "
            "{seasonal_patterns} for traveler interested in {user_interests}"
        )
    },
    {
        "filename": "test_loyalty_program_personalization.py",
        "title": "Loyalty Program Personalization",
        "description": "Personalized offers and rewards for loyalty members",
        "sequence_data": {
            "loyalty_status": "gold_member",
            "booking_history": ["frequent_traveler", "premium_bookings"],
            "redemption_patterns": ["room_upgrades", "lounge_access"],
            "points_balance": "high_balance",
            "preferences": ["experiential_rewards"]
        },
        "template": (
            "Personalize loyalty offers for {loyalty_status} with {points_balance} "
            "based on {booking_history} and {redemption_patterns} preferences"
        )
    },
    {
        "filename": "test_travel_insurance_recommendations.py",
        "title": "Travel Insurance Recommendations",
        "description": "Suggest appropriate travel insurance coverage",
        "sequence_data": {
            "trip_details": ["international_travel", "adventure_activities"],
            "traveler_profile": ["family_coverage", "pre_existing_conditions"],
            "destination_risks": ["high_risk_area", "medical_facilities"],
            "coverage_needs": ["comprehensive", "medical_evacuation"],
            "trip_value": "high_value"
        },
        "template": (
            "Recommend {coverage_needs} insurance for {trip_details} with "
            "{destination_risks} for traveler with {traveler_profile} profile"
        )
    },
    {
        "filename": "test_transportation_transfer_suggestions.py",
        "title": "Transportation and Transfer Suggestions",
        "description": "Recommend local transportation and airport transfers",
        "sequence_data": {
            "arrival_times": ["evening_arrival", "early_morning_departure"],
            "location": "city_center_hotel",
            "preferences": ["private_transfer", "cost_effective"],
            "luggage_requirements": "multiple_bags",
            "group_size": "small_group"
        },
        "template": (
            "Suggest {preferences} transportation for {group_size} with "
            "{luggage_requirements} for {arrival_times} to {location}"
        )
    }
]

# Template for generating test files
test_file_template = '''"""
Test Case: '{title}' {description}
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
            f"{{url}}/api/users/login",
            json={{"email": email, "password": password}},
            headers={{"Content-Type": "application/json"}},
        )
        response.raise_for_status()
        response = response.json()
        return {{
            "access_token": response["access_token"],
            "refresh_token": response["refresh_token"],
            "user_id": response["user_id"],
            "expires_in": response["expires_in"],
        }}
    except Exception as e:
        print(f"Sign in failed: {{e}}")
        return None


def generate_project(
    project_name: str,
    project_description: str,
):
    """Generate a project"""
    url = os.getenv("DODO_URL").rstrip("/")
    try:
        response = requests.post(
            f"{{url}}/api/projects/create",
            headers={{"Content-Type": "application/json"}},
            json={{
                "name": project_name,
                "description": project_description,
            }},
        )
        response.raise_for_status()
        response = response.json()
        return response["project_id"]
    except Exception as e:
        print(f"Project generation failed: {{e}}")
        return None


def test_{function_name}(token_data: TokenData, project_id: str):
    """Test '{title}'"""
    url = os.getenv("DODO_URL").rstrip("/")

    headers = {{
        "Content-Type": "application/json",
        "Authorization": f"Bearer {{token_data['access_token']}}",
    }}

    sequence_data = {sequence_data_str}

    template = {template_str}

    payload = {{"sequence_data": sequence_data, "template": template}}

    try:
        print("=== Testing {title} ===")
        print(f"Template: {{template}}")
        print(f"Sequence Data: {{sequence_data}}")

        response = requests.post(
            url=f"{{url}}/api/recommend/recommend",
            params={{
                "project_id": project_id,
                "model_key": "bert",
                "num_results": 10,
                "user_id": token_data["user_id"],
            }},
            headers=headers,
            json=payload,
        )

        print(f"Response Status: {{response.status_code}}")
        if response.status_code == 200:
            result = response.json()
            print(f"Recommendations: {{result}}")
            return result
        else:
            print(f"Error Response: {{response.text}}")
            return None

    except Exception as e:
        print(f"Request failed: {{e}}")
        return None


if __name__ == "__main__":
    email = "YOUR_EMAIL_ADDRESS"
    password = "YOUR_PASSWORD"
    project_id = "YOUR_PROJECT_ID"

    # Sign-in
    token_data = get_jwt_token(email, password)

    # Generate project
    project_id = generate_project(
        name="{title} Test",
        description="Test project for {title_lower}",
    )

    # Make recommendations
    test_{function_name}(token_data, project_id)
'''

# Generate all test files
output_dir = "/Users/ericngo/Desktop/projects/templates/industry-templates/travel-hospitality/templates"

for use_case in travel_use_cases:
    filename = use_case["filename"]
    title = use_case["title"]
    description = use_case["description"]
    sequence_data = use_case["sequence_data"]
    template = use_case["template"]
    
    # Convert function name to valid Python identifier
    function_name = filename.replace("test_", "").replace(".py", "_").replace("-", "_")
    title_lower = title.lower().replace(" ", "_")
    
    # Format sequence data and template for the template
    sequence_data_str = str(sequence_data).replace("'", '"')
    template_str = f'"{template}"'
    
    # Generate file content
    file_content = test_file_template.format(
        title=title,
        description=description,
        function_name=function_name,
        title_lower=title_lower,
        sequence_data_str=sequence_data_str,
        template_str=template_str
    )
    
    # Write file
    filepath = os.path.join(output_dir, filename)
    with open(filepath, 'w') as f:
        f.write(file_content)
    
    print(f"Generated: {filename}")

print("\\nAll travel hospitality use case test files generated successfully!")
