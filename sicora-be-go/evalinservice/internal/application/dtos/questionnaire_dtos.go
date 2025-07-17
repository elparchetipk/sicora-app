package dtos

import (
	"time"

	"github.com/google/uuid"
)

// QuestionnaireCreateDTO representa los datos para crear un cuestionario
type QuestionnaireCreateDTO struct {
	Name        string `json:"name" validate:"required,min=3,max=200"`
	Description string `json:"description" validate:"max=1000"`
}

// QuestionnaireUpdateDTO representa los datos para actualizar un cuestionario
type QuestionnaireUpdateDTO struct {
	Name        *string `json:"name" validate:"omitempty,min=3,max=200"`
	Description *string `json:"description" validate:"omitempty,max=1000"`
	IsActive    *bool   `json:"is_active"`
}

// QuestionnaireResponseDTO representa un cuestionario en las respuestas
type QuestionnaireResponseDTO struct {
	ID            uuid.UUID             `json:"id"`
	Name          string                `json:"name"`
	Description   string                `json:"description"`
	IsActive      bool                  `json:"is_active"`
	QuestionCount int                   `json:"question_count"`
	Questions     []QuestionResponseDTO `json:"questions,omitempty"`
	CreatedAt     time.Time             `json:"created_at"`
	UpdatedAt     time.Time             `json:"updated_at"`
}

// QuestionnaireListResponseDTO representa una lista paginada de cuestionarios
type QuestionnaireListResponseDTO struct {
	Questionnaires []QuestionnaireResponseDTO `json:"questionnaires"`
	Total          int                        `json:"total"`
	Page           int                        `json:"page"`
	PerPage        int                        `json:"per_page"`
	TotalPages     int                        `json:"total_pages"`
}

// QuestionnaireWithQuestionsResponseDTO representa un cuestionario con sus preguntas
type QuestionnaireWithQuestionsResponseDTO struct {
	Questionnaire QuestionnaireResponseDTO `json:"questionnaire"`
	Questions     []QuestionResponseDTO    `json:"questions"`
}

// AddQuestionToQuestionnaireDTO representa los datos para agregar una pregunta
type AddQuestionToQuestionnaireDTO struct {
	QuestionID uuid.UUID `json:"question_id" validate:"required"`
}

// ReorderQuestionsDTO representa los datos para reordenar preguntas
type ReorderQuestionsDTO struct {
	QuestionIDs []uuid.UUID `json:"question_ids" validate:"required,min=1"`
}

// QuestionnaireFiltersDTO representa los filtros para búsqueda de cuestionarios
type QuestionnaireFiltersDTO struct {
	IsActive     *bool  `json:"is_active"`
	Search       string `json:"search"`
	HasQuestions *bool  `json:"has_questions"`
	Page         int    `json:"page" validate:"min=1"`
	PerPage      int    `json:"per_page" validate:"min=1,max=100"`
	OrderBy      string `json:"order_by" validate:"omitempty,oneof=created_at updated_at name"`
	OrderDir     string `json:"order_dir" validate:"omitempty,oneof=asc desc"`
}

// Aliases para compatibilidad con usecases
type QuestionnaireDTO = QuestionnaireResponseDTO
type QuestionnaireWithQuestionsDTO = QuestionnaireWithQuestionsResponseDTO
