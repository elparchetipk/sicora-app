package entities

import (
	"time"

	"github.com/google/uuid"
)

type Configuration struct {
	ID          uuid.UUID `json:"id" gorm:"type:uuid;primary_key;default:gen_random_uuid()"`
	Key         string    `json:"key" gorm:"type:varchar(100);not null;unique;index"`
	Value       string    `json:"value" gorm:"type:text;not null"`
	Description string    `json:"description" gorm:"type:text"`
	Category    string    `json:"category" gorm:"type:varchar(50);not null;index"`
	IsActive    bool      `json:"is_active" gorm:"default:true"`
	IsEditable  bool      `json:"is_editable" gorm:"default:true"`
	CreatedBy   uuid.UUID `json:"created_by" gorm:"type:uuid;not null;index"`
	UpdatedBy   uuid.UUID `json:"updated_by" gorm:"type:uuid;not null;index"`
	CreatedAt   time.Time `json:"created_at" gorm:"not null;default:CURRENT_TIMESTAMP"`
	UpdatedAt   time.Time `json:"updated_at" gorm:"not null;default:CURRENT_TIMESTAMP"`
}

func NewConfiguration(key, value, description, category string, createdBy uuid.UUID) *Configuration {
	return &Configuration{
		ID:          uuid.New(),
		Key:         key,
		Value:       value,
		Description: description,
		Category:    category,
		IsActive:    true,
		IsEditable:  true,
		CreatedBy:   createdBy,
		UpdatedBy:   createdBy,
		CreatedAt:   time.Now(),
		UpdatedAt:   time.Now(),
	}
}

func (c *Configuration) UpdateValue(value string, updatedBy uuid.UUID) {
	if c.IsEditable {
		c.Value = value
		c.UpdatedBy = updatedBy
		c.UpdatedAt = time.Now()
	}
}

func (c *Configuration) SetActive(isActive bool, updatedBy uuid.UUID) {
	c.IsActive = isActive
	c.UpdatedBy = updatedBy
	c.UpdatedAt = time.Now()
}

func (c *Configuration) SetEditable(isEditable bool, updatedBy uuid.UUID) {
	c.IsEditable = isEditable
	c.UpdatedBy = updatedBy
	c.UpdatedAt = time.Now()
}

func (c *Configuration) IsValid() bool {
	return c.Key != "" && c.Value != "" && c.Category != ""
}
