"""Integration tests for Knowledge Base API endpoints."""

import pytest
from httpx import AsyncClient
from unittest.mock import patch


class TestKnowledgeBaseAPI:
    """Integration tests for Knowledge Base API."""

    async def test_health_check(self, test_client: AsyncClient):
        """Test health check endpoint."""
        response = await test_client.get("/health")

        assert response.status_code == 200
        data = response.json()
        assert data["service"] == "kbservice"
        assert data["status"] in ["healthy", "unhealthy"]
        assert "timestamp" in data
        assert "version" in data

    async def test_root_endpoint(self, test_client: AsyncClient):
        """Test root endpoint."""
        response = await test_client.get("/")

        assert response.status_code == 200
        data = response.json()
        assert data["service"] == "kbservice"
        assert data["status"] == "healthy"
        assert "timestamp" in data
        assert "version" in data

    @pytest.mark.asyncio
    async def test_create_knowledge_item_as_admin(
        self, 
        test_client: AsyncClient, 
        sample_knowledge_item,
        admin_user
    ):
        """Test creating a knowledge item as admin."""
        with patch("app.dependencies.verify_token") as mock_verify:
            # Mock token verification to return admin user
            mock_verify.return_value = type('TokenData', (), {
                'user_id': admin_user["user_id"],
                'email': admin_user["email"],
                'role': admin_user["role"],
                'exp': None
            })()

            response = await test_client.post(
                "/api/v1/kb/items",
                json=sample_knowledge_item,
                headers={"Authorization": "Bearer fake-admin-token"}
            )

            assert response.status_code == 201
            data = response.json()
            assert data["title"] == sample_knowledge_item["title"]
            assert data["content"] == sample_knowledge_item["content"]
            assert data["category"] == sample_knowledge_item["category"]
            assert "id" in data
            assert "created_at" in data

    @pytest.mark.asyncio
    async def test_create_knowledge_item_as_student_forbidden(
        self, 
        test_client: AsyncClient, 
        sample_knowledge_item,
        student_user
    ):
        """Test that students cannot create knowledge items."""
        with patch("app.dependencies.verify_token") as mock_verify:
            # Mock token verification to return student user
            mock_verify.return_value = type('TokenData', (), {
                'user_id': student_user["user_id"],
                'email': student_user["email"],
                'role': student_user["role"],
                'exp': None
            })()

            response = await test_client.post(
                "/api/v1/kb/items",
                json=sample_knowledge_item,
                headers={"Authorization": "Bearer fake-student-token"}
            )

            assert response.status_code == 403
            data = response.json()
            assert "admin" in data["detail"].lower()

    @pytest.mark.asyncio
    async def test_list_knowledge_items(
        self, 
        test_client: AsyncClient,
        student_user
    ):
        """Test listing knowledge items."""
        with patch("app.dependencies.verify_token") as mock_verify:
            # Mock token verification
            mock_verify.return_value = type('TokenData', (), {
                'user_id': student_user["user_id"],
                'email': student_user["email"],
                'role': student_user["role"],
                'exp': None
            })()

            response = await test_client.get(
                "/api/v1/kb/items",
                headers={"Authorization": "Bearer fake-token"}
            )

            assert response.status_code == 200
            data = response.json()
            assert isinstance(data, list)

    @pytest.mark.asyncio
    async def test_search_knowledge_items(
        self, 
        test_client: AsyncClient,
        student_user
    ):
        """Test searching knowledge items."""
        with patch("app.dependencies.verify_token") as mock_verify:
            # Mock token verification
            mock_verify.return_value = type('TokenData', (), {
                'user_id': student_user["user_id"],
                'email': student_user["email"],
                'role': student_user["role"],
                'exp': None
            })()

            response = await test_client.get(
                "/api/v1/kb/search?query=asistencia",
                headers={"Authorization": "Bearer fake-token"}
            )

            assert response.status_code == 200
            data = response.json()
            assert "results" in data
            assert "total_count" in data
            assert "query" in data
            assert isinstance(data["results"], list)

    @pytest.mark.asyncio
    async def test_semantic_search(
        self, 
        test_client: AsyncClient,
        student_user
    ):
        """Test semantic search endpoint."""
        with patch("app.dependencies.verify_token") as mock_verify:
            # Mock token verification
            mock_verify.return_value = type('TokenData', (), {
                'user_id': student_user["user_id"],
                'email': student_user["email"],
                'role': student_user["role"],
                'exp': None
            })()

            response = await test_client.get(
                "/api/v1/kb/semantic-search?query=como marcar presente",
                headers={"Authorization": "Bearer fake-token"}
            )

            assert response.status_code == 200
            data = response.json()
            assert "results" in data
            assert "total_count" in data
            assert "query" in data

    @pytest.mark.asyncio
    async def test_intelligent_query(
        self, 
        test_client: AsyncClient,
        student_user
    ):
        """Test intelligent query endpoint."""
        with patch("app.dependencies.verify_token") as mock_verify:
            # Mock token verification
            mock_verify.return_value = type('TokenData', (), {
                'user_id': student_user["user_id"],
                'email': student_user["email"],
                'role': student_user["role"],
                'exp': None
            })()

            query_data = {
                "query": "¿Qué pasa si no marco asistencia?",
                "context": {"location": "classroom"},
                "filters": {}
            }

            response = await test_client.post(
                "/api/v1/kb/query",
                json=query_data,
                headers={"Authorization": "Bearer fake-token"}
            )

            assert response.status_code == 200
            data = response.json()
            assert "response" in data
            assert "sources" in data
            assert "suggestions" in data
            assert "query" in data

    @pytest.mark.asyncio
    async def test_submit_feedback(
        self, 
        test_client: AsyncClient,
        student_user
    ):
        """Test submitting feedback for a knowledge item."""
        with patch("app.dependencies.verify_token") as mock_verify:
            # Mock token verification
            mock_verify.return_value = type('TokenData', (), {
                'user_id': student_user["user_id"],
                'email': student_user["email"],
                'role': student_user["role"],
                'exp': None
            })()

            feedback_data = {
                "item_id": "123e4567-e89b-12d3-a456-426614174000",
                "feedback_type": "helpful",
                "comment": "Esta información me ayudó mucho"
            }

            response = await test_client.post(
                "/api/v1/kb/feedback",
                json=feedback_data,
                headers={"Authorization": "Bearer fake-token"}
            )

            # This might return 201 or 404 depending on whether the item exists
            assert response.status_code in [201, 404]

    @pytest.mark.asyncio
    async def test_get_categories(
        self, 
        test_client: AsyncClient,
        student_user
    ):
        """Test getting available categories."""
        with patch("app.dependencies.verify_token") as mock_verify:
            # Mock token verification
            mock_verify.return_value = type('TokenData', (), {
                'user_id': student_user["user_id"],
                'email': student_user["email"],
                'role': student_user["role"],
                'exp': None
            })()

            response = await test_client.get(
                "/api/v1/kb/categories",
                headers={"Authorization": "Bearer fake-token"}
            )

            assert response.status_code == 200
            data = response.json()
            assert isinstance(data, list)
            assert len(data) > 0

    @pytest.mark.asyncio
    async def test_delete_knowledge_item_as_admin(
        self, 
        test_client: AsyncClient,
        admin_user
    ):
        """Test deleting a knowledge item as admin."""
        with patch("app.dependencies.verify_token") as mock_verify:
            # Mock token verification to return admin user
            mock_verify.return_value = type('TokenData', (), {
                'user_id': admin_user["user_id"],
                'email': admin_user["email"],
                'role': admin_user["role"],
                'exp': None
            })()

            # First create an item to delete
            sample_item = {
                "title": "Item to delete",
                "content": "This item will be deleted",
                "content_type": "article",
                "category": "Test",
                "target_audience": "all",
                "tags": ["test", "delete"]
            }

            create_response = await test_client.post(
                "/api/v1/kb/items",
                json=sample_item,
                headers={"Authorization": "Bearer fake-admin-token"}
            )

            assert create_response.status_code == 201
            created_item = create_response.json()
            item_id = created_item["id"]

            # Now delete the item
            delete_response = await test_client.delete(
                f"/api/v1/kb/items/{item_id}",
                headers={"Authorization": "Bearer fake-admin-token"}
            )

            assert delete_response.status_code == 200
            data = delete_response.json()
            assert "success" in data["message"].lower()

            # Verify the item is deleted
            get_response = await test_client.get(
                f"/api/v1/kb/items/{item_id}",
                headers={"Authorization": "Bearer fake-admin-token"}
            )

            assert get_response.status_code == 404

    @pytest.mark.asyncio
    async def test_delete_knowledge_item_as_student_forbidden(
        self, 
        test_client: AsyncClient,
        student_user
    ):
        """Test that students cannot delete knowledge items."""
        with patch("app.dependencies.verify_token") as mock_verify:
            # Mock token verification to return student user
            mock_verify.return_value = type('TokenData', (), {
                'user_id': student_user["user_id"],
                'email': student_user["email"],
                'role': student_user["role"],
                'exp': None
            })()

            # Try to delete an item (using a random UUID)
            response = await test_client.delete(
                "/api/v1/kb/items/123e4567-e89b-12d3-a456-426614174000",
                headers={"Authorization": "Bearer fake-student-token"}
            )

            assert response.status_code == 403
            data = response.json()
            assert "admin" in data["detail"].lower()

    @pytest.mark.asyncio
    async def test_unauthorized_access(self, test_client: AsyncClient):
        """Test that endpoints require authentication."""
        response = await test_client.get("/api/v1/kb/items")

        assert response.status_code == 401
        data = response.json()
        assert "authorization" in data["detail"].lower() or "missing" in data["detail"].lower()
