package tests

import (
	"testing"

	"github.com/stretchr/testify/assert"
)

func TestDocumentTypeValidation(t *testing.T) {
	doc := &ProjectDocument{}

	validTypes := []DocumentType{
		DocumentTypeRequirement,
		DocumentTypeSpecification,
		DocumentTypeDesign,
		DocumentTypeTestPlan,
		DocumentTypeUserManual,
		DocumentTypeReport,
		DocumentTypePresentation,
		DocumentTypeOther,
	}

	for _, docType := range validTypes {
		assert.True(t, doc.IsValidType(docType))
	}

	assert.False(t, doc.IsValidType("invalid_type"))
}

func TestDocumentStatusValidation(t *testing.T) {
	doc := &ProjectDocument{}

	validStatuses := []DocumentStatus{
		DocumentStatusDraft,
		DocumentStatusReview,
		DocumentStatusApproved,
		DocumentStatusRejected,
		DocumentStatusArchived,
	}

	for _, status := range validStatuses {
		assert.True(t, doc.IsValidStatus(status))
	}

	assert.False(t, doc.IsValidStatus("invalid_status"))
}

func TestDocumentVisibilityValidation(t *testing.T) {
	doc := &ProjectDocument{}

	validVisibilities := []DocumentVisibility{
		DocumentVisibilityPublic,
		DocumentVisibilityPrivate,
		DocumentVisibilityRestricted,
		DocumentVisibilityInternal,
	}

	for _, visibility := range validVisibilities {
		assert.True(t, doc.IsValidVisibility(visibility))
	}

	assert.False(t, doc.IsValidVisibility("invalid_visibility"))
}

func TestDocumentStatusCheckers(t *testing.T) {
	doc := &ProjectDocument{}

	doc.Status = DocumentStatusDraft
	assert.True(t, doc.IsDraft())
	assert.False(t, doc.IsInReview())
	assert.False(t, doc.IsApproved())
	assert.False(t, doc.IsRejected())

	doc.Status = DocumentStatusReview
	assert.False(t, doc.IsDraft())
	assert.True(t, doc.IsInReview())
	assert.False(t, doc.IsApproved())
	assert.False(t, doc.IsRejected())

	doc.Status = DocumentStatusApproved
	assert.False(t, doc.IsDraft())
	assert.False(t, doc.IsInReview())
	assert.True(t, doc.IsApproved())
	assert.False(t, doc.IsRejected())

	doc.Status = DocumentStatusRejected
	assert.False(t, doc.IsDraft())
	assert.False(t, doc.IsInReview())
	assert.False(t, doc.IsApproved())
	assert.True(t, doc.IsRejected())
}

func TestDocumentTagManagement(t *testing.T) {
	doc := &ProjectDocument{
		Tags: []string{"requirements", "v1"},
	}

	doc.AddTag("approved")
	assert.Contains(t, doc.Tags, "approved")
	assert.Len(t, doc.Tags, 3)

	doc.AddTag("requirements")
	assert.Len(t, doc.Tags, 3)

	doc.AddTag("")
	assert.Len(t, doc.Tags, 3)

	doc.RemoveTag("v1")
	assert.NotContains(t, doc.Tags, "v1")
	assert.Len(t, doc.Tags, 2)

	doc.RemoveTag("non-existing")
	assert.Len(t, doc.Tags, 2)

	assert.True(t, doc.HasTag("requirements"))
	assert.True(t, doc.HasTag("approved"))
	assert.False(t, doc.HasTag("v1"))
	assert.False(t, doc.HasTag("non-existing"))
}

func TestDocumentSubmitForReview(t *testing.T) {
	doc := &ProjectDocument{
		Status: DocumentStatusDraft,
	}

	err := doc.SubmitForReview()
	assert.NoError(t, err)
	assert.Equal(t, DocumentStatusReview, doc.Status)

	doc.Status = DocumentStatusApproved
	err = doc.SubmitForReview()
	assert.Error(t, err)
	assert.Contains(t, err.Error(), "only draft documents can be submitted for review")
}

func TestDocumentArchive(t *testing.T) {
	doc := &ProjectDocument{
		Status: DocumentStatusApproved,
	}

	doc.Archive()
	assert.Equal(t, DocumentStatusArchived, doc.Status)
}

func TestDocumentIncrementDownloadCount(t *testing.T) {
	doc := &ProjectDocument{
		DownloadCount: 5,
	}

	doc.IncrementDownloadCount()
	assert.Equal(t, 6, doc.DownloadCount)
	assert.NotNil(t, doc.LastAccessedAt)
}

func TestDocumentUpdateVersion(t *testing.T) {
	doc := &ProjectDocument{
		Version: "1.0",
	}

	doc.UpdateVersion("2.0")
	assert.Equal(t, "2.0", doc.Version)
}
