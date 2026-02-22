"""
Script to generate all remaining e-commerce use case test files
"""

import os

# Define all use cases with their data
use_cases = [
    {
        "filename": "test_complete_collection.py",
        "title": "Complete Your Collection",
        "description": "Products from same category or collection",
        "sequence_data": {
            "owned_products": ["iphone_13", "airpods_pro"],
            "product_ecosystem": "apple",
            "missing_items": ["macbook", "ipad", "apple_watch"]
        },
        "template": (
            "Help complete your {product_ecosystem} collection. "
            "You already have {owned_products}, consider {missing_items}"
        )
    },
    {
        "filename": "test_price_range_alternatives.py",
        "title": "Price Range Alternatives",
        "description": "Similar products in different price ranges",
        "sequence_data": {
            "viewed_product": "premium_laptop",
            "viewed_price": 2000.0,
            "budget_range": "under_1000",
            "preferred_features": ["fast_processor", "good_battery", "lightweight"]
        },
        "template": (
            "You viewed {viewed_product} at ${viewed_price}. "
            "Here are alternatives under $1000 with {preferred_features}"
        )
    },
    {
        "filename": "test_new_arrivals.py",
        "title": "New Arrivals",
        "description": "Recently added products matching user preferences",
        "sequence_data": {
            "user_interests": ["technology", "fitness", "outdoor"],
            "new_categories": ["smart_home", "wearables", "camping_gear"],
            "launch_period": "last_30_days"
        },
        "template": (
            "Discover new arrivals in {new_categories} from {launch_period} "
            "based on your interest in {user_interests}"
        )
    },
    {
        "filename": "test_personalized_result_ranking.py",
        "title": "Personalized Result Ranking",
        "description": "Reorder search results based on user behavior",
        "sequence_data": {
            "search_query": "laptop",
            "user_history": ["electronics", "computers", "gaming"],
            "purchase_history": ["dell_xps", "macbook_pro"],
            "price_sensitivity": "medium"
        },
        "template": (
            "Rank search results for '{search_query}' based on user's history "
            "with {user_history} and purchases of {purchase_history}"
        )
    },
    {
        "filename": "test_query_autocompletion.py",
        "title": "Query Auto-completion",
        "description": "Suggest search queries based on user history",
        "sequence_data": {
            "partial_query": "lap",
            "previous_searches": ["laptop", "laptop stand", "laptop bag"],
            "user_category_preference": "electronics"
        },
        "template": (
            "Complete the query '{partial_query}' based on previous searches "
            "like {previous_searches} and interest in {user_category_preference}"
        )
    },
    {
        "filename": "test_did_you_mean_corrections.py",
        "title": "Did You Mean Corrections",
        "description": "Spell correction based on user vocabulary",
        "sequence_data": {
            "misspelled_query": "laptap",
            "user_vocabulary": ["laptop", "tablet", "notebook"],
            "common_typos": ["laptap", "labtop", "laptopp"]
        },
        "template": (
            "Correct '{misspelled_query}' based on user's vocabulary "
            "{user_vocabulary} and common typos {common_typos}"
        )
    },
    {
        "filename": "test_category_aware_search.py",
        "title": "Category-aware Search",
        "description": "Prioritize results from preferred categories",
        "sequence_data": {
            "search_query": "gift",
            "preferred_categories": ["electronics", "books", "home"],
            "avoid_categories": ["clothing", "beauty"],
            "season": "holiday"
        },
        "template": (
            "For '{search_query}' search, prioritize results from {preferred_categories} "
            "and avoid {avoid_categories} for {season} season"
        )
    },
    {
        "filename": "test_price_sensitive_search.py",
        "title": "Price-sensitive Search",
        "description": "Adjust results based on price sensitivity",
        "sequence_data": {
            "search_query": "headphones",
            "typical_price_range": "50-100",
            "price_sensitivity": "high",
            "value_preferences": ["durability", "sound_quality"]
        },
        "template": (
            "Search for '{search_query}' in ${typical_price_range} range, "
            "focusing on {value_preferences} for price-sensitive user"
        )
    },
    {
        "filename": "test_brand_preference_integration.py",
        "title": "Brand Preference Integration",
        "description": "Boost results based on brand preferences",
        "sequence_data": {
            "search_query": "smartphone",
            "preferred_brands": ["apple", "samsung"],
            "avoid_brands": ["unknown_brands"],
            "brand_loyalty": "high"
        },
        "template": (
            "For '{search_query}' search, boost results from {preferred_brands} "
            "and avoid {avoid_brands} for brand-loyal user"
        )
    },
    {
        "filename": "test_visual_similarity_search.py",
        "title": "Visual Similarity Search",
        "description": "Find visually similar products",
        "sequence_data": {
            "viewed_product_image": "red_running_shoes.jpg",
            "visual_features": ["red_color", "athletic_style", "mesh_material"],
            "similar_attributes": ["comfort", "breathability", "durability"]
        },
        "template": (
            "Find products visually similar to {viewed_product_image} "
            "with features like {visual_features} and attributes {similar_attributes}"
        )
    },
    {
        "filename": "test_context_aware_search.py",
        "title": "Context-aware Search",
        "description": "Adjust results based on context",
        "sequence_data": {
            "search_query": "restaurant",
            "current_time": "evening",
            "user_location": "downtown",
            "device_type": "mobile",
            "weather": "rainy"
        },
        "template": (
            "Search for '{search_query}' in {user_location} during {current_time} "
            "on {device_type}, considering {weather} weather"
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


def get_jwt_token(email: str, password: str):
    """Sign in and extract JWT token"""
    url = os.getenv("ADMIN_URL").rstrip("/")
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


def test_{function_name}(token_data: TokenData, project_id: str):
    """Test '{title}'"""
    url = os.getenv("RECOMMEND_URL").rstrip("/")
    
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
    email = "dat.ngo3246@gmail.com"
    password = "password"
    project_id = os.getenv("PROJECT_ID", "698cb6e723c249dbb3c5f766")

    token_data = get_jwt_token(email, password)
    
    if token_data:
        test_{function_name}(token_data, project_id)
'''

# Generate all test files
output_dir = "/Users/ericngo/Desktop/projects/dudu/recommend/usecases"

for use_case in use_cases:
    filename = use_case["filename"]
    title = use_case["title"]
    description = use_case["description"]
    sequence_data = use_case["sequence_data"]
    template = use_case["template"]
    
    # Convert function name to valid Python identifier
    function_name = filename.replace("test_", "").replace(".py", "_").replace("-", "_")
    
    # Format sequence data and template for the template
    sequence_data_str = str(sequence_data).replace("'", '"')
    template_str = f'"{template}"'
    
    # Generate file content
    file_content = test_file_template.format(
        title=title,
        description=description,
        function_name=function_name,
        sequence_data_str=sequence_data_str,
        template_str=template_str
    )
    
    # Write file
    filepath = os.path.join(output_dir, filename)
    with open(filepath, 'w') as f:
        f.write(file_content)
    
    print(f"Generated: {filename}")

print("\\nAll use case test files generated successfully!")
