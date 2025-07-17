package entities

import (
	"time"

	"github.com/google/uuid"
)

type Checklist struct {
	ID          uuid.UUID       `json:"id" gorm:"type:uuid;primary_key;default:gen_random_uuid()"`
	Name        string          `json:"name" gorm:"not null" validate:"required,min=5,max=200"`
	Description string          `json:"description" gorm:"type:text"`
	Version     string          `json:"version" gorm:"not null;default:'1.0'" validate:"required"`
	Trimester   int             `json:"trimester" gorm:"not null" validate:"required,min=2,max=7"`
	ProjectType string          `json:"project_type" gorm:"not null" validate:"required"`
	Program     string          `json:"program" gorm:"not null" validate:"required"` // ADSO, PSW
	Status      ChecklistStatus `json:"status" gorm:"type:varchar(20);not null;default:'draft'" validate:"required"`

	// Metadata
	CreatedBy  uuid.UUID  `json:"created_by" gorm:"type:uuid;not null" validate:"required"`
	ApprovedBy *uuid.UUID `json:"approved_by" gorm:"type:uuid"`
	CreatedAt  time.Time  `json:"created_at" gorm:"autoCreateTime"`
	UpdatedAt  time.Time  `json:"updated_at" gorm:"autoUpdateTime"`
	ApprovedAt *time.Time `json:"approved_at"`

	// Relationships
	Criteria []ChecklistCriterion `json:"criteria,omitempty" gorm:"foreignKey:ChecklistID;constraint:OnDelete:CASCADE"`
	Sessions []EvaluationSession  `json:"sessions,omitempty" gorm:"foreignKey:ChecklistID"`
}

type ChecklistCriterion struct {
	ID          uuid.UUID         `json:"id" gorm:"type:uuid;primary_key;default:gen_random_uuid()"`
	ChecklistID uuid.UUID         `json:"checklist_id" gorm:"type:uuid;not null" validate:"required"`
	Name        string            `json:"name" gorm:"not null" validate:"required,min=3,max=100"`
	Description string            `json:"description" gorm:"type:text;not null" validate:"required"`
	Category    CriterionCategory `json:"category" gorm:"type:varchar(30);not null" validate:"required"`
	Weight      float64           `json:"weight" gorm:"not null" validate:"required,min=0,max=100"`
	MaxScore    float64           `json:"max_score" gorm:"not null;default:100" validate:"required,min=0"`
	IsRequired  bool              `json:"is_required" gorm:"not null;default:true"`
	Order       int               `json:"order" gorm:"not null;default:1" validate:"min=1"`

	// Evaluation guidelines
	Rubric         string `json:"rubric" gorm:"type:text"`
	Examples       string `json:"examples" gorm:"type:text"`
	CommonMistakes string `json:"common_mistakes" gorm:"type:text"`

	// Relationships
	Checklist Checklist        `json:"checklist,omitempty" gorm:"foreignKey:ChecklistID"`
	Levels    []CriterionLevel `json:"levels,omitempty" gorm:"foreignKey:CriterionID;constraint:OnDelete:CASCADE"`
}

type CriterionLevel struct {
	ID          uuid.UUID `json:"id" gorm:"type:uuid;primary_key;default:gen_random_uuid()"`
	CriterionID uuid.UUID `json:"criterion_id" gorm:"type:uuid;not null" validate:"required"`
	Level       int       `json:"level" gorm:"not null" validate:"required,min=1,max=5"`
	Name        string    `json:"name" gorm:"not null" validate:"required,min=3,max=50"`
	Description string    `json:"description" gorm:"type:text;not null" validate:"required"`
	ScoreMin    float64   `json:"score_min" gorm:"not null" validate:"required,min=0"`
	ScoreMax    float64   `json:"score_max" gorm:"not null" validate:"required,min=0"`

	// Relationships
	Criterion ChecklistCriterion `json:"criterion,omitempty" gorm:"foreignKey:CriterionID"`
}

// Enums
type ChecklistStatus string

const (
	ChecklistStatusDraft    ChecklistStatus = "draft"
	ChecklistStatusReview   ChecklistStatus = "review"
	ChecklistStatusApproved ChecklistStatus = "approved"
	ChecklistStatusActive   ChecklistStatus = "active"
	ChecklistStatusArchived ChecklistStatus = "archived"
)

type CriterionCategory string

const (
	CriterionCategoryTechnical     CriterionCategory = "technical"
	CriterionCategoryFunctional    CriterionCategory = "functional"
	CriterionCategoryDocumentation CriterionCategory = "documentation"
	CriterionCategoryPresentation  CriterionCategory = "presentation"
	CriterionCategoryTeamwork      CriterionCategory = "teamwork"
	CriterionCategoryInnovation    CriterionCategory = "innovation"
	CriterionCategoryQuality       CriterionCategory = "quality"
	CriterionCategoryDeployment    CriterionCategory = "deployment"
	CriterionCategorySecurity      CriterionCategory = "security"
	CriterionCategoryPerformance   CriterionCategory = "performance"
	CriterionCategoryUsability     CriterionCategory = "usability"
)

// Methods
func (cs ChecklistStatus) String() string {
	return string(cs)
}

func (cs ChecklistStatus) IsValid() bool {
	switch cs {
	case ChecklistStatusDraft, ChecklistStatusReview, ChecklistStatusApproved, ChecklistStatusActive, ChecklistStatusArchived:
		return true
	default:
		return false
	}
}

func (cc CriterionCategory) String() string {
	return string(cc)
}

func (cc CriterionCategory) IsValid() bool {
	switch cc {
	case CriterionCategoryTechnical, CriterionCategoryFunctional, CriterionCategoryDocumentation, CriterionCategoryPresentation, CriterionCategoryTeamwork, CriterionCategoryInnovation, CriterionCategoryQuality, CriterionCategoryDeployment, CriterionCategorySecurity, CriterionCategoryPerformance, CriterionCategoryUsability:
		return true
	default:
		return false
	}
}

func (c *Checklist) CanBeModified() bool {
	return c.Status == ChecklistStatusDraft || c.Status == ChecklistStatusReview
}

func (c *Checklist) IsActive() bool {
	return c.Status == ChecklistStatusActive
}

func (c *Checklist) GetTotalWeight() float64 {
	total := 0.0
	for _, criterion := range c.Criteria {
		total += criterion.Weight
	}
	return total
}

func (c *Checklist) IsWeightValid() bool {
	return c.GetTotalWeight() == 100.0
}

func (c *Checklist) GetRequiredCriteria() []ChecklistCriterion {
	var required []ChecklistCriterion
	for _, criterion := range c.Criteria {
		if criterion.IsRequired {
			required = append(required, criterion)
		}
	}
	return required
}

func (c *Checklist) Approve(approverID uuid.UUID) {
	c.Status = ChecklistStatusApproved
	c.ApprovedBy = &approverID
	now := time.Now()
	c.ApprovedAt = &now
}

func (c *Checklist) Activate() {
	if c.Status == ChecklistStatusApproved {
		c.Status = ChecklistStatusActive
	}
}

func (c *Checklist) Archive() {
	c.Status = ChecklistStatusArchived
}

func (cc *ChecklistCriterion) GetLevelByScore(score float64) *CriterionLevel {
	for _, level := range cc.Levels {
		if score >= level.ScoreMin && score <= level.ScoreMax {
			return &level
		}
	}
	return nil
}

func (cc *ChecklistCriterion) GetMaxPossibleScore() float64 {
	if len(cc.Levels) == 0 {
		return cc.MaxScore
	}

	maxScore := 0.0
	for _, level := range cc.Levels {
		if level.ScoreMax > maxScore {
			maxScore = level.ScoreMax
		}
	}
	return maxScore
}
