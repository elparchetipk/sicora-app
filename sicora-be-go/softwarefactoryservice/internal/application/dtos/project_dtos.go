package dtos

import (
	"errors"
	"time"

	"softwarefactoryservice/internal/domain/entities"

	"github.com/google/uuid"
)

// CreateProjectRequest represents the request to create a new project
type CreateProjectRequest struct {
	Name                   string                        `json:"name" validate:"required,min=3,max=100"`
	Description            string                        `json:"description" validate:"required,min=10"`
	ClientInfo             entities.ClientInfo           `json:"client_info" validate:"required"`
	TechStack              []string                      `json:"tech_stack" validate:"required,min=1"`
	LearningObjectives     []string                      `json:"learning_objectives" validate:"required,min=1"`
	ComplexityLevel        entities.ComplexityLevel      `json:"complexity_level" validate:"required"`
	EstimatedDurationWeeks int                           `json:"estimated_duration_weeks" validate:"required,min=4,max=26"`
	EvaluationCriteria     []entities.EvaluationCriterion `json:"evaluation_criteria"`
	Deliverables           []entities.Deliverable        `json:"deliverables"`
	Milestones             []entities.Milestone          `json:"milestones"`
	CreatedBy              uuid.UUID                     `json:"created_by" validate:"required"`
	StartDate              *time.Time                    `json:"start_date,omitempty"`
	EndDate                *time.Time                    `json:"end_date,omitempty"`
}

// Validate validates the create project request
func (r CreateProjectRequest) Validate() error {
	if r.Name == "" {
		return errors.New("name is required")
	}
	if len(r.Name) < 3 || len(r.Name) > 100 {
		return errors.New("name must be between 3 and 100 characters")
	}
	if r.Description == "" {
		return errors.New("description is required")
	}
	if len(r.Description) < 10 {
		return errors.New("description must be at least 10 characters")
	}
	if len(r.TechStack) == 0 {
		return errors.New("tech stack is required")
	}
	if len(r.LearningObjectives) == 0 {
		return errors.New("learning objectives are required")
	}
	if r.EstimatedDurationWeeks < 4 || r.EstimatedDurationWeeks > 26 {
		return errors.New("estimated duration must be between 4 and 26 weeks")
	}
	if r.StartDate != nil && r.EndDate != nil && r.StartDate.After(*r.EndDate) {
		return errors.New("start date cannot be after end date")
	}
	return nil
}

// UpdateProjectRequest represents the request to update a project
type UpdateProjectRequest struct {
	Name                   *string                        `json:"name,omitempty"`
	Description            *string                        `json:"description,omitempty"`
	TechStack              []string                       `json:"tech_stack,omitempty"`
	LearningObjectives     []string                       `json:"learning_objectives,omitempty"`
	ComplexityLevel        *entities.ComplexityLevel      `json:"complexity_level,omitempty"`
	EstimatedDurationWeeks *int                           `json:"estimated_duration_weeks,omitempty"`
	Status                 *entities.ProjectStatus        `json:"status,omitempty"`
	EvaluationCriteria     []entities.EvaluationCriterion `json:"evaluation_criteria,omitempty"`
	Deliverables           []entities.Deliverable         `json:"deliverables,omitempty"`
	Milestones             []entities.Milestone           `json:"milestones,omitempty"`
	StartDate              *time.Time                     `json:"start_date,omitempty"`
	EndDate                *time.Time                     `json:"end_date,omitempty"`
}

// Validate validates the update project request
func (r UpdateProjectRequest) Validate() error {
	if r.Name != nil {
		if len(*r.Name) < 3 || len(*r.Name) > 100 {
			return errors.New("name must be between 3 and 100 characters")
		}
	}
	if r.Description != nil {
		if len(*r.Description) < 10 {
			return errors.New("description must be at least 10 characters")
		}
	}
	if r.EstimatedDurationWeeks != nil {
		if *r.EstimatedDurationWeeks < 4 || *r.EstimatedDurationWeeks > 26 {
			return errors.New("estimated duration must be between 4 and 26 weeks")
		}
	}
	return nil
}

// ProjectResponse represents the response for project operations
type ProjectResponse struct {
	ID                     uuid.UUID                     `json:"id"`
	Name                   string                        `json:"name"`
	Description            string                        `json:"description"`
	ClientInfo             entities.ClientInfo           `json:"client_info"`
	TechStack              []string                      `json:"tech_stack"`
	LearningObjectives     []string                      `json:"learning_objectives"`
	ComplexityLevel        entities.ComplexityLevel      `json:"complexity_level"`
	EstimatedDurationWeeks int                           `json:"estimated_duration_weeks"`
	Status                 entities.ProjectStatus        `json:"status"`
	EvaluationCriteria     []entities.EvaluationCriterion `json:"evaluation_criteria"`
	Deliverables           []entities.Deliverable        `json:"deliverables"`
	Milestones             []entities.Milestone          `json:"milestones"`
	CreatedBy              uuid.UUID                     `json:"created_by"`
	CreatedAt              time.Time                     `json:"created_at"`
	UpdatedAt              time.Time                     `json:"updated_at"`
	StartDate              *time.Time                    `json:"start_date,omitempty"`
	EndDate                *time.Time                    `json:"end_date,omitempty"`
	TeamsCount             int                           `json:"teams_count,omitempty"`
	UserStoriesCount       int                           `json:"user_stories_count,omitempty"`
}

// ProjectListResponse represents the response for project listing
type ProjectListResponse struct {
	Projects   []ProjectResponse `json:"projects"`
	TotalCount int64             `json:"total_count"`
	Page       int               `json:"page"`
	PageSize   int               `json:"page_size"`
	TotalPages int               `json:"total_pages"`
}

// ProjectStats represents project statistics
type ProjectStats struct {
	ProjectID         string                   `json:"project_id"`
	TeamsCount        int                      `json:"teams_count"`
	TotalStudents     int                      `json:"total_students"`
	UserStoriesCount  int                      `json:"user_stories_count"`
	CompletedStories  int                      `json:"completed_stories"`
	InProgressStories int                      `json:"in_progress_stories"`
	SprintsCount      int                      `json:"sprints_count"`
	ActiveSprints     int                      `json:"active_sprints"`
	CompletionRate    float64                  `json:"completion_rate"`
	ProjectStatus     entities.ProjectStatus   `json:"project_status"`
}

// ToProjectEntity converts CreateProjectRequest to Project entity
func (r CreateProjectRequest) ToProjectEntity() *entities.Project {
	return &entities.Project{
		ID:                     uuid.New(),
		Name:                   r.Name,
		Description:            r.Description,
		ClientInfo:             r.ClientInfo,
		TechStack:              r.TechStack,
		LearningObjectives:     r.LearningObjectives,
		ComplexityLevel:        r.ComplexityLevel,
		EstimatedDurationWeeks: r.EstimatedDurationWeeks,
		Status:                 entities.ProjectStatusPlanning,
		EvaluationCriteria:     r.EvaluationCriteria,
		Deliverables:           r.Deliverables,
		Milestones:             r.Milestones,
		CreatedBy:              r.CreatedBy,
		StartDate:              r.StartDate,
		EndDate:                r.EndDate,
		CreatedAt:              time.Now(),
		UpdatedAt:              time.Now(),
	}
}

// FromProjectEntity converts Project entity to ProjectResponse
func FromProjectEntity(project *entities.Project) ProjectResponse {
	return ProjectResponse{
		ID:                     project.ID,
		Name:                   project.Name,
		Description:            project.Description,
		ClientInfo:             project.ClientInfo,
		TechStack:              project.TechStack,
		LearningObjectives:     project.LearningObjectives,
		ComplexityLevel:        project.ComplexityLevel,
		EstimatedDurationWeeks: project.EstimatedDurationWeeks,
		Status:                 project.Status,
		EvaluationCriteria:     project.EvaluationCriteria,
		Deliverables:           project.Deliverables,
		Milestones:             project.Milestones,
		CreatedBy:              project.CreatedBy,
		CreatedAt:              project.CreatedAt,
		UpdatedAt:              project.UpdatedAt,
		StartDate:              project.StartDate,
		EndDate:                project.EndDate,
	}
}
