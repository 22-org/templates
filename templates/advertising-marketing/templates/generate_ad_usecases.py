"""
Script to generate all advertising marketing use case test files
"""

import os

# Define all advertising use cases with their data
ad_use_cases = [
    {
        "filename": "test_retargeting_campaigns.py",
        "title": "Retargeting Campaigns",
        "description": "Ads shown to users who previously interacted with brand",
        "sequence_data": {
            "previous_interactions": ["website_visit", "product_view", "cart_addition"],
            "time_since_visit": "3_days",
            "interaction_depth": "high",
            "last_viewed_products": ["laptop", "headphones"]
        },
        "template": (
            "Retarget users who {previous_interactions} {time_since_visit} ago "
            "with {interaction_depth} engagement, focusing on {last_viewed_products}"
        )
    },
    {
        "filename": "test_lookalike_audience_targeting.py",
        "title": "Look-alike Audience Targeting",
        "description": "Target users similar to existing customers",
        "sequence_data": {
            "customer_profiles": ["tech_enthusiasts", "early_adopters"],
            "conversion_data": ["high_value", "frequent_buyers"],
            "behavioral_patterns": ["research_driven", "brand_loyal"],
            "target_similarity": "85%"
        },
        "template": (
            "Find look-alike audiences matching {customer_profiles} with "
            "{conversion_data} characteristics and {behavioral_patterns} behavior"
        )
    },
    {
        "filename": "test_dynamic_product_ads.py",
        "title": "Dynamic Product Ads",
        "description": "Automatically generated ads with personalized products",
        "sequence_data": {
            "product_catalog": ["electronics", "fashion", "home"],
            "user_browsing_history": ["laptops", "smartphones", "tablets"],
            "purchase_data": ["accessories", "cases", "chargers"],
            "personalization_level": "high"
        },
        "template": (
            "Create dynamic ads from {product_catalog} based on user's "
            "browsing of {user_browsing_history} and purchases of {purchase_data}"
        )
    },
    {
        "filename": "test_time_based_targeting.py",
        "title": "Time-based Targeting",
        "description": "Ads delivered at optimal times for each user",
        "sequence_data": {
            "activity_patterns": ["morning_browser", "evening_shopper"],
            "time_zones": ["PST", "EST"],
            "historical_engagement": ["high_morning", "peak_evening"],
            "optimal_timing": "7-9pm"
        },
        "template": (
            "Schedule ads during {optimal_timing} for {activity_patterns} "
            "in {time_zones} based on {historical_engagement} patterns"
        )
    },
    {
        "filename": "test_device_specific_targeting.py",
        "title": "Device-specific Targeting",
        "description": "Ads optimized for specific devices and platforms",
        "sequence_data": {
            "device_usage": ["mobile_primary", "desktop_secondary"],
            "platform_preferences": ["iOS", "Android", "Web"],
            "conversion_data": ["mobile_high", "desktop_medium"],
            "cross_device_behavior": "seamless"
        },
        "template": (
            "Optimize ads for {device_usage} users on {platform_preferences} "
            "platforms with {conversion_data} conversion rates"
        )
    },
    {
        "filename": "test_location_based_advertising.py",
        "title": "Location-based Advertising",
        "description": "Ads targeted based on user's geographic location",
        "sequence_data": {
            "location_data": ["urban_center", "suburban_area"],
            "gps_coordinates": "40.7128_N_74.0060_W",
            "location_history": ["downtown_frequent", "mall_visits"],
            "poi_proximity": "nearby_stores"
        },
        "template": (
            "Target ads for users in {location_data} at {gps_coordinates} "
            "with {location_history} patterns near {poi_proximity}"
        )
    },
    {
        "filename": "test_interest_based_targeting.py",
        "title": "Interest-based Targeting",
        "description": "Ads based on declared or inferred user interests",
        "sequence_data": {
            "interest_profiles": ["technology", "fitness", "travel"],
            "content_consumption": ["tech_blogs", "fitness_apps", "travel_sites"],
            "social_connections": ["tech_groups", "fitness_communities"],
            "inferred_interests": ["gadgets", "health", "adventure"]
        },
        "template": (
            "Target ads based on {interest_profiles} with content from "
            "{content_consumption} and {social_connections} engagement"
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
output_dir = "/Users/ericngo/Desktop/projects/templates/industry-templates/advertising-marketing/templates"

for use_case in ad_use_cases:
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

print("\\nAll advertising use case test files generated successfully!")
