#!/bin/bash

# Test 'Because You Viewed' Session-based Recommendations using curl
# Based on test_because_you_viewed.py

# Set your API key here or export as environment variable
API_KEY="${API_KEY:-YOUR_API_KEY_HERE}"
RECOMMEND_URL="${RECOMMEND_URL:-https://api.trydodo.xyz}"

if [ "$API_KEY" = "YOUR_API_KEY_HERE" ]; then
    echo "Please set your API_KEY environment variable"
    echo "Example: export API_KEY=your_actual_api_key"
    exit 1
fi

echo "=== Testing Because You Viewed ==="
echo "Using API key: $API_KEY"
echo "Recommend URL: $RECOMMEND_URL"
echo

# Prepare the JSON payload
PAYLOAD='{
    "context": {
        "current_session_views": [
            "smartphone_001",
            "laptop_001", 
            "headphones_001"
        ],
        "session_duration": "15_minutes",
        "view_time": "evening",
        "user_preferences": {
            "preferred_brands": ["TechCorp", "AudioPro", "TechBrand"],
            "price_sensitivity": "medium",
            "desired_categories": ["electronics"]
        }
    },
    "template": "Since you viewed {current_session_views} in {view_time} for {session_duration}, recommend related products considering your preferences: {user_preferences}. Focus on complementary items to your viewed products.",
    "catalog": {
        "8": {"product_name": "MacBook Pro", "price": 1999, "category": "electronics"},
        "4": {"product_name": "iPad Air", "price": 599, "category": "electronics"},
        "1": {"product_name": "iPhone 16", "price": 999, "category": "electronics"},
        "3": {"product_name": "AirPods Pro", "price": 249, "category": "electronics"},
        "5": {"product_name": "Apple Watch", "price": 399, "category": "electronics"},
        "6": {"product_name": "Magic Keyboard", "price": 149, "category": "electronics"},
        "9": {"product_name": "Magic Mouse", "price": 99, "category": "electronics"},
        "7": {"product_name": "Magic Trackpad", "price": 129, "category": "electronics"},
        "2": {"product_name": "Apple Pencil", "price": 129, "category": "electronics"},
        "10": {"product_name": "USB-C Charge Cable", "price": 19, "category": "accessories"}
    }
}'

echo "Request payload:"
echo "$PAYLOAD" | jq .
echo

# Make the curl request
curl -X POST \
    "${RECOMMEND_URL}/api/recommend/recommend?model_key=${MODEL_KEY}&user_id=${USER_ID}&num_results=${NUM_RESULTS}" \
    -H "Content-Type: application/json" \
    -H "Authorization: Bearer ${API_KEY}" \
    -G \
    --data-raw "$PAYLOAD"

echo
echo "Request completed."
