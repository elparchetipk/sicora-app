package tests

import (
	"testing"

	"projectevalservice/internal/domain/entities"

	"github.com/google/uuid"
	"github.com/stretchr/testify/assert"
)

func TestDocumentTypeValidation(t *testing.T) {
	doc := &entities.ProjectDocument{}

	validTypes := []entities.DocumentType{
		entities.DocumentTypeRequirement,
		entities.DocumentTypeSpecification,
		entities.DocumentTypeDesign,
		entities.DocumentTypeTestPlan,
		entities.DocumentTypeUserManual,
		entities.DocumentTypeReport,
		entities.DocumentTypePresentation,
		entities.DocumentTypeOther,
	}

	for _, docType := range validTypes {
		assert.True(t, doc.IsValidType(docType))
	}

	assert.False(t, doc.IsValidType("invalid_type"))
}

func TestDocumentStatusValidation(t *testing.T) {
	doc := &entities.ProjectDocument{}

	validStatuses := []entities.DocumentStatus{
		entities.DocumentStatusDraft,
		entities.DocumentStatusReview,
		entities.DocumentStatusApproved,
		entities.DocumentStatusRejected,
		entities.DocumentStatusArchived,
	}

	for _, status := range validStatuses {
		assert.True(t, doc.IsValidStatus(status))
	}

	assert.False(t, doc.IsValidStatus("invalid_status"))
}

func TestDocumentVisibilityValidation(t *testing.T) {
	doc := &entities.ProjectDocument{}

	validVisibilities := []entities.DocumentVisibility{
		entities.DocumentVisibilityPublic,
		entities.DocumentVisibilityPrivate,
		entities.DocumentVisibilityRestricted,
	}

	for _, visibility := range validVisibilities {
		assert.True(t, doc.IsValidVisibility(visibility))
	}

	assert.False(t, doc.IsValidVisibility("invalid_visibility"))
}

func TestDocumentStatusCheckers(t *testing.T) {
	doc := &entities.ProjectDocument{}

	doc.Status = entities.DocumentStatusDraft
	assert.True(t, doc.IsDraft())
	assert.False(t, doc.IsApproved())
	assert.False(t, doc.IsInReview())
	assert.False(t, doc.IsRejected())

	doc.Status = entities.DocumentStatusApproved
	assert.False(t, doc.IsDraft())
	assert.True(t, doc.IsApproved())
	assert.False(t, doc.IsInReview())
	assert.False(t, doc.IsRejected())

	doc.Status = entities.DocumentStatusReview
	assert.False(t, doc.IsDraft())
	assert.False(t, doc.IsApproved())
	assert.True(t, doc.IsInReview())
	assert.False(t, doc.IsRejected())

	doc.Status = entities.DocumentStatusRejected
	assert.False(t, doc.IsDraft())
	assert.False(t, doc.IsApproved())
	assert.False(t, doc.IsInReview())
	assert.True(t, doc.IsRejected())
}

func TestDocumentApproval(t *testing.T) {
	doc := &entities.ProjectDocument{
		Status: entities.DocumentStatusReview,
	}

	approverID := uuid.New()
	err := doc.Approve(approverID)
	assert.NoError(t, err)
	assert.Equal(t, entities.DocumentStatusApproved, doc.Status)
	assert.Equal(t, approverID, *doc.ApprovedByID)
	assert.NotNil(t, doc.ApprovedAt)
}

func TestDocumentRejection(t *testing.T) {
	doc := &entities.ProjectDocument{
		Status: entities.DocumentStatusReview,
	}

	reviewerID := uuid.New()
	err := doc.Reject(reviewerID, "needs revision")
	assert.NoError(t, err)
	assert.Equal(t, entities.DocumentStatusRejected, doc.Status)
	assert.Equal(t, "needs revision", doc.ReviewComments)
	assert.Equal(t, reviewerID, *doc.ReviewedByID)
	assert.NotNil(t, doc.ReviewedAt)
}

func TestDocumentTagManagement(t *testing.T) {
	doc := &entities.ProjectDocument{
		Tags: []string{"initial", "test"},
	}

	// Test adding tag
	doc.AddTag("new-tag")
	assert.True(t, doc.HasTag("new-tag"))
	assert.True(t, doc.HasTag("initial"))
	assert.True(t, doc.HasTag("test"))

	// Test removing tag
	doc.RemoveTag("initial")
	assert.False(t, doc.HasTag("initial"))
	assert.True(t, doc.HasTag("new-tag"))
	assert.True(t, doc.HasTag("test"))

	// Test checking non-existent tag
	assert.False(t, doc.HasTag("non-existent"))
}
