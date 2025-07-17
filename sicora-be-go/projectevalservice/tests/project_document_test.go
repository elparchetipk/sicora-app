package tests

import (
	"testing"

	"projectevalservice/internal/domain/entities"

	"github.com/google/uuid"
	"github.com/stretchr/testify/assert"
)

func TestNewProjectDocument(t *testing.T) {
	projectID := uuid.New()
	uploadedByID := uuid.New()
	title := "Test Document"
	fileName := "test_document.pdf"
	filePath := "/uploads/test_document.pdf"
	fileSize := int64(1024)
	docType := entities.DocumentTypeRequirement

	doc := entities.NewProjectDocument(projectID, uploadedByID, title, fileName, filePath, fileSize, docType)

	assert.Equal(t, projectID, doc.ProjectID)
	assert.Equal(t, uploadedByID, doc.UploadedByID)
	assert.Equal(t, title, doc.Title)
	assert.Equal(t, fileName, doc.FileName)
	assert.Equal(t, filePath, doc.FilePath)
	assert.Equal(t, fileSize, doc.FileSize)
	assert.Equal(t, docType, doc.Type)
	assert.Equal(t, entities.DocumentStatusDraft, doc.Status)
	assert.Equal(t, entities.DocumentVisibilityPrivate, doc.Visibility)
	assert.Equal(t, "1.0", doc.Version)
	assert.Equal(t, 0, doc.DownloadCount)
	assert.NotEqual(t, uuid.Nil, doc.ID)
}

func TestProjectDocument_IsValid(t *testing.T) {
	t.Run("Valid document", func(t *testing.T) {
		doc := entities.NewProjectDocument(
			uuid.New(),
			uuid.New(),
			"Test Document",
			"test.pdf",
			"/uploads/test.pdf",
			1024,
			entities.DocumentTypeRequirement,
		)

		err := doc.IsValid()
		assert.NoError(t, err)
	})

	t.Run("Invalid project ID", func(t *testing.T) {
		doc := entities.NewProjectDocument(
			uuid.Nil,
			uuid.New(),
			"Test Document",
			"test.pdf",
			"/uploads/test.pdf",
			1024,
			entities.DocumentTypeRequirement,
		)

		err := doc.IsValid()
		assert.Error(t, err)
		assert.Contains(t, err.Error(), "project ID is required")
	})

	t.Run("Invalid title - too short", func(t *testing.T) {
		doc := entities.NewProjectDocument(
			uuid.New(),
			uuid.New(),
			"Te",
			"test.pdf",
			"/uploads/test.pdf",
			1024,
			entities.DocumentTypeRequirement,
		)

		err := doc.IsValid()
		assert.Error(t, err)
		assert.Contains(t, err.Error(), "title must be between 3 and 200 characters")
	})

	t.Run("Invalid file size", func(t *testing.T) {
		doc := entities.NewProjectDocument(
			uuid.New(),
			uuid.New(),
			"Test Document",
			"test.pdf",
			"/uploads/test.pdf",
			0,
			entities.DocumentTypeRequirement,
		)

		err := doc.IsValid()
		assert.Error(t, err)
		assert.Contains(t, err.Error(), "file size must be greater than 0")
	})
}

func TestProjectDocument_IsValidType(t *testing.T) {
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

func TestProjectDocument_IsValidStatus(t *testing.T) {
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

func TestProjectDocument_IsValidVisibility(t *testing.T) {
	doc := &entities.ProjectDocument{}

	validVisibilities := []entities.DocumentVisibility{
		entities.DocumentVisibilityPublic,
		entities.DocumentVisibilityPrivate,
		entities.DocumentVisibilityRestricted,
		entities.DocumentVisibilityInternal,
	}

	for _, visibility := range validVisibilities {
		assert.True(t, doc.IsValidVisibility(visibility))
	}

	assert.False(t, doc.IsValidVisibility("invalid_visibility"))
}

func TestProjectDocument_CanBeAccessedBy(t *testing.T) {
	uploadedByID := uuid.New()
	otherUserID := uuid.New()

	t.Run("Public document", func(t *testing.T) {
		doc := &entities.ProjectDocument{
			UploadedByID: uploadedByID,
			Visibility:   entities.DocumentVisibilityPublic,
		}

		assert.True(t, doc.CanBeAccessedBy(uploadedByID, "student"))
		assert.True(t, doc.CanBeAccessedBy(otherUserID, "student"))
	})

	t.Run("Private document", func(t *testing.T) {
		doc := &entities.ProjectDocument{
			UploadedByID: uploadedByID,
			Visibility:   entities.DocumentVisibilityPrivate,
		}

		assert.True(t, doc.CanBeAccessedBy(uploadedByID, "student"))
		assert.False(t, doc.CanBeAccessedBy(otherUserID, "student"))
	})

	t.Run("Restricted document", func(t *testing.T) {
		doc := &entities.ProjectDocument{
			UploadedByID: uploadedByID,
			Visibility:   entities.DocumentVisibilityRestricted,
		}

		assert.True(t, doc.CanBeAccessedBy(uploadedByID, "student"))
		assert.True(t, doc.CanBeAccessedBy(otherUserID, "coordinator"))
		assert.True(t, doc.CanBeAccessedBy(otherUserID, "manager"))
		assert.False(t, doc.CanBeAccessedBy(otherUserID, "student"))
	})

	t.Run("Internal document", func(t *testing.T) {
		doc := &entities.ProjectDocument{
			UploadedByID: uploadedByID,
			Visibility:   entities.DocumentVisibilityInternal,
		}

		assert.True(t, doc.CanBeAccessedBy(uploadedByID, "student"))
		assert.True(t, doc.CanBeAccessedBy(otherUserID, "coordinator"))
		assert.True(t, doc.CanBeAccessedBy(otherUserID, "student"))
	})
}

func TestProjectDocument_SubmitForReview(t *testing.T) {
	t.Run("Submit draft document", func(t *testing.T) {
		doc := &entities.ProjectDocument{
			Status: entities.DocumentStatusDraft,
		}

		err := doc.SubmitForReview()
		assert.NoError(t, err)
		assert.Equal(t, entities.DocumentStatusReview, doc.Status)
	})

	t.Run("Cannot submit non-draft document", func(t *testing.T) {
		doc := &entities.ProjectDocument{
			Status: entities.DocumentStatusApproved,
		}

		err := doc.SubmitForReview()
		assert.Error(t, err)
		assert.Contains(t, err.Error(), "only draft documents can be submitted for review")
	})
}

func TestProjectDocument_Review(t *testing.T) {
	reviewerID := uuid.New()
	comments := "Looks good, needs minor revisions"

	t.Run("Review document in review status", func(t *testing.T) {
		doc := &entities.ProjectDocument{
			Status: entities.DocumentStatusReview,
		}

		err := doc.Review(reviewerID, comments)
		assert.NoError(t, err)
		assert.Equal(t, reviewerID, *doc.ReviewedByID)
		assert.Equal(t, comments, doc.ReviewComments)
		assert.NotNil(t, doc.ReviewedAt)
	})

	t.Run("Cannot review document not in review status", func(t *testing.T) {
		doc := &entities.ProjectDocument{
			Status: entities.DocumentStatusDraft,
		}

		err := doc.Review(reviewerID, comments)
		assert.Error(t, err)
		assert.Contains(t, err.Error(), "document is not in review status")
	})
}

func TestProjectDocument_Approve(t *testing.T) {
	approverID := uuid.New()

	t.Run("Approve reviewed document", func(t *testing.T) {
		doc := &entities.ProjectDocument{
			Status: entities.DocumentStatusReview,
		}

		err := doc.Approve(approverID)
		assert.NoError(t, err)
		assert.Equal(t, entities.DocumentStatusApproved, doc.Status)
		assert.Equal(t, approverID, *doc.ApprovedByID)
		assert.NotNil(t, doc.ApprovedAt)
	})

	t.Run("Cannot approve document not in review", func(t *testing.T) {
		doc := &entities.ProjectDocument{
			Status: entities.DocumentStatusDraft,
		}

		err := doc.Approve(approverID)
		assert.Error(t, err)
		assert.Contains(t, err.Error(), "document must be reviewed before approval")
	})
}

func TestProjectDocument_Reject(t *testing.T) {
	reviewerID := uuid.New()
	reason := "Does not meet requirements"

	t.Run("Reject document in review", func(t *testing.T) {
		doc := &entities.ProjectDocument{
			Status: entities.DocumentStatusReview,
		}

		err := doc.Reject(reviewerID, reason)
		assert.NoError(t, err)
		assert.Equal(t, entities.DocumentStatusRejected, doc.Status)
		assert.Equal(t, reviewerID, *doc.ReviewedByID)
		assert.Equal(t, reason, doc.ReviewComments)
		assert.NotNil(t, doc.ReviewedAt)
	})

	t.Run("Cannot reject document not in review", func(t *testing.T) {
		doc := &entities.ProjectDocument{
			Status: entities.DocumentStatusDraft,
		}

		err := doc.Reject(reviewerID, reason)
		assert.Error(t, err)
		assert.Contains(t, err.Error(), "document is not in review status")
	})
}

func TestProjectDocument_Archive(t *testing.T) {
	doc := &entities.ProjectDocument{
		Status: entities.DocumentStatusApproved,
	}

	doc.Archive()
	assert.Equal(t, entities.DocumentStatusArchived, doc.Status)
}

func TestProjectDocument_IncrementDownloadCount(t *testing.T) {
	doc := &entities.ProjectDocument{
		DownloadCount: 5,
	}

	doc.IncrementDownloadCount()
	assert.Equal(t, 6, doc.DownloadCount)
	assert.NotNil(t, doc.LastAccessedAt)
}

func TestProjectDocument_UpdateVersion(t *testing.T) {
	doc := &entities.ProjectDocument{
		Version: "1.0",
	}

	doc.UpdateVersion("2.0")
	assert.Equal(t, "2.0", doc.Version)
}

func TestProjectDocument_StatusCheckers(t *testing.T) {
	doc := &entities.ProjectDocument{}

	doc.Status = entities.DocumentStatusDraft
	assert.True(t, doc.IsDraft())
	assert.False(t, doc.IsInReview())
	assert.False(t, doc.IsApproved())
	assert.False(t, doc.IsRejected())

	doc.Status = entities.DocumentStatusReview
	assert.False(t, doc.IsDraft())
	assert.True(t, doc.IsInReview())
	assert.False(t, doc.IsApproved())
	assert.False(t, doc.IsRejected())

	doc.Status = entities.DocumentStatusApproved
	assert.False(t, doc.IsDraft())
	assert.False(t, doc.IsInReview())
	assert.True(t, doc.IsApproved())
	assert.False(t, doc.IsRejected())

	doc.Status = entities.DocumentStatusRejected
	assert.False(t, doc.IsDraft())
	assert.False(t, doc.IsInReview())
	assert.False(t, doc.IsApproved())
	assert.True(t, doc.IsRejected())
}

func TestProjectDocument_TagManagement(t *testing.T) {
	doc := &entities.ProjectDocument{
		Tags: []string{"requirements", "v1"},
	}

	t.Run("Add new tag", func(t *testing.T) {
		doc.AddTag("approved")
		assert.Contains(t, doc.Tags, "approved")
		assert.Len(t, doc.Tags, 3)
	})

	t.Run("Add duplicate tag", func(t *testing.T) {
		doc.AddTag("requirements")
		assert.Len(t, doc.Tags, 3) // Should not increase
	})

	t.Run("Add empty tag", func(t *testing.T) {
		doc.AddTag("")
		assert.Len(t, doc.Tags, 3) // Should not increase
	})

	t.Run("Remove existing tag", func(t *testing.T) {
		doc.RemoveTag("v1")
		assert.NotContains(t, doc.Tags, "v1")
		assert.Len(t, doc.Tags, 2)
	})

	t.Run("Remove non-existing tag", func(t *testing.T) {
		doc.RemoveTag("non-existing")
		assert.Len(t, doc.Tags, 2) // Should not change
	})

	t.Run("Check tag existence", func(t *testing.T) {
		assert.True(t, doc.HasTag("requirements"))
		assert.True(t, doc.HasTag("approved"))
		assert.False(t, doc.HasTag("v1"))
		assert.False(t, doc.HasTag("non-existing"))
	})
}
