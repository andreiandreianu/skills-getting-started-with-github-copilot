"""
FastAPI tests for Mergington High School Activities API.

Tests cover:
- GET /activities endpoint
- POST /activities/{activity_name}/signup endpoint
- DELETE /activities/{activity_name}/signup endpoint
"""

import pytest


class TestGetActivities:
    """Tests for GET /activities endpoint."""

    def test_get_activities_returns_all_activities(self, client):
        """Test that GET /activities returns all activities."""
        response = client.get("/activities")
        assert response.status_code == 200
        data = response.json()
        assert len(data) == 9
        assert "Chess Club" in data
        assert "Programming Class" in data
        assert "Gym Class" in data
        assert "Basketball Team" in data
        assert "Swimming Club" in data
        assert "Drama Club" in data
        assert "Art Workshop" in data
        assert "Science Olympiad" in data
        assert "Debate Team" in data

    def test_get_activities_returns_correct_structure(self, client):
        """Test that each activity has required fields."""
        response = client.get("/activities")
        data = response.json()
        activity = data["Chess Club"]
        
        assert "description" in activity
        assert "schedule" in activity
        assert "max_participants" in activity
        assert "participants" in activity

    def test_get_activities_participant_counts_correct(self, client):
        """Test that participant counts are accurate."""
        response = client.get("/activities")
        data = response.json()
        
        assert len(data["Chess Club"]["participants"]) == 2
        assert len(data["Programming Class"]["participants"]) == 2
        assert len(data["Gym Class"]["participants"]) == 2

    def test_get_activities_max_participants_correct(self, client):
        """Test that max_participants values are correct."""
        response = client.get("/activities")
        data = response.json()
        
        assert data["Chess Club"]["max_participants"] == 12
        assert data["Programming Class"]["max_participants"] == 20
        assert data["Gym Class"]["max_participants"] == 30


class TestSignup:
    """Tests for POST /activities/{activity_name}/signup endpoint."""

    def test_signup_successful(self, client):
        """Test successful signup returns 200 and correct message."""
        response = client.post(
            "/activities/Chess Club/signup",
            params={"email": "newstudent@mergington.edu"}
        )
        assert response.status_code == 200
        assert "Signed up newstudent@mergington.edu for Chess Club" in response.json()["message"]

    def test_signup_adds_participant_to_list(self, client):
        """Test that signup adds participant to the activity's participant list."""
        client.post(
            "/activities/Chess Club/signup",
            params={"email": "newstudent@mergington.edu"}
        )
        
        response = client.get("/activities")
        data = response.json()
        assert "newstudent@mergington.edu" in data["Chess Club"]["participants"]
        assert len(data["Chess Club"]["participants"]) == 3

    def test_signup_duplicate_returns_error(self, client):
        """Test that signing up twice for same activity returns 400 error."""
        # First signup should succeed
        response1 = client.post(
            "/activities/Chess Club/signup",
            params={"email": "duplicate@mergington.edu"}
        )
        assert response1.status_code == 200
        
        # Second signup should fail
        response2 = client.post(
            "/activities/Chess Club/signup",
            params={"email": "duplicate@mergington.edu"}
        )
        assert response2.status_code == 400
        assert "already signed up" in response2.json()["detail"]

    def test_signup_nonexistent_activity_returns_404(self, client):
        """Test that signup for non-existent activity returns 404."""
        response = client.post(
            "/activities/Nonexistent Activity/signup",
            params={"email": "student@mergington.edu"}
        )
        assert response.status_code == 404
        assert "Activity not found" in response.json()["detail"]

    def test_signup_multiple_different_students(self, client):
        """Test that multiple different students can sign up for same activity."""
        email1 = "student1@mergington.edu"
        email2 = "student2@mergington.edu"
        
        response1 = client.post(
            "/activities/Chess Club/signup",
            params={"email": email1}
        )
        response2 = client.post(
            "/activities/Chess Club/signup",
            params={"email": email2}
        )
        
        assert response1.status_code == 200
        assert response2.status_code == 200
        
        data = client.get("/activities").json()
        assert email1 in data["Chess Club"]["participants"]
        assert email2 in data["Chess Club"]["participants"]
        assert len(data["Chess Club"]["participants"]) == 4  # 2 initial + 2 new

    def test_signup_works_for_different_activities(self, client):
        """Test that same student can signup for multiple activities."""
        email = "student@mergington.edu"
        
        response1 = client.post(
            "/activities/Chess Club/signup",
            params={"email": email}
        )
        response2 = client.post(
            "/activities/Programming Class/signup",
            params={"email": email}
        )
        
        assert response1.status_code == 200
        assert response2.status_code == 200
        
        data = client.get("/activities").json()
        assert email in data["Chess Club"]["participants"]
        assert email in data["Programming Class"]["participants"]


class TestUnregister:
    """Tests for DELETE /activities/{activity_name}/signup endpoint."""

    def test_unregister_successful(self, client):
        """Test successful unregister returns 200 and correct message."""
        response = client.delete(
            "/activities/Chess Club/signup",
            params={"email": "michael@mergington.edu"}
        )
        assert response.status_code == 200
        assert "Unregistered michael@mergington.edu from Chess Club" in response.json()["message"]

    def test_unregister_removes_participant_from_list(self, client):
        """Test that unregister removes participant from activity."""
        client.delete(
            "/activities/Chess Club/signup",
            params={"email": "michael@mergington.edu"}
        )
        
        response = client.get("/activities")
        data = response.json()
        assert "michael@mergington.edu" not in data["Chess Club"]["participants"]
        assert len(data["Chess Club"]["participants"]) == 1

    def test_unregister_nonexistent_participant_returns_404(self, client):
        """Test that unregistering non-existent participant returns 404."""
        response = client.delete(
            "/activities/Chess Club/signup",
            params={"email": "notregistered@mergington.edu"}
        )
        assert response.status_code == 404
        assert "not registered" in response.json()["detail"]

    def test_unregister_nonexistent_activity_returns_404(self, client):
        """Test that unregistering from non-existent activity returns 404."""
        response = client.delete(
            "/activities/Nonexistent Activity/signup",
            params={"email": "student@mergington.edu"}
        )
        assert response.status_code == 404
        assert "Activity not found" in response.json()["detail"]

    def test_unregister_all_participants_leaves_empty_list(self, client):
        """Test that unregistering all participants leaves empty list."""
        # Unregister both participants
        client.delete(
            "/activities/Chess Club/signup",
            params={"email": "michael@mergington.edu"}
        )
        client.delete(
            "/activities/Chess Club/signup",
            params={"email": "daniel@mergington.edu"}
        )
        
        data = client.get("/activities").json()
        assert data["Chess Club"]["participants"] == []

    def test_unregister_multiple_times_fails_on_second(self, client):
        """Test that trying to unregister same participant twice fails."""
        # First unregister should succeed
        response1 = client.delete(
            "/activities/Chess Club/signup",
            params={"email": "michael@mergington.edu"}
        )
        assert response1.status_code == 200
        
        # Second unregister should fail
        response2 = client.delete(
            "/activities/Chess Club/signup",
            params={"email": "michael@mergington.edu"}
        )
        assert response2.status_code == 404


class TestSignupAndUnregisterFlow:
    """Integration tests for signup and unregister flows."""

    def test_signup_then_unregister_flow(self, client):
        """Test full flow: signup, verify, unregister, verify."""
        email = "flowtest@mergington.edu"
        activity = "Chess Club"
        
        # Initially not signed up
        data = client.get("/activities").json()
        assert email not in data[activity]["participants"]
        initial_count = len(data[activity]["participants"])
        
        # Sign up
        response = client.post(
            f"/activities/{activity}/signup",
            params={"email": email}
        )
        assert response.status_code == 200
        
        # Verify signed up
        data = client.get("/activities").json()
        assert email in data[activity]["participants"]
        assert len(data[activity]["participants"]) == initial_count + 1
        
        # Unregister
        response = client.delete(
            f"/activities/{activity}/signup",
            params={"email": email}
        )
        assert response.status_code == 200
        
        # Verify unregistered
        data = client.get("/activities").json()
        assert email not in data[activity]["participants"]
        assert len(data[activity]["participants"]) == initial_count

    def test_multiple_signups_and_unregisters(self, client):
        """Test complex flow with multiple signups and unregisters."""
        emails = ["student1@test.edu", "student2@test.edu", "student3@test.edu"]
        activity = "Programming Class"
        
        # Sign up all
        for email in emails:
            response = client.post(
                f"/activities/{activity}/signup",
                params={"email": email}
            )
            assert response.status_code == 200
        
        # Verify all signed up
        data = client.get("/activities").json()
        for email in emails:
            assert email in data[activity]["participants"]
        assert len(data[activity]["participants"]) == 5  # 2 initial + 3 new
        
        # Unregister middle one
        client.delete(
            f"/activities/{activity}/signup",
            params={"email": emails[1]}
        )
        
        # Verify only middle one removed
        data = client.get("/activities").json()
        assert emails[0] in data[activity]["participants"]
        assert emails[1] not in data[activity]["participants"]
        assert emails[2] in data[activity]["participants"]
        assert len(data[activity]["participants"]) == 4
