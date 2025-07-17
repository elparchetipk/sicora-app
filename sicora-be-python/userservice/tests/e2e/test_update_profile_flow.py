import pytest
import asyncio
from fastapi.testclient import TestClient
from sqlalchemy.ext.asyncio import AsyncSession

from main import app
from tests.utils.test_helpers import AuthTestHelper
from app.domain.value_objects.user_role import UserRole

class TestUpdateProfileFlow:
    @pytest.fixture(autouse=True)
    def setup(self, test_db_session: AsyncSession):
        self.client = TestClient(app)
        self.auth_helper = AuthTestHelper(self.client)
        self.test_db_session = test_db_session
    
    def test_complete_update_profile_flow(self):
        """Test the complete flow of updating a user profile."""
        # Step 1: Register a new user
        user_data = {
            "first_name": "Profile",
            "last_name": "Test",
            "email": "profile.test@example.com",
            "document_number": "12345678",
            "document_type": "CC",
            "password": "StrongPass123!",
            "role": "APPRENTICE"
        }
        
        register_response = self.client.post(
            "/api/v1/auth/register",
            json=user_data
        )
        assert register_response.status_code == 201
        
        # Extract tokens from registration response
        tokens = register_response.json()
        access_token = tokens["access_token"]
        
        # Step 2: Get current profile
        profile_response = self.client.get(
            "/api/v1/auth/me",
            headers={"Authorization": f"Bearer {access_token}"}
        )
        assert profile_response.status_code == 200
        initial_profile = profile_response.json()
        
        # Verify initial profile data
        assert initial_profile["first_name"] == "Profile"
        assert initial_profile["last_name"] == "Test"
        assert initial_profile["email"] == "profile.test@example.com"
        
        # Step 3: Update profile
        update_data = {
            "first_name": "Updated",
            "last_name": "Profile",
            "phone": "9876543210"
        }
        
        update_response = self.client.put(
            "/api/v1/auth/profile",
            json=update_data,
            headers={"Authorization": f"Bearer {access_token}"}
        )
        assert update_response.status_code == 200
        updated_profile = update_response.json()
        
        # Verify updated profile data
        assert updated_profile["first_name"] == "Updated"
        assert updated_profile["last_name"] == "Profile"
        assert updated_profile["phone"] == "9876543210"
        
        # Verify that other fields remain unchanged
        assert updated_profile["email"] == "profile.test@example.com"
        assert updated_profile["document_number"] == "12345678"
        
        # Step 4: Verify profile was actually updated in the database by getting it again
        verify_response = self.client.get(
            "/api/v1/auth/me",
            headers={"Authorization": f"Bearer {access_token}"}
        )
        assert verify_response.status_code == 200
        verified_profile = verify_response.json()
        
        # Verify that the changes persisted
        assert verified_profile["first_name"] == "Updated"
        assert verified_profile["last_name"] == "Profile"
        assert verified_profile["phone"] == "9876543210"
    
    def test_update_profile_with_different_roles(self):
        """Test that users with different roles can update their profiles."""
        # Create users with different roles
        roles = [UserRole.ADMIN, UserRole.INSTRUCTOR, UserRole.APPRENTICE]
        tokens = {}
        
        for role in roles:
            email = f"{role.value.lower()}.profile@example.com"
            token = self.auth_helper.create_and_login_user(
                email=email,
                password="StrongPass123!",
                role=role
            )
            tokens[role.value] = token
        
        # Update profile for each role
        for role, token in tokens.items():
            update_data = {
                "first_name": f"Updated{role}",
                "last_name": "User",
                "phone": "9876543210"
            }
            
            response = self.client.put(
                "/api/v1/auth/profile",
                json=update_data,
                headers={"Authorization": f"Bearer {token}"}
            )
            
            assert response.status_code == 200
            updated_profile = response.json()
            
            # Verify updated profile data
            assert updated_profile["first_name"] == f"Updated{role}"
            assert updated_profile["last_name"] == "User"
            assert updated_profile["phone"] == "9876543210"
            
            # Verify with a get request
            verify_response = self.client.get(
                "/api/v1/auth/me",
                headers={"Authorization": f"Bearer {token}"}
            )
            
            assert verify_response.status_code == 200
            verified_profile = verify_response.json()
            
            assert verified_profile["first_name"] == f"Updated{role}"
            assert verified_profile["last_name"] == "User"
            assert verified_profile["phone"] == "9876543210"