package models

import (
	"time"

	"github.com/google/uuid"
	"gorm.io/gorm"
)

// Question representa el modelo GORM para preguntas
type Question struct {
	ID          uuid.UUID      `gorm:"type:uuid;primary_key;default:gen_random_uuid()" json:"id"`
	Text        string         `gorm:"type:text;not null" json:"text"`
	Description string         `gorm:"type:text" json:"description"`
	Type        string         `gorm:"type:varchar(50);not null" json:"type"`
	IsRequired  bool           `gorm:"default:false" json:"is_required"`
	IsActive    bool           `gorm:"default:true" json:"is_active"`
	Options     string         `gorm:"type:jsonb" json:"options"` // Stored as JSON
	Category    string         `gorm:"type:varchar(100);not null;index" json:"category"`
	CreatedAt   time.Time      `gorm:"not null;default:CURRENT_TIMESTAMP" json:"created_at"`
	UpdatedAt   time.Time      `gorm:"not null;default:CURRENT_TIMESTAMP" json:"updated_at"`
	DeletedAt   gorm.DeletedAt `gorm:"index" json:"deleted_at,omitempty"`

	// Relaciones
	QuestionnaireQuestions []QuestionnaireQuestion `gorm:"foreignKey:QuestionID;constraint:OnUpdate:CASCADE,OnDelete:CASCADE" json:"-"`
}

// TableName especifica el nombre de la tabla
func (Question) TableName() string {
	return "questions"
}

// Questionnaire representa el modelo GORM para cuestionarios
type Questionnaire struct {
	ID          uuid.UUID      `gorm:"type:uuid;primary_key;default:gen_random_uuid()" json:"id"`
	Name        string         `gorm:"type:varchar(255);not null" json:"name"`
	Description string         `gorm:"type:text" json:"description"`
	IsActive    bool           `gorm:"default:true" json:"is_active"`
	CreatedAt   time.Time      `gorm:"not null;default:CURRENT_TIMESTAMP" json:"created_at"`
	UpdatedAt   time.Time      `gorm:"not null;default:CURRENT_TIMESTAMP" json:"updated_at"`
	DeletedAt   gorm.DeletedAt `gorm:"index" json:"deleted_at,omitempty"`

	// Relaciones
	Questions   []QuestionnaireQuestion `gorm:"foreignKey:QuestionnaireID;constraint:OnUpdate:CASCADE,OnDelete:CASCADE" json:"questions"`
	Evaluations []Evaluation            `gorm:"foreignKey:QuestionnaireID;constraint:OnUpdate:CASCADE,OnDelete:RESTRICT" json:"-"`
}

// TableName especifica el nombre de la tabla
func (Questionnaire) TableName() string {
	return "questionnaires"
}

// QuestionnaireQuestion representa la tabla intermedia entre cuestionarios y preguntas
type QuestionnaireQuestion struct {
	ID              uuid.UUID `gorm:"type:uuid;primary_key;default:gen_random_uuid()" json:"id"`
	QuestionnaireID uuid.UUID `gorm:"type:uuid;not null;index" json:"questionnaire_id"`
	QuestionID      uuid.UUID `gorm:"type:uuid;not null;index" json:"question_id"`
	Order           int       `gorm:"not null;default:0" json:"order"`
	CreatedAt       time.Time `gorm:"not null;default:CURRENT_TIMESTAMP" json:"created_at"`

	// Relaciones
	Questionnaire *Questionnaire `gorm:"foreignKey:QuestionnaireID;constraint:OnUpdate:CASCADE,OnDelete:CASCADE" json:"questionnaire,omitempty"`
	Question      *Question      `gorm:"foreignKey:QuestionID;constraint:OnUpdate:CASCADE,OnDelete:CASCADE" json:"question,omitempty"`
}

// TableName especifica el nombre de la tabla
func (QuestionnaireQuestion) TableName() string {
	return "questionnaire_questions"
}

// EvaluationPeriod representa el modelo GORM para períodos de evaluación
type EvaluationPeriod struct {
	ID              uuid.UUID      `gorm:"type:uuid;primary_key;default:gen_random_uuid()" json:"id"`
	Name            string         `gorm:"type:varchar(255);not null" json:"name"`
	Description     string         `gorm:"type:text" json:"description"`
	Status          string         `gorm:"type:varchar(20);not null;default:'DRAFT'" json:"status"`
	StartDate       time.Time      `gorm:"not null" json:"start_date"`
	EndDate         time.Time      `gorm:"not null" json:"end_date"`
	QuestionnaireID uuid.UUID      `gorm:"type:uuid;not null;index" json:"questionnaire_id"`
	FichaID         uuid.UUID      `gorm:"type:uuid;not null;index" json:"ficha_id"`
	IsActive        bool           `gorm:"default:false" json:"is_active"`
	CreatedAt       time.Time      `gorm:"not null;default:CURRENT_TIMESTAMP" json:"created_at"`
	UpdatedAt       time.Time      `gorm:"not null;default:CURRENT_TIMESTAMP" json:"updated_at"`
	DeletedAt       gorm.DeletedAt `gorm:"index" json:"deleted_at,omitempty"`

	// Relaciones
	Questionnaire *Questionnaire `gorm:"foreignKey:QuestionnaireID;constraint:OnUpdate:CASCADE,OnDelete:RESTRICT" json:"questionnaire,omitempty"`
	Evaluations   []Evaluation   `gorm:"foreignKey:PeriodID;constraint:OnUpdate:CASCADE,OnDelete:RESTRICT" json:"-"`
	Reports       []Report       `gorm:"foreignKey:PeriodID;constraint:OnUpdate:CASCADE,OnDelete:CASCADE" json:"-"`
}

// TableName especifica el nombre de la tabla
func (EvaluationPeriod) TableName() string {
	return "evaluation_periods"
}

// Evaluation representa el modelo GORM para evaluaciones
type Evaluation struct {
	ID              uuid.UUID      `gorm:"type:uuid;primary_key;default:gen_random_uuid()" json:"id"`
	StudentID       uuid.UUID      `gorm:"type:uuid;not null;index" json:"student_id"`
	InstructorID    uuid.UUID      `gorm:"type:uuid;not null;index" json:"instructor_id"`
	PeriodID        uuid.UUID      `gorm:"type:uuid;not null;index" json:"period_id"`
	QuestionnaireID uuid.UUID      `gorm:"type:uuid;not null;index" json:"questionnaire_id"`
	Responses       string         `gorm:"type:jsonb" json:"responses"` // Stored as JSON
	GeneralComment  string         `gorm:"type:text" json:"general_comment"`
	Status          string         `gorm:"type:varchar(20);not null;default:'DRAFT'" json:"status"`
	SubmittedAt     *time.Time     `gorm:"null" json:"submitted_at"`
	CreatedAt       time.Time      `gorm:"not null;default:CURRENT_TIMESTAMP" json:"created_at"`
	UpdatedAt       time.Time      `gorm:"not null;default:CURRENT_TIMESTAMP" json:"updated_at"`
	DeletedAt       gorm.DeletedAt `gorm:"index" json:"deleted_at,omitempty"`

	// Relaciones
	Period        *EvaluationPeriod `gorm:"foreignKey:PeriodID;constraint:OnUpdate:CASCADE,OnDelete:RESTRICT" json:"period,omitempty"`
	Questionnaire *Questionnaire    `gorm:"foreignKey:QuestionnaireID;constraint:OnUpdate:CASCADE,OnDelete:RESTRICT" json:"questionnaire,omitempty"`
	Comments      []Comment         `gorm:"foreignKey:EvaluationID;constraint:OnUpdate:CASCADE,OnDelete:CASCADE" json:"comments,omitempty"`
}

// TableName especifica el nombre de la tabla
func (Evaluation) TableName() string {
	return "evaluations"
}

// Comment representa el modelo GORM para comentarios
type Comment struct {
	ID           uuid.UUID      `gorm:"type:uuid;primary_key;default:gen_random_uuid()" json:"id"`
	EvaluationID uuid.UUID      `gorm:"type:uuid;not null;index" json:"evaluation_id"`
	UserID       uuid.UUID      `gorm:"type:uuid;not null;index" json:"user_id"`
	Content      string         `gorm:"type:text;not null" json:"content"`
	Rating       *int           `gorm:"type:integer;check:rating >= 1 AND rating <= 5" json:"rating"`
	IsPrivate    bool           `gorm:"default:false" json:"is_private"`
	CreatedAt    time.Time      `gorm:"not null;default:CURRENT_TIMESTAMP" json:"created_at"`
	UpdatedAt    time.Time      `gorm:"not null;default:CURRENT_TIMESTAMP" json:"updated_at"`
	DeletedAt    gorm.DeletedAt `gorm:"index" json:"deleted_at,omitempty"`

	// Relaciones
	Evaluation *Evaluation `gorm:"foreignKey:EvaluationID;constraint:OnUpdate:CASCADE,OnDelete:CASCADE" json:"evaluation,omitempty"`
}

// TableName especifica el nombre de la tabla
func (Comment) TableName() string {
	return "comments"
}

// Report representa el modelo GORM para reportes
type Report struct {
	ID           uuid.UUID      `gorm:"type:uuid;primary_key;default:gen_random_uuid()" json:"id"`
	PeriodID     uuid.UUID      `gorm:"type:uuid;not null;index" json:"period_id"`
	Type         string         `gorm:"type:varchar(50);not null" json:"type"`
	Status       string         `gorm:"type:varchar(20);not null;default:'pending'" json:"status"`
	Title        string         `gorm:"type:varchar(255);not null" json:"title"`
	Description  string         `gorm:"type:text" json:"description"`
	Parameters   string         `gorm:"type:jsonb" json:"parameters"` // Stored as JSON
	Results      string         `gorm:"type:jsonb" json:"results"`    // Stored as JSON
	FilePath     string         `gorm:"type:varchar(500)" json:"file_path"`
	GeneratedBy  uuid.UUID      `gorm:"type:uuid;not null;index" json:"generated_by"`
	GeneratedAt  *time.Time     `gorm:"null" json:"generated_at"`
	ErrorMessage string         `gorm:"type:text" json:"error_message"`
	CreatedAt    time.Time      `gorm:"not null;default:CURRENT_TIMESTAMP" json:"created_at"`
	UpdatedAt    time.Time      `gorm:"not null;default:CURRENT_TIMESTAMP" json:"updated_at"`
	DeletedAt    gorm.DeletedAt `gorm:"index" json:"deleted_at,omitempty"`

	// Relaciones
	Period *EvaluationPeriod `gorm:"foreignKey:PeriodID;constraint:OnUpdate:CASCADE,OnDelete:CASCADE" json:"period,omitempty"`
}

// TableName especifica el nombre de la tabla
func (Report) TableName() string {
	return "reports"
}

// Configuration representa el modelo GORM para configuraciones
type Configuration struct {
	ID          uuid.UUID      `gorm:"type:uuid;primary_key;default:gen_random_uuid()" json:"id"`
	Key         string         `gorm:"type:varchar(100);not null;unique;index" json:"key"`
	Value       string         `gorm:"type:text;not null" json:"value"`
	Description string         `gorm:"type:text" json:"description"`
	Category    string         `gorm:"type:varchar(50);not null;index" json:"category"`
	IsActive    bool           `gorm:"default:true" json:"is_active"`
	IsEditable  bool           `gorm:"default:true" json:"is_editable"`
	CreatedBy   uuid.UUID      `gorm:"type:uuid;not null;index" json:"created_by"`
	UpdatedBy   uuid.UUID      `gorm:"type:uuid;not null;index" json:"updated_by"`
	CreatedAt   time.Time      `gorm:"not null;default:CURRENT_TIMESTAMP" json:"created_at"`
	UpdatedAt   time.Time      `gorm:"not null;default:CURRENT_TIMESTAMP" json:"updated_at"`
	DeletedAt   gorm.DeletedAt `gorm:"index" json:"deleted_at,omitempty"`
}

// TableName especifica el nombre de la tabla
func (Configuration) TableName() string {
	return "configurations"
}

// Notification representa el modelo GORM para notificaciones
type Notification struct {
	ID         uuid.UUID      `gorm:"type:uuid;primary_key;default:gen_random_uuid()" json:"id"`
	Type       string         `gorm:"type:varchar(50);not null;index" json:"type"`
	Title      string         `gorm:"type:varchar(255);not null" json:"title"`
	Message    string         `gorm:"type:text;not null" json:"message"`
	Recipient  uuid.UUID      `gorm:"type:uuid;not null;index" json:"recipient"`
	EntityType string         `gorm:"type:varchar(50);index" json:"entity_type"`
	EntityID   *uuid.UUID     `gorm:"type:uuid;index" json:"entity_id"`
	Metadata   string         `gorm:"type:jsonb" json:"metadata"` // Stored as JSON
	IsRead     bool           `gorm:"default:false" json:"is_read"`
	IsSent     bool           `gorm:"default:false" json:"is_sent"`
	SentAt     *time.Time     `gorm:"null" json:"sent_at"`
	ReadAt     *time.Time     `gorm:"null" json:"read_at"`
	CreatedAt  time.Time      `gorm:"not null;default:CURRENT_TIMESTAMP" json:"created_at"`
	UpdatedAt  time.Time      `gorm:"not null;default:CURRENT_TIMESTAMP" json:"updated_at"`
	DeletedAt  gorm.DeletedAt `gorm:"index" json:"deleted_at,omitempty"`
}

// TableName especifica el nombre de la tabla
func (Notification) TableName() string {
	return "notifications"
}
