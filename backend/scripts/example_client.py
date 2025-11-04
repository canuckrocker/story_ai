"""
Story AI - Example Client
Simple Python client demonstrating how to interact with the Story AI API
"""
import requests
import json
from typing import Dict, List

BASE_URL = "http://localhost:8000/api/v1"


class StoryAIClient:
    def __init__(self, base_url: str = BASE_URL):
        self.base_url = base_url

    def create_user(self, name: str, email: str, phone: str = None) -> Dict:
        """Create a new user"""
        response = requests.post(
            f"{self.base_url}/users",
            json={"name": name, "email": email, "phone_number": phone}
        )
        response.raise_for_status()
        return response.json()

    def create_branch(self, user_id: int, branch_type: str, title: str, description: str = None) -> Dict:
        """Create a memory branch"""
        response = requests.post(
            f"{self.base_url}/branches",
            json={
                "user_id": user_id,
                "branch_type": branch_type,
                "title": title,
                "description": description
            }
        )
        response.raise_for_status()
        return response.json()

    def submit_text_input(self, user_id: int, text: str, branch_id: int = None) -> Dict:
        """Submit a text input"""
        response = requests.post(
            f"{self.base_url}/inputs",
            json={
                "user_id": user_id,
                "input_type": "text",
                "raw_text": text,
                "memory_branch_id": branch_id
            }
        )
        response.raise_for_status()
        return response.json()

    def generate_story(self, user_id: int, input_ids: List[int], branch_id: int = None, style: str = "narrative") -> Dict:
        """Generate a story from inputs"""
        response = requests.post(
            f"{self.base_url}/stories/generate",
            json={
                "user_id": user_id,
                "input_ids": input_ids,
                "memory_branch_id": branch_id,
                "style": style
            }
        )
        response.raise_for_status()
        return response.json()

    def get_user_stories(self, user_id: int) -> List[Dict]:
        """Get all stories for a user"""
        response = requests.get(f"{self.base_url}/stories/user/{user_id}")
        response.raise_for_status()
        return response.json()

    def get_user_branches(self, user_id: int) -> List[Dict]:
        """Get all branches for a user"""
        response = requests.get(f"{self.base_url}/branches/user/{user_id}")
        response.raise_for_status()
        return response.json()


def demo():
    """Run a complete demo of the Story AI workflow"""
    client = StoryAIClient()

    print("🎬 Story AI Demo")
    print("=" * 50)

    # 1. Create a user
    print("\n1️⃣  Creating user...")
    user = client.create_user(
        name="Demo Grandparent",
        email="demo@storyai.com",
        phone="+1555123456"
    )
    print(f"   ✓ Created user: {user['name']} (ID: {user['id']})")

    # 2. Create memory branches
    print("\n2️⃣  Creating memory branches...")
    branches = []
    branch_configs = [
        ("childhood", "Growing Up", "Memories from my childhood"),
        ("adventures", "Life Adventures", "Exciting moments and travels"),
        ("grateful", "Things I'm Grateful For", "Moments of gratitude")
    ]

    for branch_type, title, desc in branch_configs:
        branch = client.create_branch(user['id'], branch_type, title, desc)
        branches.append(branch)
        print(f"   ✓ Created branch: {title}")

    # 3. Submit story inputs
    print("\n3️⃣  Submitting story inputs...")
    inputs = []

    story_texts = [
        "I remember when I was 8 years old, we lived in a small town. Every summer, my siblings and I would run through the fields behind our house, catching fireflies in mason jars.",
        "My mother taught me how to bake bread from scratch. The smell of fresh bread still brings me back to those Saturday mornings in her kitchen.",
        "When I was young, we didn't have much money, but we had each other. Those were some of the happiest times of my life."
    ]

    for text in story_texts:
        inp = client.submit_text_input(
            user['id'],
            text,
            branches[0]['id']  # childhood branch
        )
        inputs.append(inp)
        print(f"   ✓ Submitted input (ID: {inp['id']})")

    # 4. Generate AI story
    print("\n4️⃣  Generating AI story from inputs...")
    story = client.generate_story(
        user['id'],
        [inp['id'] for inp in inputs],
        branches[0]['id'],
        style="narrative"
    )
    print(f"   ✓ Generated story: {story['title']}")
    print(f"\n📖 Story Preview:")
    print(f"   {story['content'][:200]}...")

    # 5. Get all user stories
    print("\n5️⃣  Fetching all user stories...")
    all_stories = client.get_user_stories(user['id'])
    print(f"   ✓ Found {len(all_stories)} stories")

    # 6. Get all user branches
    print("\n6️⃣  Fetching all memory branches...")
    all_branches = client.get_user_branches(user['id'])
    print(f"   ✓ Found {len(all_branches)} branches:")
    for branch in all_branches:
        print(f"      • {branch['title']} ({branch['branch_type']})")

    print("\n" + "=" * 50)
    print("✨ Demo complete! Check http://localhost:8000/docs for more.")


if __name__ == "__main__":
    try:
        demo()
    except requests.exceptions.ConnectionError:
        print("❌ Error: Could not connect to API")
        print("   Make sure the server is running: uvicorn app.main:app")
    except Exception as e:
        print(f"❌ Error: {e}")
