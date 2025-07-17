package entities

import (
	"time"

	"github.com/google/uuid"
)

type Comment struct {
	ID           uuid.UUID `json:"id" gorm:"type:uuid;primary_key;default:gen_random_uuid()"`
	EvaluationID uuid.UUID `json:"evaluation_id" gorm:"type:uuid;not null;index"`
	UserID       uuid.UUID `json:"user_id" gorm:"type:uuid;not null;index"`
	Content      string    `json:"content" gorm:"type:text;not null"`
	Rating       *int      `json:"rating" gorm:"type:integer;check:rating >= 1 AND rating <= 5"`
	IsPrivate    bool      `json:"is_private" gorm:"default:false"`
	CreatedAt    time.Time `json:"created_at" gorm:"not null;default:CURRENT_TIMESTAMP"`
	UpdatedAt    time.Time `json:"updated_at" gorm:"not null;default:CURRENT_TIMESTAMP"`

	Evaluation *Evaluation `json:"evaluation,omitempty" gorm:"foreignKey:EvaluationID;constraint:OnUpdate:CASCADE,OnDelete:CASCADE"`
}

func NewComment(evaluationID, userID uuid.UUID, content string, rating *int, isPrivate bool) *Comment {
	return &Comment{
		ID:           uuid.New(),
		EvaluationID: evaluationID,
		UserID:       userID,
		Content:      content,
		Rating:       rating,
		IsPrivate:    isPrivate,
		CreatedAt:    time.Now(),
		UpdatedAt:    time.Now(),
	}
}

func (c *Comment) UpdateContent(content string) {
	c.Content = content
	c.UpdatedAt = time.Now()
}

func (c *Comment) UpdateRating(rating *int) {
	c.Rating = rating
	c.UpdatedAt = time.Now()
}

func (c *Comment) SetPrivacy(isPrivate bool) {
	c.IsPrivate = isPrivate
	c.UpdatedAt = time.Now()
}

func (c *Comment) IsValid() bool {
	if c.Content == "" {
		return false
	}
	if c.Rating != nil && (*c.Rating < 1 || *c.Rating > 5) {
		return false
	}
	return true
}
