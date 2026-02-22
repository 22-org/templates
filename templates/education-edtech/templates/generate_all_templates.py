"""
Script to generate all education-edtech template files
"""

import os

# Template definitions
templates = [
    {
        "filename": "test_career_path_recommendations.py",
        "description": "Career Path Recommendations",
        "docstring": "Suggest courses and skills for career development",
        "sequence_data": {
            "career_goal": "data_scientist",
            "current_skills": ["python", "statistics"],
            "industry": "technology",
            "experience_level": "entry_level",
            "time_horizon": "6_months",
        },
        "template": (
            "Recommend career path for {career_goal} in {industry} with current "
            "skills {current_skills} at {experience_level} within {time_horizon}"
        ),
    },
    {
        "filename": "test_personalized_assessments.py",
        "description": "Personalized Assessments",
        "docstring": "Adaptive assessments that adjust to student level",
        "sequence_data": {
            "subject": "mathematics",
            "current_level": "intermediate",
            "assessment_type": "formative",
            "time_limit": 30,
            "adaptive_mode": "enabled",
        },
        "template": (
            "Create {assessment_type} assessment for {subject} at {current_level} "
            "level with {time_limit} minutes and {adaptive_mode} adaptation"
        ),
    },
    {
        "filename": "test_learning_style_adaptation.py",
        "description": "Learning Style Adaptation",
        "docstring": "Adapt content delivery to individual learning styles",
        "sequence_data": {
            "learning_style": "visual",
            "content_type": "video",
            "subject": "biology",
            "complexity": "medium",
            "interaction_preference": "interactive",
        },
        "template": (
            "Adapt {content_type} content for {learning_style} learners studying "
            "{subject} at {complexity} complexity with {interaction_preference} "
            "interaction"
        ),
    },
    {
        "filename": "test_prerequisites_dependencies.py",
        "description": "Prerequisites and Dependencies",
        "docstring": "Recommend prerequisite courses and learning dependencies",
        "sequence_data": {
            "target_course": "machine_learning",
            "current_knowledge": ["basic_programming", "statistics"],
            "learning_goal": "advanced",
            "time_available": "3_months",
            "preferred_format": "online",
        },
        "template": (
            "Identify prerequisites for {target_course} given current knowledge "
            "{current_knowledge} for {learning_goal} goal within {time_available} "
            "using {preferred_format} format"
        ),
    },
    {
        "filename": "test_motivation_engagement_strategies.py",
        "description": "Motivation and Engagement Strategies",
        "docstring": "Personalized motivation strategies and gamification",
        "sequence_data": {
            "student_profile": "competitive",
            "motivation_type": "achievement",
            "engagement_preference": "gamification",
            "subject": "mathematics",
            "age_group": "teenagers",
        },
        "template": (
            "Design {engagement_preference} strategies for {motivation_type} "
            "motivated {student_profile} students learning {subject} in {age_group} "
            "age group"
        ),
    },
    {
        "filename": "test_personalized_content_search.py",
        "description": "Personalized Content Search",
        "docstring": "Search results ranked based on learning preferences and level",
        "sequence_data": {
            "search_query": "calculus basics",
            "learning_level": "beginner",
            "content_preference": "video",
            "language": "english",
            "duration_preference": "short",
        },
        "template": (
            "Search for {search_query} at {learning_level} level with {content_preference} "
            "content in {language} language with {duration_preference} duration"
        ),
    },
    {
        "filename": "test_skill_based_content_recommendations.py",
        "description": "Skill-based Content Recommendations",
        "docstring": "Recommend content based on specific skill development needs",
        "sequence_data": {
            "target_skill": "data_analysis",
            "current_skill_level": "beginner",
            "desired_level": "intermediate",
            "learning_context": "professional",
            "time_commitment": "2_hours_per_week",
        },
        "template": (
            "Recommend content to develop {target_skill} from {current_skill_level} "
            "to {desired_level} for {learning_context} context with "
            "{time_commitment} commitment"
        ),
    },
    {
        "filename": "test_learning_resource_discovery.py",
        "description": "Learning Resource Discovery",
        "docstring": "Discover relevant learning resources across platforms",
        "sequence_data": {
            "topic": "python_programming",
            "resource_types": ["tutorial", "course", "book"],
            "difficulty": "beginner",
            "platforms": ["coursera", "youtube", "udemy"],
            "free_preference": "yes",
        },
        "template": (
            "Discover {resource_types} resources for {topic} at {difficulty} level "
            "on {platforms} platforms with {free_preference} free preference"
        ),
    },
]

# Base template code
base_template = '''"""
Test Case: {description}
{docstring}
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
            f"{url}/api/projects/create",
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


def {function_name}(token_data: TokenData, project_id: str):
    """Test {description}"""
    url = os.getenv("DODO_URL").rstrip("/")

    headers = {{
        "Content-Type": "application/json",
        "Authorization": f"Bearer {{token_data['access_token']}}",
    }}

    sequence_data = {sequence_data}

    template = (
        "{template_string}"
    )

    payload = {{"sequence_data": sequence_data, "template": template}}

    try:
        print("=== Testing {description} ===")
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
            print(f"Results: {{result}}")
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
        name="{test_name}",
        description="Test project for {description_lower}",
    )

    # Make recommendations
    {function_name}(token_data, project_id)
'''


def generate_template_files():
    """Generate all template files"""
    for template_info in templates:
        filename = template_info["filename"]
        description = template_info["description"]
        docstring = template_info["docstring"]
        sequence_data = template_info["sequence_data"]
        template_string = template_info["template"]

        # Generate function name from filename
        function_name = filename.replace("test_", "").replace(".py", "")

        # Generate test name
        test_name = description.replace(" ", " ") + " Test"

        # Generate description lower
        description_lower = description.lower().replace(" ", " ")

        # Format the template
        content = base_template.format(
            description=description,
            docstring=docstring,
            function_name=function_name,
            sequence_data=sequence_data,
            template_string=template_string,
            test_name=test_name,
            description_lower=description_lower,
        )

        # Write file
        filepath = os.path.join(os.path.dirname(__file__), filename)
        with open(filepath, "w") as f:
            f.write(content)

        print(f"Generated {filename}")


if __name__ == "__main__":
    generate_template_files()
