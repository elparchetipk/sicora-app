package repositories

import (
	"context"
	"time"

	"kbservice/internal/domain/entities"

	"github.com/google/uuid"
)

// DocumentSearchCriteria represents search criteria for documents
type DocumentSearchCriteria struct {
	Query         string                      `json:"query"`
	Categories    []entities.DocumentCategory `json:"categories"`
	Types         []entities.DocumentType     `json:"types"`
	Audiences     []entities.AudienceType     `json:"audiences"`
	Statuses      []entities.DocumentStatus   `json:"statuses"`
	Tags          []string                    `json:"tags"`
	AuthorIDs     []uuid.UUID                 `json:"authorIds"`
	DateFrom      *time.Time                  `json:"dateFrom"`
	DateTo        *time.Time                  `json:"dateTo"`
	MinRating     *float64                    `json:"minRating"`
	SortBy        string                      `json:"sortBy"` // title, created_at, updated_at, view_count, rating
	SortOrder     string                      `json:"sortOrder"` // asc, desc
	Limit         int                         `json:"limit"`
	Offset        int                         `json:"offset"`
}

// SemanticSearchRequest represents a semantic search request
type SemanticSearchRequest struct {
	Query         string                      `json:"query"`
	Embedding     []float32                   `json:"embedding"`
	Categories    []entities.DocumentCategory `json:"categories"`
	Audiences     []entities.AudienceType     `json:"audiences"`
	Limit         int                         `json:"limit"`
	Threshold     float64                     `json:"threshold"` // similarity threshold
}

// DocumentRepository defines the interface for document data persistence
type DocumentRepository interface {
	// Basic CRUD operations
	Create(ctx context.Context, document *entities.Document) error
	GetByID(ctx context.Context, id uuid.UUID) (*entities.Document, error)
	GetBySlug(ctx context.Context, slug string) (*entities.Document, error)
	Update(ctx context.Context, document *entities.Document) error
	Delete(ctx context.Context, id uuid.UUID) error
	SoftDelete(ctx context.Context, id uuid.UUID) error
	
	// List and search operations
	List(ctx context.Context, criteria DocumentSearchCriteria) ([]entities.Document, int, error)
	Search(ctx context.Context, criteria DocumentSearchCriteria) ([]entities.Document, int, error)
	SemanticSearch(ctx context.Context, request SemanticSearchRequest) ([]entities.Document, error)
	
	// Category and filtering
	GetByCategory(ctx context.Context, category entities.DocumentCategory, limit, offset int) ([]entities.Document, error)
	GetByAuthor(ctx context.Context, authorID uuid.UUID, limit, offset int) ([]entities.Document, error)
	GetByStatus(ctx context.Context, status entities.DocumentStatus, limit, offset int) ([]entities.Document, error)
	GetByAudience(ctx context.Context, audience entities.AudienceType, limit, offset int) ([]entities.Document, error)
	
	// Hierarchical operations
	GetChildren(ctx context.Context, parentID uuid.UUID) ([]entities.Document, error)
	GetParent(ctx context.Context, documentID uuid.UUID) (*entities.Document, error)
	
	// Version management
	CreateVersion(ctx context.Context, version *entities.DocumentVersion) error
	GetVersions(ctx context.Context, documentID uuid.UUID) ([]entities.DocumentVersion, error)
	GetVersion(ctx context.Context, documentID uuid.UUID, version string) (*entities.DocumentVersion, error)
	RestoreVersion(ctx context.Context, documentID uuid.UUID, version string) error
	
	// Analytics and statistics
	IncrementViewCount(ctx context.Context, documentID uuid.UUID, userID *uuid.UUID) error
	IncrementLikeCount(ctx context.Context, documentID uuid.UUID) error
	IncrementShareCount(ctx context.Context, documentID uuid.UUID) error
	GetPopularDocuments(ctx context.Context, category *entities.DocumentCategory, limit int) ([]entities.Document, error)
	GetRecentDocuments(ctx context.Context, category *entities.DocumentCategory, limit int) ([]entities.Document, error)
	
	// Rating operations
	AddRating(ctx context.Context, rating *entities.DocumentRating) error
	UpdateRating(ctx context.Context, rating *entities.DocumentRating) error
	GetRating(ctx context.Context, documentID, userID uuid.UUID) (*entities.DocumentRating, error)
	GetAverageRating(ctx context.Context, documentID uuid.UUID) (float64, int, error)
	
	// Comment operations
	AddComment(ctx context.Context, comment *entities.DocumentComment) error
	UpdateComment(ctx context.Context, comment *entities.DocumentComment) error
	DeleteComment(ctx context.Context, commentID uuid.UUID) error
	GetComments(ctx context.Context, documentID uuid.UUID, limit, offset int) ([]entities.DocumentComment, error)
	
	// Workflow operations
	SubmitForReview(ctx context.Context, documentID uuid.UUID, reviewerID uuid.UUID) error
	ApproveDocument(ctx context.Context, documentID uuid.UUID, reviewerID uuid.UUID) error
	RejectDocument(ctx context.Context, documentID uuid.UUID, reviewerID uuid.UUID, reason string) error
	PublishDocument(ctx context.Context, documentID uuid.UUID) error
	ArchiveDocument(ctx context.Context, documentID uuid.UUID) error
	
	// Bulk operations
	BulkUpdateStatus(ctx context.Context, documentIDs []uuid.UUID, status entities.DocumentStatus) error
	BulkDelete(ctx context.Context, documentIDs []uuid.UUID) error
	BulkArchive(ctx context.Context, documentIDs []uuid.UUID) error
	
	// Analytics tracking
	RecordAnalytic(ctx context.Context, analytic *entities.DocumentAnalytic) error
	GetAnalytics(ctx context.Context, documentID uuid.UUID, from, to time.Time) ([]entities.DocumentAnalytic, error)
	GetDocumentStats(ctx context.Context, documentID uuid.UUID) (*DocumentStats, error)
	
	// Search index operations
	UpdateSearchIndex(ctx context.Context, documentID uuid.UUID) error
	RebuildSearchIndex(ctx context.Context) error
	
	// Related content
	GetRelatedDocuments(ctx context.Context, documentID uuid.UUID, limit int) ([]entities.Document, error)
	GetSimilarDocuments(ctx context.Context, embedding []float32, excludeID uuid.UUID, limit int) ([]entities.Document, error)
}

// DocumentStats represents aggregated statistics for a document
type DocumentStats struct {
	TotalViews    int     `json:"totalViews"`
	TotalLikes    int     `json:"totalLikes"`
	TotalShares   int     `json:"totalShares"`
	TotalComments int     `json:"totalComments"`
	AverageRating float64 `json:"averageRating"`
	RatingCount   int     `json:"ratingCount"`
	ViewsToday    int     `json:"viewsToday"`
	ViewsThisWeek int     `json:"viewsThisWeek"`
	ViewsThisMonth int    `json:"viewsThisMonth"`
}
