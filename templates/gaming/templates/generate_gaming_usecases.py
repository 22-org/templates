"""
Script to generate all gaming use case test files
"""

import os

# Define all gaming use cases with their data
gaming_use_cases = [
    {
        "filename": "test_social_connection_suggestions.py",
        "title": "Social Connection Suggestions",
        "description": "Recommend friends, guilds, and team members",
        "sequence_data": {
            "play_patterns": ["team_player", "strategic_gameplay"],
            "skill_level": "advanced",
            "social_connections": ["existing_friends", "guild_members"],
            "preferences": ["cooperative_play", "competitive_teams"],
            "play_schedule": "evening_player"
        },
        "template": (
            "Suggest {preferences} connections for {skill_level} {play_schedule} player "
            "with {play_patterns} and existing {social_connections}"
        )
    },
    {
        "filename": "test_personalized_challenges_quests.py",
        "title": "Personalized Challenges and Quests",
        "description": "Generate personalized challenges based on player skill",
        "sequence_data": {
            "skill_level": "expert",
            "play_history": ["completionist", "speed_runner"],
            "preferences": ["puzzle_challenges", "boss_battles"],
            "completion_patterns": {"daily": "high", "weekly": "medium"},
            "difficulty_preference": "challenging"
        },
        "template": (
            "Generate {difficulty_preference} quests for {skill_level} player with "
            "{play_history} style who prefers {preferences} and has {completion_patterns} patterns"
        )
    },
    {
        "filename": "test_game_discovery_recommendations.py",
        "title": "Game Discovery Recommendations",
        "description": "Suggest new games based on playing preferences",
        "sequence_data": {
            "game_library": ["rpg_games", "strategy_titles", "indie_games"],
            "play_time": {"casual": "high", "hardcore": "medium"},
            "genre_preferences": ["role_playing", "strategy", "puzzle"],
            "ratings": ["4_plus_stars", "community_favorite"],
            "platform": "multi_platform"
        },
        "template": (
            "Recommend games with {ratings} on {platform} for player who enjoys "
            "{genre_preferences} with {play_time} patterns from {game_library}"
        )
    },
    {
        "filename": "test_tutorial_help_content.py",
        "title": "Tutorial and Help Content",
        "description": "Personalized tutorials and help based on player needs",
        "sequence_data": {
            "skill_level": "beginner",
            "common_mistakes": ["controls", "strategy_basics"],
            "learning_patterns": ["visual_learner", "hands_on"],
            "progress": {"tutorial_completion": "low", "skill_growth": "high"},
            "help_needs": ["game_mechanics", "advanced_techniques"]
        },
        "template": (
            "Provide {help_needs} tutorials for {skill_level} {learning_patterns} "
            "with {common_mistakes} challenges and {progress} progress"
        )
    },
    {
        "filename": "test_event_tournament_recommendations.py",
        "title": "Event and Tournament Recommendations",
        "description": "Suggest relevant events and tournaments",
        "sequence_data": {
            "skill_level": "competitive",
            "play_schedule": ["weekend_warrior", "evening_player"],
            "competitive_history": ["tournament_participant", "team_leader"],
            "preferences": ["solo_competition", "team_events"],
            "time_commitment": "moderate"
        },
        "template": (
            "Suggest {preferences} events for {skill_level} {time_commitment} player "
            "with {competitive_history} during {play_schedule} times"
        )
    },
    {
        "filename": "test_monetization_personalization.py",
        "title": "Monetization Personalization",
        "description": "Personalized offers and in-game purchase suggestions",
        "sequence_data": {
            "purchase_history": ["cosmetic_items", "battle_passes"],
            "spending_patterns": {"monthly": "moderate", "seasonal": "high"},
            "player_value": "whale_potential",
            "preferences": ["value_offers", "exclusive_content"],
            "engagement": "highly_engaged"
        },
        "template": (
            "Create {preferences} offers for {engagement} {player_value} player with "
            "{spending_patterns} and {purchase_history} background"
        )
    },
    {
        "filename": "test_play_style_adaptation.py",
        "title": "Play Style Adaptation",
        "description": "Adapt game difficulty and content to play style",
        "sequence_data": {
            "play_patterns": ["explorer", "completionist"],
            "skill_metrics": {"reaction_time": "fast", "strategy": "high"},
            "preferences": ["open_world", "story_driven"],
            "engagement_data": {"session_length": "long", "frequency": "daily"},
            "adaptation_needs": "dynamic_difficulty"
        },
        "template": (
            "Adapt {adaptation_needs} for player with {play_patterns} style, "
            "{skill_metrics} and {preferences} in {engagement_data} sessions"
        )
    },
    {
        "filename": "test_cross_platform_recommendations.py",
        "title": "Cross-Platform Recommendations",
        "description": "Suggest content across different gaming platforms",
        "sequence_data": {
            "cross_platform_behavior": ["mobile_casual", "pc_hardcore"],
            "platform_preferences": ["console_primary", "mobile_secondary"],
            "play_history": ["multiplatform_gamer", "cross_progress"],
            "device_capabilities": ["high_end_pc", "latest_console"],
            "sync_preferences": "cloud_sync_enabled"
        },
        "template": (
            "Recommend cross-platform content for {cross_platform_behavior} gamer "
            "with {platform_preferences} and {device_capabilities} setup"
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
output_dir = "/Users/ericngo/Desktop/projects/templates/industry-templates/gaming/templates"

for use_case in gaming_use_cases:
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

print("\\nAll gaming use case test files generated successfully!")
