"""Unit tests for KnowledgeItem entity."""

import pytest
from datetime import datetime, timezone
from uuid import uuid4

from app.domain.entities.kb_entities import (
    KnowledgeItem, ContentType, ContentStatus, TargetAudience, UserRole
)
from app.domain.value_objects.kb_value_objects import (
    KnowledgeItemId, Title, Content, CategoryName, TagName, Vector
)


class TestKnowledgeItem:
    """Test cases for KnowledgeItem entity."""
    
    def test_create_knowledge_item_with_required_fields(self):
        """Test creating a knowledge item with required fields only."""
        item = KnowledgeItem(
            title=Title("Test Title"),
            content=Content("Test content"),
            content_type=ContentType.GUIDE,
            category=CategoryName("test-category"),
            target_audience=TargetAudience.STUDENT,
            author_id=uuid4()
        )
        
        assert item.title.value == "Test Title"
        assert item.content.value == "Test content"
        assert item.content_type == ContentType.GUIDE
        assert item.category.value == "test-category"
        assert item.target_audience == TargetAudience.STUDENT
        assert item.status == ContentStatus.DRAFT  # Default status
        assert item.tags == []  # Default empty tags
        assert item.view_count == 0
        assert item.helpful_count == 0
        assert item.unhelpful_count == 0
        assert item.version == 1
        assert isinstance(item.created_at, datetime)
        assert isinstance(item.updated_at, datetime)
    
    def test_create_knowledge_item_with_all_fields(self):
        """Test creating a knowledge item with all fields."""
        tags = [TagName("tag1"), TagName("tag2")]
        embedding = Vector([0.1, 0.2, 0.3])
        
        item = KnowledgeItem(
            title=Title("Test Title"),
            content=Content("Test content"),
            content_type=ContentType.FAQ,
            category=CategoryName("test-category"),
            target_audience=TargetAudience.INSTRUCTOR,
            author_id=uuid4(),
            status=ContentStatus.PUBLISHED,
            tags=tags,
            embedding=embedding
        )
        
        assert item.status == ContentStatus.PUBLISHED
        assert len(item.tags) == 2
        assert item.tags[0].value == "tag1"
        assert item.tags[1].value == "tag2"
        assert item.embedding == embedding
    
    def test_is_accessible_by_admin(self):
        """Test that admin can access any content."""
        item = KnowledgeItem(
            title=Title("Test Title"),
            content=Content("Test content"),
            content_type=ContentType.GUIDE,
            category=CategoryName("test-category"),
            target_audience=TargetAudience.STUDENT,
            author_id=uuid4(),
            status=ContentStatus.DRAFT
        )
        
        assert item.is_accessible_by(UserRole.ADMIN) is True
    
    def test_is_accessible_by_student_published_only(self):
        """Test that student can only access published content."""
        # Draft item - not accessible
        draft_item = KnowledgeItem(
            title=Title("Draft Title"),
            content=Content("Draft content"),
            content_type=ContentType.GUIDE,
            category=CategoryName("test-category"),
            target_audience=TargetAudience.STUDENT,
            author_id=uuid4(),
            status=ContentStatus.DRAFT
        )
        
        assert draft_item.is_accessible_by(UserRole.STUDENT) is False
        
        # Published item - accessible
        published_item = KnowledgeItem(
            title=Title("Published Title"),
            content=Content("Published content"),
            content_type=ContentType.GUIDE,
            category=CategoryName("test-category"),
            target_audience=TargetAudience.STUDENT,
            author_id=uuid4(),
            status=ContentStatus.PUBLISHED
        )
        
        assert published_item.is_accessible_by(UserRole.STUDENT) is True
    
    def test_can_be_edited_by_author(self):
        """Test that author can edit their own content."""
        author_id = uuid4()
        item = KnowledgeItem(
            title=Title("Test Title"),
            content=Content("Test content"),
            content_type=ContentType.GUIDE,
            category=CategoryName("test-category"),
            target_audience=TargetAudience.STUDENT,
            author_id=author_id
        )
        
        assert item.can_be_edited_by(author_id, UserRole.INSTRUCTOR) is True
    
    def test_can_be_edited_by_admin(self):
        """Test that admin can edit any content."""
        item = KnowledgeItem(
            title=Title("Test Title"),
            content=Content("Test content"),
            content_type=ContentType.GUIDE,
            category=CategoryName("test-category"),
            target_audience=TargetAudience.STUDENT,
            author_id=uuid4()
        )
        
        assert item.can_be_edited_by(uuid4(), UserRole.ADMIN) is True
    
    def test_cannot_be_edited_by_different_user(self):
        """Test that non-admin, non-author cannot edit content."""
        item = KnowledgeItem(
            title=Title("Test Title"),
            content=Content("Test content"),
            content_type=ContentType.GUIDE,
            category=CategoryName("test-category"),
            target_audience=TargetAudience.STUDENT,
            author_id=uuid4()
        )
        
        assert item.can_be_edited_by(uuid4(), UserRole.STUDENT) is False
    
    def test_increment_view_count(self):
        """Test incrementing view count."""
        item = KnowledgeItem(
            title=Title("Test Title"),
            content=Content("Test content"),
            content_type=ContentType.GUIDE,
            category=CategoryName("test-category"),
            target_audience=TargetAudience.STUDENT,
            author_id=uuid4()
        )
        
        initial_count = item.view_count
        item.increment_view_count()
        
        assert item.view_count == initial_count + 1
    
    def test_add_helpful_feedback(self):
        """Test adding helpful feedback."""
        item = KnowledgeItem(
            title=Title("Test Title"),
            content=Content("Test content"),
            content_type=ContentType.GUIDE,
            category=CategoryName("test-category"),
            target_audience=TargetAudience.STUDENT,
            author_id=uuid4()
        )
        
        initial_count = item.helpful_count
        item.add_helpful_feedback()
        
        assert item.helpful_count == initial_count + 1
    
    def test_add_unhelpful_feedback(self):
        """Test adding unhelpful feedback."""
        item = KnowledgeItem(
            title=Title("Test Title"),
            content=Content("Test content"),
            content_type=ContentType.GUIDE,
            category=CategoryName("test-category"),
            target_audience=TargetAudience.STUDENT,
            author_id=uuid4()
        )
        
        initial_count = item.unhelpful_count
        item.add_unhelpful_feedback()
        
        assert item.unhelpful_count == initial_count + 1
