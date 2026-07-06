import pytest
from copy import deepcopy
from fastapi.testclient import TestClient
from src import app as app_module
from src.app import app


@pytest.fixture
def sample_activities():
    """Fixture providing sample activities data for tests."""
    return {
        "Chess Club": {
            "description": "Learn strategies and compete in chess tournaments",
            "schedule": "Fridays, 3:30 PM - 5:00 PM",
            "max_participants": 12,
            "participants": ["michael@mergington.edu", "daniel@mergington.edu"]
        },
        "Programming Class": {
            "description": "Learn programming fundamentals and build software projects",
            "schedule": "Tuesdays and Thursdays, 3:30 PM - 4:30 PM",
            "max_participants": 20,
            "participants": ["emma@mergington.edu", "sophia@mergington.edu"]
        },
        "Gym Class": {
            "description": "Physical education and sports activities",
            "schedule": "Mondays, Wednesdays, Fridays, 2:00 PM - 3:00 PM",
            "max_participants": 30,
            "participants": ["john@mergington.edu", "olivia@mergington.edu"]
        },
        "Basketball Team": {
            "description": "Team practices and inter-school competitions",
            "schedule": "Mondays, Wednesdays, Fridays, 4:00 PM - 6:00 PM",
            "max_participants": 15,
            "participants": ["alex@mergington.edu"]
        },
        "Swimming Club": {
            "description": "Swim training and technique improvement",
            "schedule": "Tuesdays and Thursdays, 5:00 PM - 6:30 PM",
            "max_participants": 20,
            "participants": ["nora@mergington.edu"]
        },
        "Drama Club": {
            "description": "Acting, stagecraft, and school productions",
            "schedule": "Wednesdays, 3:30 PM - 5:30 PM",
            "max_participants": 25,
            "participants": ["liam@mergington.edu"]
        },
        "Art Workshop": {
            "description": "Painting, drawing, and mixed media projects",
            "schedule": "Fridays, 3:30 PM - 5:00 PM",
            "max_participants": 18,
            "participants": ["ava@mergington.edu"]
        },
        "Science Olympiad": {
            "description": "Hands-on science challenges and competition prep",
            "schedule": "Thursdays, 3:30 PM - 5:00 PM",
            "max_participants": 20,
            "participants": ["noah@mergington.edu"]
        },
        "Debate Team": {
            "description": "Competitive debate practice and tournaments",
            "schedule": "Tuesdays, 4:00 PM - 5:30 PM",
            "max_participants": 16,
            "participants": ["sophia@mergington.edu"]
        }
    }


@pytest.fixture
def client(sample_activities):
    """Fixture providing a TestClient with isolated activities data for each test."""
    # Clear and reset activities for this test to ensure isolation
    app_module.activities.clear()
    app_module.activities.update(deepcopy(sample_activities))
    return TestClient(app)
