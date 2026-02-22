"""
Comprehensive test cases for E-commerce Recommendation Systems
Tests all use cases from the combined e-commerce use cases document
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
            f"{url}/api/users/login",
            json={
                "email": email,
                "password": password,
            },
            headers={
                "Content-Type": "application/json",
            },
        )
        response.raise_for_status()

        response = response.json()
        print("Successfully signed in!")
        print(f"Access Token (JWT): {response['access_token']}")
        print(f"User ID: {response['user_id']}")

        return {
            "access_token": response["access_token"],
            "refresh_token": response["refresh_token"],
            "user_id": response["user_id"],
            "expires_in": response["expires_in"],
        }

    except Exception as e:
        print(f"Sign in failed: {e}")
        return None


def make_recommendation_request(
    token_data: TokenData,
    project_id: str,
    sequence_data: dict,
    template: str,
    use_case_name: str
):
    """Make recommendation request with given parameters"""
    url = os.getenv("RECOMMEND_URL").rstrip("/")

    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {token_data['access_token']}",
    }

    payload = {
        "sequence_data": sequence_data,
        "template": template,
    }

    try:
        print(f"\n=== Testing {use_case_name} ===")
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
        print(f"Request failed for {use_case_name}: {e}")
        return None


# Product Recommendation Use Cases

def test_customers_also_bought(token_data: TokenData, project_id: str):
    """Test 'Customers Also Bought' Recommendations"""
    sequence_data = {
        "current_product": "laptop",
        "product_category": "electronics",
        "price_range": "medium"
    }
    template = "Recommend products frequently bought together with {current_product} in {product_category} category"
    return make_recommendation_request(
        token_data, project_id, sequence_data, template, 
        "Customers Also Bought"
    )


def test_frequently_bought_together(token_data: TokenData, project_id: str):
    """Test 'Frequently Bought Together' Bundles"""
    sequence_data = {
        "current_product": "smartphone",
        "related_products": ["phone_case", "screen_protector"],
        "bundle_savings": 15.0
    }
    template = "Suggest product bundles that include {current_product} with {related_products}, offering {bundle_savings}% savings"
    return make_recommendation_request(
        token_data, project_id, sequence_data, template,
        "Frequently Bought Together"
    )


def test_you_might_also_like(token_data: TokenData, project_id: str):
    """Test 'You Might Also Like' Personalized Suggestions"""
    sequence_data = {
        "previous_purchases": ["electronics", "books", "home_garden"],
        "user_preferences": ["technology", "reading", "cooking"],
        "browsing_history": ["laptops", "novels", "kitchen_appliances"]
    }
    template = "Based on your interest in {user_preferences} and previous purchases of {previous_purchases}, recommend similar products"
    return make_recommendation_request(
        token_data, project_id, sequence_data, template,
        "You Might Also Like"
    )


def test_because_you_viewed(token_data: TokenData, project_id: str):
    """Test 'Because You Viewed' Session-based Recommendations"""
    sequence_data = {
        "current_session_views": ["running_shoes", "sports_watch", "fitness_tracker"],
        "session_duration": "15_minutes",
        "view_time": "evening"
    }
    template = "Since you viewed {current_session_views} in the {view_time}, recommend related products for your active session"
    return make_recommendation_request(
        token_data, project_id, sequence_data, template,
        "Because You Viewed"
    )


def test_trending_products(token_data: TokenData, project_id: str):
    """Test 'Trending Products' Popularity-based Recommendations"""
    sequence_data = {
        "user_segment": "young_professionals",
        "time_period": "last_7_days",
        "trending_categories": ["electronics", "fashion", "home"]
    }
    template = "Show trending products in {trending_categories} for {user_segment} from {time_period}"
    return make_recommendation_request(
        token_data, project_id, sequence_data, template,
        "Trending Products"
    )


def test_complete_collection(token_data: TokenData, project_id: str):
    """Test 'Complete Your Collection' Category Recommendations"""
    sequence_data = {
        "owned_products": ["iphone_13", "airpods_pro"],
        "product_ecosystem": "apple",
        "missing_items": ["macbook", "ipad", "apple_watch"]
    }
    template = "Help complete your {product_ecosystem} collection. You already have {owned_products}, consider {missing_items}"
    return make_recommendation_request(
        token_data, project_id, sequence_data, template,
        "Complete Your Collection"
    )


def test_price_range_alternatives(token_data: TokenData, project_id: str):
    """Test 'Price Range' Alternative Recommendations"""
    sequence_data = {
        "viewed_product": "premium_laptop",
        "viewed_price": 2000.0,
        "budget_range": "under_1000",
        "preferred_features": ["fast_processor", "good_battery", "lightweight"]
    }
    template = "You viewed {viewed_product} at ${viewed_price}. Here are alternatives under $1000 with {preferred_features}"
    return make_recommendation_request(
        token_data, project_id, sequence_data, template,
        "Price Range Alternatives"
    )


def test_new_arrivals(token_data: TokenData, project_id: str):
    """Test 'New Arrivals' Fresh Content Recommendations"""
    sequence_data = {
        "user_interests": ["technology", "fitness", "outdoor"],
        "new_categories": ["smart_home", "wearables", "camping_gear"],
        "launch_period": "last_30_days"
    }
    template = "Discover new arrivals in {new_categories} from {launch_period} based on your interest in {user_interests}"
    return make_recommendation_request(
        token_data, project_id, sequence_data, template,
        "New Arrivals"
    )


# Personalized Search Use Cases

def test_personalized_result_ranking(token_data: TokenData, project_id: str):
    """Test Personalized Result Ranking"""
    sequence_data = {
        "search_query": "laptop",
        "user_history": ["electronics", "computers", "gaming"],
        "purchase_history": ["dell_xps", "macbook_pro"],
        "price_sensitivity": "medium"
    }
    template = "Rank search results for '{search_query}' based on user's history with {user_history} and purchases of {purchase_history}"
    return make_recommendation_request(
        token_data, project_id, sequence_data, template,
        "Personalized Result Ranking"
    )


def test_query_autocompletion(token_data: TokenData, project_id: str):
    """Test Query Auto-completion with Personalization"""
    sequence_data = {
        "partial_query": "lap",
        "previous_searches": ["laptop", "laptop stand", "laptop bag"],
        "user_category_preference": "electronics"
    }
    template = "Complete the query '{partial_query}' based on previous searches like {previous_searches} and interest in {user_category_preference}"
    return make_recommendation_request(
        token_data, project_id, sequence_data, template,
        "Query Auto-completion"
    )


def test_did_you_mean_corrections(token_data: TokenData, project_id: str):
    """Test 'Did You Mean' Personalized Corrections"""
    sequence_data = {
        "misspelled_query": "laptap",
        "user_vocabulary": ["laptop", "tablet", "notebook"],
        "common_typos": ["laptap", "labtop", "laptopp"]
    }
    template = "Correct '{misspelled_query}' based on user's vocabulary {user_vocabulary} and common typos {common_typos}"
    return make_recommendation_request(
        token_data, project_id, sequence_data, template,
        "Did You Mean Corrections"
    )


def test_category_aware_search(token_data: TokenData, project_id: str):
    """Test Category-aware Search"""
    sequence_data = {
        "search_query": "gift",
        "preferred_categories": ["electronics", "books", "home"],
        "avoid_categories": ["clothing", "beauty"],
        "season": "holiday"
    }
    template = "For '{search_query}' search, prioritize results from {preferred_categories} and avoid {avoid_categories} for {season} season"
    return make_recommendation_request(
        token_data, project_id, sequence_data, template,
        "Category-aware Search"
    )


def test_price_sensitive_search(token_data: TokenData, project_id: str):
    """Test Price-sensitive Search Results"""
    sequence_data = {
        "search_query": "headphones",
        "typical_price_range": "50-100",
        "price_sensitivity": "high",
        "value_preferences": ["durability", "sound_quality"]
    }
    template = "Search for '{search_query}' in ${typical_price_range} range, focusing on {value_preferences} for price-sensitive user"
    return make_recommendation_request(
        token_data, project_id, sequence_data, template,
        "Price-sensitive Search"
    )


def test_brand_preference_integration(token_data: TokenData, project_id: str):
    """Test Brand Preference Integration"""
    sequence_data = {
        "search_query": "smartphone",
        "preferred_brands": ["apple", "samsung"],
        "avoid_brands": ["unknown_brands"],
        "brand_loyalty": "high"
    }
    template = "For '{search_query}' search, boost results from {preferred_brands} and avoid {avoid_brands} for brand-loyal user"
    return make_recommendation_request(
        token_data, project_id, sequence_data, template,
        "Brand Preference Integration"
    )


def test_visual_similarity_search(token_data: TokenData, project_id: str):
    """Test Visual Similarity Search"""
    sequence_data = {
        "viewed_product_image": "red_running_shoes.jpg",
        "visual_features": ["red_color", "athletic_style", "mesh_material"],
        "similar_attributes": ["comfort", "breathability", "durability"]
    }
    template = "Find products visually similar to {viewed_product_image} with features like {visual_features} and attributes {similar_attributes}"
    return make_recommendation_request(
        token_data, project_id, sequence_data, template,
        "Visual Similarity Search"
    )


def test_context_aware_search(token_data: TokenData, project_id: str):
    """Test Context-aware Search"""
    sequence_data = {
        "search_query": "restaurant",
        "current_time": "evening",
        "user_location": "downtown",
        "device_type": "mobile",
        "weather": "rainy"
    }
    template = "Search for '{search_query}' in {user_location} during {current_time} on {device_type}, considering {weather} weather"
    return make_recommendation_request(
        token_data, project_id, sequence_data, template,
        "Context-aware Search"
    )


def run_all_tests(token_data: TokenData, project_id: str):
    """Run all e-commerce use case tests"""
    print("=" * 80)
    print("RUNNING ALL E-COMMERCE RECOMMENDATION USE CASE TESTS")
    print("=" * 80)

    # Product Recommendation Tests
    print("\n📦 PRODUCT RECOMMENDATION TESTS")
    print("-" * 50)
    
    test_customers_also_bought(token_data, project_id)
    test_frequently_bought_together(token_data, project_id)
    test_you_might_also_like(token_data, project_id)
    test_because_you_viewed(token_data, project_id)
    test_trending_products(token_data, project_id)
    test_complete_collection(token_data, project_id)
    test_price_range_alternatives(token_data, project_id)
    test_new_arrivals(token_data, project_id)

    # Personalized Search Tests
    print("\n🔍 PERSONALIZED SEARCH TESTS")
    print("-" * 50)
    
    test_personalized_result_ranking(token_data, project_id)
    test_query_autocompletion(token_data, project_id)
    test_did_you_mean_corrections(token_data, project_id)
    test_category_aware_search(token_data, project_id)
    test_price_sensitive_search(token_data, project_id)
    test_brand_preference_integration(token_data, project_id)
    test_visual_similarity_search(token_data, project_id)
    test_context_aware_search(token_data, project_id)

    print("\n" + "=" * 80)
    print("ALL TESTS COMPLETED")
    print("=" * 80)


if __name__ == "__main__":
    email = "dat.ngo3246@gmail.com"
    password = "password"
    project_id = os.getenv(
        "PROJECT_ID",
        "698cb6e723c249dbb3c5f766",
    )

    # Get JWT token
    token_data = get_jwt_token(email, password)

    # Verify project access
    url = os.getenv("ADMIN_URL").rstrip("/")
    headers = {
        "Authorization": f"Bearer {token_data['access_token']}",
    }
    try:
        response = requests.get(
            f"{url}/api/projects/get",
            headers=headers,
            params={
                "user_id": token_data["user_id"],
                "project_id": project_id,
            },
        )
        response.raise_for_status()
        print("Project access verified!")
    except requests.exceptions.HTTPError as e:
        print(f"HTTP Error: {e}")
        print(f"Status Code: {response.status_code}")
        print(f"Response Body: {response.text}")
        raise

    if token_data:
        # Run all use case tests
        run_all_tests(token_data, project_id)
