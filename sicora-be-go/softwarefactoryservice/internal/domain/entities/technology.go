package entities

import (
	"time"

	"github.com/google/uuid"
)

// TechnologyCategory representa la categoría de una tecnología
type TechnologyCategory string

const (
	CategoryFrontend  TechnologyCategory = "frontend"
	CategoryBackend   TechnologyCategory = "backend"
	CategoryDatabase  TechnologyCategory = "database"
	CategoryDevOps    TechnologyCategory = "devops"
	CategoryTesting   TechnologyCategory = "testing"
	CategoryMobile    TechnologyCategory = "mobile"
	CategoryTools     TechnologyCategory = "tools"
)

// TechnologyLevel representa el nivel de dificultad de una tecnología
type TechnologyLevel string

const (
	LevelBeginner     TechnologyLevel = "beginner"
	LevelIntermediate TechnologyLevel = "intermediate"
	LevelAdvanced     TechnologyLevel = "advanced"
	LevelExpert       TechnologyLevel = "expert"
)

// LicenseType representa el tipo de licencia de una tecnología
type LicenseType string

const (
	LicenseOpenSource   LicenseType = "opensource"
	LicenseEducational  LicenseType = "educational"
	LicenseCommercial   LicenseType = "commercial"
	LicenseFree         LicenseType = "free"
)

// TechnologyStatus representa el estado de una tecnología en el catálogo
type TechnologyStatus string

const (
	TechnologyActive     TechnologyStatus = "active"
	TechnologyDeprecated TechnologyStatus = "deprecated"
	TechnologyExperimental TechnologyStatus = "experimental"
	TechnologyPlanned    TechnologyStatus = "planned"
)

// Technology representa una tecnología en el catálogo de la fábrica
type Technology struct {
	ID                uuid.UUID          `json:"id" gorm:"type:uuid;primary_key;default:gen_random_uuid()"`
	Name              string             `json:"name" gorm:"not null;size:100;uniqueIndex" validate:"required,min=2,max=100"`
	Version           string             `json:"version" gorm:"not null;size:50" validate:"required"`
	Category          TechnologyCategory `json:"category" gorm:"type:varchar(20)" validate:"required"`
	Level             TechnologyLevel    `json:"level" gorm:"type:varchar(20)" validate:"required"`
	Description       string             `json:"description" gorm:"type:text" validate:"required,min=10"`
	LicenseType       LicenseType        `json:"license_type" gorm:"type:varchar(20)" validate:"required"`
	Status            TechnologyStatus   `json:"status" gorm:"type:varchar(20);default:'active'"`
	LogoURL           string             `json:"logo_url" gorm:"size:512"`
	DocumentationURL  string             `json:"documentation_url" gorm:"size:512"`
	LearningResources []LearningResource `json:"learning_resources" gorm:"serializer:json"`
	Tags              []string           `json:"tags" gorm:"type:text[]"`
	Compatibility     []string           `json:"compatibility" gorm:"type:text[]"` // Compatible technology IDs
	Prerequisites     []string           `json:"prerequisites" gorm:"type:text[]"` // Required knowledge/technologies
	LicenseLimit      int                `json:"license_limit" gorm:"default:0"` // 0 = unlimited
	LicenseUsed       int                `json:"license_used" gorm:"default:0"`
	RenewalDate       *time.Time         `json:"renewal_date,omitempty"`
	Cost              float64            `json:"cost" gorm:"default:0.0"` // Cost per license
	PopularityScore   int                `json:"popularity_score" gorm:"default:0"` // Usage metrics
	CreatedBy         uuid.UUID          `json:"created_by" gorm:"type:uuid;not null"`
	CreatedAt         time.Time          `json:"created_at" gorm:"autoCreateTime"`
	UpdatedAt         time.Time          `json:"updated_at" gorm:"autoUpdateTime"`
	
	// Relationships
	UsageStats        []TechnologyUsage  `json:"usage_stats,omitempty" gorm:"foreignKey:TechnologyID"`
}

// LearningResource representa un recurso de aprendizaje para una tecnología
type LearningResource struct {
	Type        string `json:"type"` // tutorial, course, documentation, video, book
	Title       string `json:"title"`
	URL         string `json:"url"`
	Duration    string `json:"duration,omitempty"` // "2h 30m", "5 days", etc.
	Level       string `json:"level"` // beginner, intermediate, advanced
	Language    string `json:"language"` // es, en, fr, etc.
	IsFree      bool   `json:"is_free"`
	Rating      float64 `json:"rating,omitempty"` // 1-5 stars
}

// TechnologyUsage representa el uso de una tecnología en proyectos
type TechnologyUsage struct {
	ID           uuid.UUID `json:"id" gorm:"type:uuid;primary_key;default:gen_random_uuid()"`
	TechnologyID uuid.UUID `json:"technology_id" gorm:"type:uuid;not null"`
	ProjectID    uuid.UUID `json:"project_id" gorm:"type:uuid;not null"`
	TeamID       uuid.UUID `json:"team_id" gorm:"type:uuid;not null"`
	StartDate    time.Time `json:"start_date" gorm:"not null"`
	EndDate      *time.Time `json:"end_date,omitempty"`
	SuccessRate  float64   `json:"success_rate" gorm:"default:0.0"` // 0-100%
	Satisfaction int       `json:"satisfaction" gorm:"default:0"` // 1-5 rating
	Feedback     string    `json:"feedback" gorm:"type:text"`
	CreatedAt    time.Time `json:"created_at" gorm:"autoCreateTime"`
	
	// Relationships
	Technology   Technology `json:"technology,omitempty" gorm:"foreignKey:TechnologyID"`
	Project      Project    `json:"project,omitempty" gorm:"foreignKey:ProjectID"`
	Team         Team       `json:"team,omitempty" gorm:"foreignKey:TeamID"`
}

// TechnologyRoadmap representa la planificación de adopción de tecnologías
type TechnologyRoadmap struct {
	ID                uuid.UUID        `json:"id" gorm:"type:uuid;primary_key;default:gen_random_uuid()"`
	TechnologyID      uuid.UUID        `json:"technology_id" gorm:"type:uuid;not null"`
	Quarter           string           `json:"quarter" gorm:"not null;size:10"` // "2025-Q1"
	AdoptionPhase     AdoptionPhase    `json:"adoption_phase" gorm:"type:varchar(20)"`
	TargetProjects    int              `json:"target_projects" gorm:"default:1"`
	RequiredTraining  []TrainingItem   `json:"required_training" gorm:"serializer:json"`
	SuccessCriteria   []string         `json:"success_criteria" gorm:"type:text[]"`
	RiskAssessment    RiskAssessment   `json:"risk_assessment" gorm:"embedded;embeddedPrefix:risk_"`
	Status            RoadmapStatus    `json:"status" gorm:"type:varchar(20);default:'planned'"`
	Progress          int              `json:"progress" gorm:"default:0"` // 0-100%
	ResponsibleTeam   string           `json:"responsible_team" gorm:"size:100"`
	CreatedAt         time.Time        `json:"created_at" gorm:"autoCreateTime"`
	UpdatedAt         time.Time        `json:"updated_at" gorm:"autoUpdateTime"`
	
	// Relationships
	Technology        Technology       `json:"technology,omitempty" gorm:"foreignKey:TechnologyID"`
}

// AdoptionPhase representa la fase de adopción de una tecnología
type AdoptionPhase string

const (
	PhaseExploration AdoptionPhase = "exploration"
	PhasePilot       AdoptionPhase = "pilot"
	PhaseAdoption    AdoptionPhase = "adoption"
	PhaseDeprecation AdoptionPhase = "deprecation"
)

// TrainingItem representa un elemento de capacitación requerido
type TrainingItem struct {
	Topic       string `json:"topic"`
	Duration    string `json:"duration"`
	Type        string `json:"type"` // workshop, course, self-study
	Instructor  string `json:"instructor,omitempty"`
	IsCompleted bool   `json:"is_completed"`
}

// RiskAssessment representa la evaluación de riesgos
type RiskAssessment struct {
	TechnicalRisk     int      `json:"technical_risk" gorm:"column:risk_technical_risk"` // 1-5
	LearningCurveRisk int      `json:"learning_curve_risk" gorm:"column:risk_learning_curve_risk"` // 1-5
	SupportRisk       int      `json:"support_risk" gorm:"column:risk_support_risk"` // 1-5
	MitigationActions []string `json:"mitigation_actions" gorm:"column:risk_mitigation_actions;type:text[]"`
}

// RoadmapStatus representa el estado del roadmap
type RoadmapStatus string

const (
	RoadmapPlanned     RoadmapStatus = "planned"
	RoadmapInProgress  RoadmapStatus = "in_progress"
	RoadmapCompleted   RoadmapStatus = "completed"
	RoadmapPostponed   RoadmapStatus = "postponed"
	RoadmapCancelled   RoadmapStatus = "cancelled"
)

// TableName especifica el nombre de la tabla para GORM
func (Technology) TableName() string {
	return "factory_technologies"
}

// TableName especifica el nombre de la tabla para GORM
func (TechnologyUsage) TableName() string {
	return "factory_technology_usage"
}

// TableName especifica el nombre de la tabla para GORM
func (TechnologyRoadmap) TableName() string {
	return "factory_technology_roadmap"
}

// Validate valida las reglas de negocio de la tecnología
func (t *Technology) Validate() error {
	if t.LicenseLimit > 0 && t.LicenseUsed > t.LicenseLimit {
		return &ValidationError{Field: "license_used", Message: "license usage cannot exceed limit"}
	}
	
	if t.PopularityScore < 0 || t.PopularityScore > 100 {
		return &ValidationError{Field: "popularity_score", Message: "popularity score must be between 0 and 100"}
	}
	
	return nil
}

// IsActive verifica si la tecnología está activa
func (t *Technology) IsActive() bool {
	return t.Status == TechnologyActive
}

// IsAvailable verifica si hay licencias disponibles
func (t *Technology) IsAvailable() bool {
	if t.LicenseLimit == 0 {
		return true // Unlimited
	}
	return t.LicenseUsed < t.LicenseLimit
}

// GetAvailableLicenses retorna el número de licencias disponibles
func (t *Technology) GetAvailableLicenses() int {
	if t.LicenseLimit == 0 {
		return -1 // Unlimited
	}
	available := t.LicenseLimit - t.LicenseUsed
	if available < 0 {
		return 0
	}
	return available
}

// NeedsRenewal verifica si la tecnología necesita renovación de licencia
func (t *Technology) NeedsRenewal() bool {
	if t.RenewalDate == nil {
		return false
	}
	
	// Alert 30 days before renewal
	alertDate := t.RenewalDate.AddDate(0, 0, -30)
	return time.Now().After(alertDate)
}

// IsCompatibleWith verifica si es compatible con otra tecnología
func (t *Technology) IsCompatibleWith(technologyID string) bool {
	for _, compatible := range t.Compatibility {
		if compatible == technologyID {
			return true
		}
	}
	return false
}

// IncreaseLicenseUsage incrementa el uso de licencias
func (t *Technology) IncreaseLicenseUsage() error {
	if !t.IsAvailable() {
		return &BusinessRuleError{Rule: "license_limit", Message: "no licenses available"}
	}
	
	t.LicenseUsed++
	return nil
}

// DecreaseLicenseUsage decrementa el uso de licencias
func (t *Technology) DecreaseLicenseUsage() {
	if t.LicenseUsed > 0 {
		t.LicenseUsed--
	}
}

// UpdatePopularityScore actualiza el score de popularidad basado en uso
func (t *Technology) UpdatePopularityScore(usageCount int) {
	// Simple algorithm: more usage = higher popularity
	t.PopularityScore = usageCount * 5
	if t.PopularityScore > 100 {
		t.PopularityScore = 100
	}
}

// Validate valida las reglas de negocio del uso de tecnología
func (tu *TechnologyUsage) Validate() error {
	if tu.SuccessRate < 0 || tu.SuccessRate > 100 {
		return &ValidationError{Field: "success_rate", Message: "success rate must be between 0 and 100"}
	}
	
	if tu.Satisfaction < 1 || tu.Satisfaction > 5 {
		return &ValidationError{Field: "satisfaction", Message: "satisfaction must be between 1 and 5"}
	}
	
	if tu.EndDate != nil && tu.EndDate.Before(tu.StartDate) {
		return &ValidationError{Field: "end_date", Message: "end date cannot be before start date"}
	}
	
	return nil
}

// IsActive verifica si el uso de tecnología está activo
func (tu *TechnologyUsage) IsActive() bool {
	return tu.EndDate == nil
}

// GetDuration calcula la duración del uso
func (tu *TechnologyUsage) GetDuration() time.Duration {
	if tu.EndDate == nil {
		return time.Since(tu.StartDate)
	}
	return tu.EndDate.Sub(tu.StartDate)
}

// Validate valida las reglas de negocio del roadmap
func (tr *TechnologyRoadmap) Validate() error {
	if tr.Progress < 0 || tr.Progress > 100 {
		return &ValidationError{Field: "progress", Message: "progress must be between 0 and 100"}
	}
	
	if tr.TargetProjects < 1 {
		return &ValidationError{Field: "target_projects", Message: "target projects must be at least 1"}
	}
	
	// Validate risk assessment
	if tr.RiskAssessment.TechnicalRisk < 1 || tr.RiskAssessment.TechnicalRisk > 5 {
		return &ValidationError{Field: "risk_assessment.technical_risk", Message: "technical risk must be between 1 and 5"}
	}
	
	if tr.RiskAssessment.LearningCurveRisk < 1 || tr.RiskAssessment.LearningCurveRisk > 5 {
		return &ValidationError{Field: "risk_assessment.learning_curve_risk", Message: "learning curve risk must be between 1 and 5"}
	}
	
	if tr.RiskAssessment.SupportRisk < 1 || tr.RiskAssessment.SupportRisk > 5 {
		return &ValidationError{Field: "risk_assessment.support_risk", Message: "support risk must be between 1 and 5"}
	}
	
	return nil
}

// IsCompleted verifica si el roadmap está completado
func (tr *TechnologyRoadmap) IsCompleted() bool {
	return tr.Status == RoadmapCompleted || tr.Progress >= 100
}

// GetOverallRisk calcula el riesgo general del roadmap
func (tr *TechnologyRoadmap) GetOverallRisk() float64 {
	return float64(tr.RiskAssessment.TechnicalRisk+tr.RiskAssessment.LearningCurveRisk+tr.RiskAssessment.SupportRisk) / 3.0
}

// UpdateProgress actualiza el progreso del roadmap
func (tr *TechnologyRoadmap) UpdateProgress() {
	if len(tr.RequiredTraining) == 0 {
		return
	}
	
	completedTraining := 0
	for _, training := range tr.RequiredTraining {
		if training.IsCompleted {
			completedTraining++
		}
	}
	
	tr.Progress = (completedTraining * 100) / len(tr.RequiredTraining)
	
	if tr.Progress >= 100 {
		tr.Status = RoadmapCompleted
	}
}
