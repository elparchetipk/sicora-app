import pytest
from fastapi.testclient import TestClient
from sqlalchemy.ext.asyncio import AsyncSession
import json
from uuid import uuid4

from main import app
from tests.utils.test_helpers import AuthTestHelper
from app.domain.value_objects.user_role import UserRole

class TestUpdateProfileEndpoint:
    @pytest.fixture(autouse=True)
    def setup(self, test_db_session: AsyncSession):
        self.client = TestClient(app)
        self.auth_helper = AuthTestHelper(self.client)
        self.test_db_session = test_db_session
        
        # Create test users for different roles
        self.admin_token = self.auth_helper.create_and_login_user(
            email="admin.profile@test.com",
            password="StrongPass123!",
            role=UserRole.ADMIN
        )
        
        self.apprentice_token = self.auth_helper.create_and_login_user(
            email="apprentice.profile@test.com",
            password="StrongPass123!",
            role=UserRole.APPRENTICE
        )
        
        self.instructor_token = self.auth_helper.create_and_login_user(
            email="instructor.profile@test.com",
            password="StrongPass123!",
            role=UserRole.INSTRUCTOR
        )
    
    def test_update_profile_success(self):
        """Test successful profile update with all fields."""
        # Arrange
        update_data = {
            "first_name": "Updated",
            "last_name": "Name",
            "phone": "9876543210"
        }
        
        # Act
        response = self.client.put(
            "/api/v1/auth/profile",
            json=update_data,
            headers={"Authorization": f"Bearer {self.apprentice_token}"}
        )
        
        # Assert
        assert response.status_code == 200
        data = response.json()
        assert data["first_name"] == "Updated"
        assert data["last_name"] == "Name"
        assert data["phone"] == "9876543210"
    
    def test_update_profile_partial(self):
        """Test partial profile update with only some fields."""
        # Arrange
        update_data = {
            "first_name": "PartialUpdate"
        }
        
        # Act
        response = self.client.put(
            "/api/v1/auth/profile",
            json=update_data,
            headers={"Authorization": f"Bearer {self.instructor_token}"}
        )
        
        # Assert
        assert response.status_code == 200
        data = response.json()
        assert data["first_name"] == "PartialUpdate"
        # Last name should remain unchanged
        assert data["last_name"] != ""
    
    def test_update_profile_unauthorized(self):
        """Test profile update without authentication."""
        # Arrange
        update_data = {
            "first_name": "Unauthorized",
            "last_name": "Update"
        }
        
        # Act
        response = self.client.put(
            "/api/v1/auth/profile",
            json=update_data
        )
        
        # Assert
        assert response.status_code == 401
    
    def test_update_profile_invalid_token(self):
        """Test profile update with invalid token."""
        # Arrange
        update_data = {
            "first_name": "Invalid",
            "last_name": "Token"
        }
        
        # Act
        response = self.client.put(
            "/api/v1/auth/profile",
            json=update_data,
            headers={"Authorization": "Bearer invalid_token"}
        )
        
        # Assert
        assert response.status_code == 401
    
    def test_update_profile_empty_fields(self):
        """Test profile update with empty fields."""
        # Arrange
        update_data = {
            "first_name": "",
            "last_name": ""
        }
        
        # Act
        response = self.client.put(
            "/api/v1/auth/profile",
            json=update_data,
            headers={"Authorization": f"Bearer {self.admin_token}"}
        )
        
        # Assert
        assert response.status_code == 200
        data = response.json()
        # Empty strings should be allowed for these fields
        assert data["first_name"] == ""
        assert data["last_name"] == ""
    
    def test_update_profile_all_roles(self):
        """Test that all roles can update their own profile."""
        # Arrange
        update_data = {
            "first_name": "RoleTest",
            "last_name": "User"
        }
        
        # Test for each role
        for token in [self.admin_token, self.instructor_token, self.apprentice_token]:
            # Act
            response = self.client.put(
                "/api/v1/auth/profile",
                json=update_data,
                headers={"Authorization": f"Bearer {token}"}
            )
            
            # Assert
            assert response.status_code == 200
            data = response.json()
            assert data["first_name"] == "RoleTest"
            assert data["last_name"] == "User"