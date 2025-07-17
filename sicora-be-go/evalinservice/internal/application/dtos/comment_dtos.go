package dtos

import (
	"time"

	"github.com/google/uuid"
)

type CommentCreateRequest struct {
	EvaluationID uuid.UUID `json:"evaluation_id" binding:"required"`
	Content      string    `json:"content" binding:"required,min=1,max=2000"`
	Rating       *int      `json:"rating" binding:"omitempty,min=1,max=5"`
	IsPrivate    bool      `json:"is_private"`
}

type CommentUpdateRequest struct {
	Content   string `json:"content" binding:"required,min=1,max=2000"`
	Rating    *int   `json:"rating" binding:"omitempty,min=1,max=5"`
	IsPrivate bool   `json:"is_private"`
}

type CommentResponse struct {
	ID           uuid.UUID `json:"id"`
	EvaluationID uuid.UUID `json:"evaluation_id"`
	UserID       uuid.UUID `json:"user_id"`
	Content      string    `json:"content"`
	Rating       *int      `json:"rating"`
	IsPrivate    bool      `json:"is_private"`
	CreatedAt    time.Time `json:"created_at"`
	UpdatedAt    time.Time `json:"updated_at"`
	UserName     string    `json:"user_name,omitempty"`
	UserEmail    string    `json:"user_email,omitempty"`
}

type CommentFilterRequest struct {
	EvaluationID *uuid.UUID `form:"evaluation_id"`
	UserID       *uuid.UUID `form:"user_id"`
	IsPrivate    *bool      `form:"is_private"`
	HasRating    *bool      `form:"has_rating"`
	MinRating    *int       `form:"min_rating" binding:"omitempty,min=1,max=5"`
	MaxRating    *int       `form:"max_rating" binding:"omitempty,min=1,max=5"`
	StartDate    *string    `form:"start_date"`
	EndDate      *string    `form:"end_date"`
	Page         int        `form:"page" binding:"min=1"`
	PageSize     int        `form:"page_size" binding:"min=1,max=100"`
}

type CommentStatsResponse struct {
	TotalComments   int64   `json:"total_comments"`
	PublicComments  int64   `json:"public_comments"`
	PrivateComments int64   `json:"private_comments"`
	RatedComments   int64   `json:"rated_comments"`
	AverageRating   float64 `json:"average_rating"`
	CommentsPerDay  float64 `json:"comments_per_day"`
}

type CommentBulkDeleteRequest struct {
	CommentIDs []uuid.UUID `json:"comment_ids" binding:"required"`
}
