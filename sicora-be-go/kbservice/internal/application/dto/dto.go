package dto

import (
	"errors"
	"time"

	"kbservice/internal/domain/entities"
	"kbservice/internal/domain/repositories"

	"github.com/google/uuid"
)

// CreateDocumentRequest represents a request to create a new document
type CreateDocumentRequest struct {
	Title           string                      `json:"title" validate:"required,max=500"`
	Content         string                      `json:"content" validate:"required"`
	Summary         string                      `json:"summary,omitempty" validate:"max=1000"`
	Type            entities.DocumentType       `json:"type" validate:"required"`
	Category        entities.DocumentCategory   `json:"category" validate:"required"`
	Audience        entities.AudienceType       `json:"audience" validate:"required"`
	Tags            []string                    `json:"tags,omitempty"`
	Slug            string                      `json:"slug,omitempty" validate:"max=100"`
	MetaTitle       string                      `json:"metaTitle,omitempty" validate:"max=60"`
	MetaDescription string                      `json:"metaDescription,omitempty" validate:"max=160"`
	Keywords        []string                    `json:"keywords,omitempty"`
	TableOfContents string                      `json:"tableOfContents,omitempty"`
	Difficulty      string                      `json:"difficulty,omitempty" validate:"oneof=BEGINNER INTERMEDIATE ADVANCED"`
	AuthorID        uuid.UUID                   `json:"authorId" validate:"required"`
	ParentID        *uuid.UUID                  `json:"parentId,omitempty"`
}

// Validate validates the create document request
func (r *CreateDocumentRequest) Validate() error {
	if r.Title == "" {
		return errors.New("title is required")
	}
	if r.Content == "" {
		return errors.New("content is required")
	}
	if r.AuthorID == uuid.Nil {
		return errors.New("authorId is required")
	}
	return nil
}

// UpdateDocumentRequest represents a request to update a document
type UpdateDocumentRequest struct {
	Title           *string    `json:"title,omitempty" validate:"omitempty,max=500"`
	Content         *string    `json:"content,omitempty"`
	Summary         *string    `json:"summary,omitempty" validate:"omitempty,max=1000"`
	Tags            *[]string  `json:"tags,omitempty"`
	MetaTitle       *string    `json:"metaTitle,omitempty" validate:"omitempty,max=60"`
	MetaDescription *string    `json:"metaDescription,omitempty" validate:"omitempty,max=160"`
	Keywords        *[]string  `json:"keywords,omitempty"`
	TableOfContents *string    `json:"tableOfContents,omitempty"`
	Difficulty      *string    `json:"difficulty,omitempty" validate:"omitempty,oneof=BEGINNER INTERMEDIATE ADVANCED"`
	UserID          uuid.UUID  `json:"userId" validate:"required"`
	UserRole        string     `json:"userRole" validate:"required"`
}

// SearchDocumentsRequest represents a request to search documents
type SearchDocumentsRequest struct {
	Query      string                        `json:"query,omitempty"`
	Categories []entities.DocumentCategory   `json:"categories,omitempty"`
	Types      []entities.DocumentType       `json:"types,omitempty"`
	Audiences  []entities.AudienceType       `json:"audiences,omitempty"`
	Tags       []string                      `json:"tags,omitempty"`
	DateFrom   *time.Time                    `json:"dateFrom,omitempty"`
	DateTo     *time.Time                    `json:"dateTo,omitempty"`
	MinRating  *float64                      `json:"minRating,omitempty"`
	SortBy     string                        `json:"sortBy,omitempty" validate:"omitempty,oneof=title created_at updated_at view_count rating"`
	SortOrder  string                        `json:"sortOrder,omitempty" validate:"omitempty,oneof=asc desc"`
	Limit      int                           `json:"limit,omitempty" validate:"omitempty,min=1,max=100"`
	Offset     int                           `json:"offset,omitempty" validate:"omitempty,min=0"`
}

// SemanticSearchRequest represents a request for semantic search
type SemanticSearchRequest struct {
	Query      string                        `json:"query" validate:"required"`
	Categories []entities.DocumentCategory   `json:"categories,omitempty"`
	Audiences  []entities.AudienceType       `json:"audiences,omitempty"`
	Limit      int                           `json:"limit,omitempty" validate:"omitempty,min=1,max=50"`
	Threshold  float64                       `json:"threshold,omitempty" validate:"omitempty,min=0,max=1"`
}

// DocumentResponse represents a document in API responses
type DocumentResponse struct {
	ID              uuid.UUID                 `json:"id"`
	Title           string                    `json:"title"`
	Content         string                    `json:"content"`
	Summary         string                    `json:"summary"`
	Type            entities.DocumentType     `json:"type"`
	Category        entities.DocumentCategory `json:"category"`
	Audience        entities.AudienceType     `json:"audience"`
	Status          entities.DocumentStatus   `json:"status"`
	Tags            []string                  `json:"tags"`
	Slug            string                    `json:"slug"`
	MetaTitle       string                    `json:"metaTitle"`
	MetaDescription string                    `json:"metaDescription"`
	Keywords        []string                  `json:"keywords"`
	TableOfContents string                    `json:"tableOfContents"`
	ReadingTime     int                       `json:"readingTime"`
	Difficulty      string                    `json:"difficulty"`
	Version         string                    `json:"version"`
	VersionNotes    string                    `json:"versionNotes"`
	ViewCount       int                       `json:"viewCount"`
	LikeCount       int                       `json:"likeCount"`
	ShareCount      int                       `json:"shareCount"`
	AuthorID        uuid.UUID                 `json:"authorId"`
	ReviewerID      *uuid.UUID                `json:"reviewerId,omitempty"`
	ParentID        *uuid.UUID                `json:"parentId,omitempty"`
	CreatedAt       time.Time                 `json:"createdAt"`
	UpdatedAt       time.Time                 `json:"updatedAt"`
	PublishedAt     *time.Time                `json:"publishedAt,omitempty"`
	LastViewedAt    *time.Time                `json:"lastViewedAt,omitempty"`
	Author          *UserResponse             `json:"author,omitempty"`
	Reviewer        *UserResponse             `json:"reviewer,omitempty"`
	Parent          *DocumentResponse         `json:"parent,omitempty"`
	Children        []DocumentResponse        `json:"children,omitempty"`
}

// SearchDocumentsResponse represents a search results response
type SearchDocumentsResponse struct {
	Results []*DocumentResponse `json:"results"`
	Total   int                 `json:"total"`
	Query   string              `json:"query"`
	Limit   int                 `json:"limit"`
	Offset  int                 `json:"offset"`
}

// DocumentAnalyticsResponse represents document analytics data
type DocumentAnalyticsResponse struct {
	DocumentID uuid.UUID                     `json:"documentId"`
	Stats      *repositories.DocumentStats   `json:"stats"`
	Analytics  []entities.DocumentAnalytic   `json:"analytics"`
	Period     TimePeriod                    `json:"period"`
}

// CreateFAQRequest represents a request to create a new FAQ
type CreateFAQRequest struct {
	Question    string                      `json:"question" validate:"required,max=1000"`
	Answer      string                      `json:"answer" validate:"required"`
	Category    entities.DocumentCategory   `json:"category" validate:"required"`
	Audience    entities.AudienceType       `json:"audience" validate:"required"`
	Tags        []string                    `json:"tags,omitempty"`
	Keywords    []string                    `json:"keywords,omitempty"`
	Priority    entities.FAQPriority        `json:"priority,omitempty"`
	AuthorID    uuid.UUID                   `json:"authorId" validate:"required"`
	SourceType  string                      `json:"sourceType,omitempty"`
	SourceID    *uuid.UUID                  `json:"sourceId,omitempty"`
	SourceData  string                      `json:"sourceData,omitempty"`
}

// Validate validates the create FAQ request
func (r *CreateFAQRequest) Validate() error {
	if r.Question == "" {
		return errors.New("question is required")
	}
	if r.Answer == "" {
		return errors.New("answer is required")
	}
	if r.AuthorID == uuid.Nil {
		return errors.New("authorId is required")
	}
	return nil
}

// UpdateFAQRequest represents a request to update a FAQ
type UpdateFAQRequest struct {
	Question *string                     `json:"question,omitempty" validate:"omitempty,max=1000"`
	Answer   *string                     `json:"answer,omitempty"`
	Tags     *[]string                   `json:"tags,omitempty"`
	Keywords *[]string                   `json:"keywords,omitempty"`
	Priority *entities.FAQPriority       `json:"priority,omitempty"`
	UserID   uuid.UUID                   `json:"userId" validate:"required"`
	UserRole string                      `json:"userRole" validate:"required"`
}

// SearchFAQsRequest represents a request to search FAQs
type SearchFAQsRequest struct {
	Query      string                        `json:"query,omitempty"`
	Categories []entities.DocumentCategory   `json:"categories,omitempty"`
	Audiences  []entities.AudienceType       `json:"audiences,omitempty"`
	Priorities []entities.FAQPriority        `json:"priorities,omitempty"`
	Tags       []string                      `json:"tags,omitempty"`
	DateFrom   *time.Time                    `json:"dateFrom,omitempty"`
	DateTo     *time.Time                    `json:"dateTo,omitempty"`
	MinScore   *float64                      `json:"minScore,omitempty"`
	SortBy     string                        `json:"sortBy,omitempty" validate:"omitempty,oneof=score popularity created_at updated_at"`
	SortOrder  string                        `json:"sortOrder,omitempty" validate:"omitempty,oneof=asc desc"`
	Limit      int                           `json:"limit,omitempty" validate:"omitempty,min=1,max=100"`
	Offset     int                           `json:"offset,omitempty" validate:"omitempty,min=0"`
}

// FAQResponse represents a FAQ in API responses
type FAQResponse struct {
	ID               uuid.UUID                 `json:"id"`
	Question         string                    `json:"question"`
	Answer           string                    `json:"answer"`
	Category         entities.DocumentCategory `json:"category"`
	Audience         entities.AudienceType     `json:"audience"`
	Tags             []string                  `json:"tags"`
	Keywords         []string                  `json:"keywords"`
	Status           entities.FAQStatus        `json:"status"`
	Priority         entities.FAQPriority      `json:"priority"`
	ViewCount        int                       `json:"viewCount"`
	HelpfulCount     int                       `json:"helpfulCount"`
	UnhelpfulCount   int                       `json:"unhelpfulCount"`
	SearchCount      int                       `json:"searchCount"`
	ClickCount       int                       `json:"clickCount"`
	PopularityScore  float64                   `json:"popularityScore"`
	RelevanceScore   float64                   `json:"relevanceScore"`
	FreshnessScore   float64                   `json:"freshnessScore"`
	OverallScore     float64                   `json:"overallScore"`
	RelatedFAQs      []uuid.UUID               `json:"relatedFaqs"`
	RelatedDocuments []uuid.UUID               `json:"relatedDocuments"`
	SourceType       string                    `json:"sourceType"`
	SourceID         *uuid.UUID                `json:"sourceId,omitempty"`
	AuthorID         uuid.UUID                 `json:"authorId"`
	ReviewerID       *uuid.UUID                `json:"reviewerId,omitempty"`
	CreatedAt        time.Time                 `json:"createdAt"`
	UpdatedAt        time.Time                 `json:"updatedAt"`
	PublishedAt      *time.Time                `json:"publishedAt,omitempty"`
	LastViewedAt     *time.Time                `json:"lastViewedAt,omitempty"`
	LastUpdatedByAI  *time.Time                `json:"lastUpdatedByAI,omitempty"`
	Author           *UserResponse             `json:"author,omitempty"`
	Reviewer         *UserResponse             `json:"reviewer,omitempty"`
}

// SearchFAQsResponse represents a FAQ search results response
type SearchFAQsResponse struct {
	Results []*FAQResponse `json:"results"`
	Total   int            `json:"total"`
	Query   string         `json:"query"`
	Limit   int            `json:"limit"`
	Offset  int            `json:"offset"`
}

// FAQAnalyticsResponse represents FAQ analytics data
type FAQAnalyticsResponse struct {
	FAQID     uuid.UUID                   `json:"faqId"`
	Stats     *repositories.FAQStats      `json:"stats"`
	Analytics []entities.FAQAnalytic      `json:"analytics"`
	Period    TimePeriod                  `json:"period"`
}

// RateFAQRequest represents a request to rate a FAQ
type RateFAQRequest struct {
	FAQID     uuid.UUID `json:"faqId" validate:"required"`
	SessionID string    `json:"sessionId" validate:"required"`
	IsHelpful bool      `json:"isHelpful"`
	Feedback  string    `json:"feedback,omitempty"`
	UserID    *uuid.UUID `json:"userId,omitempty"`
}

// UserResponse represents a user in API responses
type UserResponse struct {
	ID     uuid.UUID `json:"id"`
	Name   string    `json:"name"`
	Email  string    `json:"email"`
	Role   string    `json:"role"`
	Avatar string    `json:"avatar"`
}

// TimePeriod represents a time period
type TimePeriod struct {
	From time.Time `json:"from"`
	To   time.Time `json:"to"`
}

// AnalyticsFilter represents filters for analytics queries
type AnalyticsFilter struct {
	Categories   []entities.DocumentCategory `json:"categories,omitempty"`
	Audiences    []entities.AudienceType     `json:"audiences,omitempty"`
	UserIDs      []uuid.UUID                 `json:"userIds,omitempty"`
	ContentTypes []string                    `json:"contentTypes,omitempty"`
	From         time.Time                   `json:"from"`
	To           time.Time                   `json:"to"`
	Timeframe    string                      `json:"timeframe,omitempty"`
}

// AnalyticsResponse represents general analytics data
type AnalyticsResponse struct {
	DashboardStats    *repositories.DashboardStats `json:"dashboardStats,omitempty"`
	TopSearchQueries  []repositories.SearchQuery   `json:"topSearchQueries,omitempty"`
	PopularResources  []repositories.ResourceStats `json:"popularResources,omitempty"`
	UserActivities    []repositories.UserActivity  `json:"userActivities,omitempty"`
	Period            TimePeriod                    `json:"period"`
	GeneratedAt       time.Time                     `json:"generatedAt"`
}

// Helper functions to convert entities to DTOs

// DocumentToResponse converts a Document entity to DocumentResponse DTO
func DocumentToResponse(doc *entities.Document) *DocumentResponse {
	if doc == nil {
		return nil
	}

	resp := &DocumentResponse{
		ID:              doc.ID,
		Title:           doc.Title,
		Content:         doc.Content,
		Summary:         doc.Summary,
		Type:            doc.Type,
		Category:        doc.Category,
		Audience:        doc.Audience,
		Status:          doc.Status,
		Tags:            doc.Tags,
		Slug:            doc.Slug,
		MetaTitle:       doc.MetaTitle,
		MetaDescription: doc.MetaDescription,
		Keywords:        doc.Keywords,
		TableOfContents: doc.TableOfContents,
		ReadingTime:     doc.ReadingTime,
		Difficulty:      doc.Difficulty,
		Version:         doc.Version,
		VersionNotes:    doc.VersionNotes,
		ViewCount:       doc.ViewCount,
		LikeCount:       doc.LikeCount,
		ShareCount:      doc.ShareCount,
		AuthorID:        doc.AuthorID,
		ReviewerID:      doc.ReviewerID,
		ParentID:        doc.ParentID,
		CreatedAt:       doc.CreatedAt,
		UpdatedAt:       doc.UpdatedAt,
		PublishedAt:     doc.PublishedAt,
		LastViewedAt:    doc.LastViewedAt,
	}

	// Convert related entities if loaded
	if doc.Author != nil {
		resp.Author = UserToResponse(doc.Author)
	}
	if doc.Reviewer != nil {
		resp.Reviewer = UserToResponse(doc.Reviewer)
	}
	if doc.Parent != nil {
		resp.Parent = DocumentToResponse(doc.Parent)
	}
	if len(doc.Children) > 0 {
		resp.Children = make([]DocumentResponse, len(doc.Children))
		for i, child := range doc.Children {
			childResp := DocumentToResponse(&child)
			if childResp != nil {
				resp.Children[i] = *childResp
			}
		}
	}

	return resp
}

// FAQToResponse converts a FAQ entity to FAQResponse DTO
func FAQToResponse(faq *entities.FAQ) *FAQResponse {
	if faq == nil {
		return nil
	}

	resp := &FAQResponse{
		ID:               faq.ID,
		Question:         faq.Question,
		Answer:           faq.Answer,
		Category:         faq.Category,
		Audience:         faq.Audience,
		Tags:             faq.Tags,
		Keywords:         faq.Keywords,
		Status:           faq.Status,
		Priority:         faq.Priority,
		ViewCount:        faq.ViewCount,
		HelpfulCount:     faq.HelpfulCount,
		UnhelpfulCount:   faq.UnhelpfulCount,
		SearchCount:      faq.SearchCount,
		ClickCount:       faq.ClickCount,
		PopularityScore:  faq.PopularityScore,
		RelevanceScore:   faq.RelevanceScore,
		FreshnessScore:   faq.FreshnessScore,
		OverallScore:     faq.OverallScore,
		RelatedFAQs:      faq.RelatedFAQs,
		RelatedDocuments: faq.RelatedDocuments,
		SourceType:       faq.SourceType,
		SourceID:         faq.SourceID,
		AuthorID:         faq.AuthorID,
		ReviewerID:       faq.ReviewerID,
		CreatedAt:        faq.CreatedAt,
		UpdatedAt:        faq.UpdatedAt,
		PublishedAt:      faq.PublishedAt,
		LastViewedAt:     faq.LastViewedAt,
		LastUpdatedByAI:  faq.LastUpdatedByAI,
	}

	// Convert related entities if loaded
	if faq.Author != nil {
		resp.Author = UserToResponse(faq.Author)
	}
	if faq.Reviewer != nil {
		resp.Reviewer = UserToResponse(faq.Reviewer)
	}

	return resp
}

// UserToResponse converts a User entity to UserResponse DTO
func UserToResponse(user *entities.User) *UserResponse {
	if user == nil {
		return nil
	}

	return &UserResponse{
		ID:     user.ID,
		Name:   user.Name,
		Email:  user.Email,
		Role:   user.Role,
		Avatar: user.Avatar,
	}
}
