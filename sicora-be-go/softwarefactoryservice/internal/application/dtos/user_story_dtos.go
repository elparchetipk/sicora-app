package dtos

import (
	"time"

	"github.com/google/uuid"
	"softwarefactoryservice/internal/domain/entities"
)

// CreateUserStoryRequest represents the request to create a new user story
type CreateUserStoryRequest struct {
	ProjectID              string                            `json:"project_id" binding:"required" validate:"uuid"`
	SprintID               *string                           `json:"sprint_id,omitempty" validate:"omitempty,uuid"`
	Title                  string                            `json:"title" binding:"required,min=5,max=255"`
	Description            string                            `json:"description" binding:"required,min=10"`
	FunctionalObjective    string                            `json:"functional_objective" binding:"required"`
	AcademicObjective      string                            `json:"academic_objective" binding:"required"`
	AcceptanceCriteria     []CreateAcceptanceCriterionRequest `json:"acceptance_criteria" binding:"required,min=1"`
	AcademicCriteria       []CreateAcademicCriterionRequest  `json:"academic_criteria" binding:"required,min=1"`
	StoryPoints            int                               `json:"story_points" binding:"required,min=1,max=21"`
	Priority               int                               `json:"priority" binding:"required,min=1,max=5"`
	Type                   string                            `json:"type" binding:"required,oneof=functional academic technical bugfix"`
	Status                 string                            `json:"status" binding:"required,oneof=backlog todo in_progress review done"`
	AssignedTo             *string                           `json:"assigned_to,omitempty" validate:"omitempty,uuid"`
	EstimatedHours         int                               `json:"estimated_hours" binding:"min=0"`
	LearningHours          int                               `json:"learning_hours" binding:"min=0"`
	Tags                   []string                          `json:"tags,omitempty"`
	Dependencies           []string                          `json:"dependencies,omitempty" validate:"dive,uuid"`
	CreatedBy              string                            `json:"created_by" binding:"required" validate:"uuid"`
}

// CreateAcceptanceCriterionRequest represents a technical acceptance criterion
type CreateAcceptanceCriterionRequest struct {
	Description string `json:"description" binding:"required"`
	TestCase    string `json:"test_case,omitempty"`
}

// CreateAcademicCriterionRequest represents an academic acceptance criterion
type CreateAcademicCriterionRequest struct {
	Competency       string   `json:"competency" binding:"required"`
	Description      string   `json:"description" binding:"required"`
	EvidenceRequired []string `json:"evidence_required" binding:"required,min=1"`
	RubricScale      int      `json:"rubric_scale" binding:"required,min=1,max=5"`
}

// UpdateUserStoryRequest represents the request to update a user story
type UpdateUserStoryRequest struct {
	Title                  *string                            `json:"title,omitempty" validate:"omitempty,min=5,max=255"`
	Description            *string                            `json:"description,omitempty" validate:"omitempty,min=10"`
	FunctionalObjective    *string                            `json:"functional_objective,omitempty"`
	AcademicObjective      *string                            `json:"academic_objective,omitempty"`
	AcceptanceCriteria     []CreateAcceptanceCriterionRequest `json:"acceptance_criteria,omitempty"`
	AcademicCriteria       []CreateAcademicCriterionRequest   `json:"academic_criteria,omitempty"`
	StoryPoints            *int                               `json:"story_points,omitempty" validate:"omitempty,min=1,max=21"`
	Priority               *int                               `json:"priority,omitempty" validate:"omitempty,min=1,max=5"`
	Type                   *string                            `json:"type,omitempty" validate:"omitempty,oneof=functional academic technical bugfix"`
	Status                 *string                            `json:"status,omitempty" validate:"omitempty,oneof=backlog todo in_progress review done"`
	AssignedTo             *string                            `json:"assigned_to,omitempty" validate:"omitempty,uuid"`
	SprintID               *string                            `json:"sprint_id,omitempty" validate:"omitempty,uuid"`
	EstimatedHours         *int                               `json:"estimated_hours,omitempty" validate:"omitempty,min=0"`
	ActualHours            *int                               `json:"actual_hours,omitempty" validate:"omitempty,min=0"`
	LearningHours          *int                               `json:"learning_hours,omitempty" validate:"omitempty,min=0"`
	Tags                   []string                           `json:"tags,omitempty"`
	Dependencies           []string                           `json:"dependencies,omitempty" validate:"dive,uuid"`
}

// UserStoryResponse represents a user story in API responses
type UserStoryResponse struct {
	ID                     string                         `json:"id"`
	ProjectID              string                         `json:"project_id"`
	SprintID               *string                        `json:"sprint_id,omitempty"`
	Title                  string                         `json:"title"`
	Description            string                         `json:"description"`
	FunctionalObjective    string                         `json:"functional_objective"`
	AcademicObjective      string                         `json:"academic_objective"`
	AcceptanceCriteria     []AcceptanceCriterionResponse  `json:"acceptance_criteria"`
	AcademicCriteria       []AcademicCriterionResponse    `json:"academic_criteria"`
	StoryPoints            int                            `json:"story_points"`
	Priority               int                            `json:"priority"`
	Type                   string                         `json:"type"`
	Status                 string                         `json:"status"`
	AssignedTo             *string                        `json:"assigned_to,omitempty"`
	EstimatedHours         int                            `json:"estimated_hours"`
	ActualHours            int                            `json:"actual_hours"`
	LearningHours          int                            `json:"learning_hours"`
	Tags                   []string                       `json:"tags"`
	Dependencies           []string                       `json:"dependencies"`
	CreatedBy              string                         `json:"created_by"`
	CreatedAt              time.Time                      `json:"created_at"`
	UpdatedAt              time.Time                      `json:"updated_at"`
	CompletedAt            *time.Time                     `json:"completed_at,omitempty"`
	Progress               float64                        `json:"progress"`
}

// AcceptanceCriterionResponse represents a technical acceptance criterion response
type AcceptanceCriterionResponse struct {
	ID          string `json:"id"`
	Description string `json:"description"`
	IsCompleted bool   `json:"is_completed"`
	TestCase    string `json:"test_case,omitempty"`
}

// AcademicCriterionResponse represents an academic acceptance criterion response
type AcademicCriterionResponse struct {
	ID               string   `json:"id"`
	Competency       string   `json:"competency"`
	Description      string   `json:"description"`
	EvidenceRequired []string `json:"evidence_required"`
	IsCompleted      bool     `json:"is_completed"`
	RubricScale      int      `json:"rubric_scale"`
}

// UserStoryListResponse represents a paginated list of user stories
type UserStoryListResponse struct {
	UserStories []UserStoryResponse `json:"user_stories"`
	Total       int64               `json:"total"`
	Page        int                 `json:"page"`
	PageSize    int                 `json:"page_size"`
	TotalPages  int                 `json:"total_pages"`
}

// UserStoryFilterRequest represents filters for user story queries
type UserStoryFilterRequest struct {
	ProjectID        *string `form:"project_id" validate:"omitempty,uuid"`
	SprintID         *string `form:"sprint_id" validate:"omitempty,uuid"`
	AssignedTo       *string `form:"assigned_to" validate:"omitempty,uuid"`
	Status           *string `form:"status" validate:"omitempty,oneof=backlog todo in_progress review done"`
	Type             *string `form:"type" validate:"omitempty,oneof=functional academic technical bugfix"`
	Priority         *int    `form:"priority" validate:"omitempty,min=1,max=5"`
	MinStoryPoints   *int    `form:"min_story_points" validate:"omitempty,min=1"`
	MaxStoryPoints   *int    `form:"max_story_points" validate:"omitempty,max=21"`
	Tags             *string `form:"tags"` // Comma-separated tags
	HasDependencies  *bool   `form:"has_dependencies"`
	Page             int     `form:"page" validate:"min=1"`
	PageSize         int     `form:"page_size" validate:"min=1,max=100"`
}

// UserStoryStatsResponse represents statistics about user stories
type UserStoryStatsResponse struct {
	TotalStories         int64                   `json:"total_stories"`
	StoriesByStatus      map[string]int64        `json:"stories_by_status"`
	StoriesByType        map[string]int64        `json:"stories_by_type"`
	StoriesByPriority    map[string]int64        `json:"stories_by_priority"`
	AverageStoryPoints   float64                 `json:"average_story_points"`
	TotalStoryPoints     int                     `json:"total_story_points"`
	CompletedStoryPoints int                     `json:"completed_story_points"`
	TotalEstimatedHours  int                     `json:"total_estimated_hours"`
	TotalActualHours     int                     `json:"total_actual_hours"`
	TotalLearningHours   int                     `json:"total_learning_hours"`
	AverageProgress      float64                 `json:"average_progress"`
	CompletionRate       float64                 `json:"completion_rate"`
}

// BacklogResponse represents the product backlog with prioritized stories
type BacklogResponse struct {
	Stories     []UserStoryResponse `json:"stories"`
	TotalPoints int                 `json:"total_points"`
	Statistics  UserStoryStatsResponse `json:"statistics"`
	LastUpdated time.Time          `json:"last_updated"`
}

// EvidenceResponse represents evidence for a user story
type EvidenceResponse struct {
	ID          string    `json:"id"`
	UserStoryID string    `json:"user_story_id"`
	Type        string    `json:"type"`
	Title       string    `json:"title"`
	Description string    `json:"description"`
	URL         string    `json:"url"`
	FilePath    string    `json:"file_path"`
	SubmittedBy string    `json:"submitted_by"`
	SubmittedAt time.Time `json:"submitted_at"`
	ReviewedBy  *string   `json:"reviewed_by,omitempty"`
	ReviewedAt  *time.Time `json:"reviewed_at,omitempty"`
	IsApproved  bool      `json:"is_approved"`
	Feedback    string    `json:"feedback"`
}

// Conversion methods

// ToEntity converts CreateUserStoryRequest to entities.UserStory
func (r *CreateUserStoryRequest) ToEntity() (*entities.UserStory, error) {
	projectID, err := uuid.Parse(r.ProjectID)
	if err != nil {
		return nil, err
	}

	createdBy, err := uuid.Parse(r.CreatedBy)
	if err != nil {
		return nil, err
	}

	story := &entities.UserStory{
		ProjectID:           projectID,
		Title:               r.Title,
		Description:         r.Description,
		FunctionalObjective: r.FunctionalObjective,
		AcademicObjective:   r.AcademicObjective,
		StoryPoints:         r.StoryPoints,
		Priority:            r.Priority,
		Type:                entities.StoryType(r.Type),
		Status:              entities.StoryStatus(r.Status),
		EstimatedHours:      r.EstimatedHours,
		LearningHours:       r.LearningHours,
		Tags:                r.Tags,
		CreatedBy:           createdBy,
	}

	// Convert SprintID if provided
	if r.SprintID != nil {
		sprintID, err := uuid.Parse(*r.SprintID)
		if err != nil {
			return nil, err
		}
		story.SprintID = &sprintID
	}

	// Convert AssignedTo if provided
	if r.AssignedTo != nil {
		assignedTo, err := uuid.Parse(*r.AssignedTo)
		if err != nil {
			return nil, err
		}
		story.AssignedTo = &assignedTo
	}

	// Convert Dependencies
	if len(r.Dependencies) > 0 {
		dependencies := make([]uuid.UUID, len(r.Dependencies))
		for i, dep := range r.Dependencies {
			depID, err := uuid.Parse(dep)
			if err != nil {
				return nil, err
			}
			dependencies[i] = depID
		}
		story.Dependencies = dependencies
	}

	// Convert AcceptanceCriteria
	acceptanceCriteria := make([]entities.AcceptanceCriterion, len(r.AcceptanceCriteria))
	for i, criterion := range r.AcceptanceCriteria {
		acceptanceCriteria[i] = entities.AcceptanceCriterion{
			ID:          uuid.New().String(),
			Description: criterion.Description,
			TestCase:    criterion.TestCase,
			IsCompleted: false,
		}
	}
	story.AcceptanceCriteria = acceptanceCriteria

	// Convert AcademicCriteria
	academicCriteria := make([]entities.AcademicCriterion, len(r.AcademicCriteria))
	for i, criterion := range r.AcademicCriteria {
		academicCriteria[i] = entities.AcademicCriterion{
			ID:               uuid.New().String(),
			Competency:       criterion.Competency,
			Description:      criterion.Description,
			EvidenceRequired: criterion.EvidenceRequired,
			IsCompleted:      false,
			RubricScale:      criterion.RubricScale,
		}
	}
	story.AcademicCriteria = academicCriteria

	return story, nil
}

// FromEntity converts entities.UserStory to UserStoryResponse
func (r *UserStoryResponse) FromEntity(userStory *entities.UserStory) {
	r.ID = userStory.ID.String()
	r.ProjectID = userStory.ProjectID.String()
	
	if userStory.SprintID != nil {
		sprintIDStr := userStory.SprintID.String()
		r.SprintID = &sprintIDStr
	}
	
	if userStory.AssignedTo != nil {
		assignedToStr := userStory.AssignedTo.String()
		r.AssignedTo = &assignedToStr
	}

	r.Title = userStory.Title
	r.Description = userStory.Description
	r.FunctionalObjective = userStory.FunctionalObjective
	r.AcademicObjective = userStory.AcademicObjective
	r.StoryPoints = userStory.StoryPoints
	r.Priority = userStory.Priority
	r.Type = string(userStory.Type)
	r.Status = string(userStory.Status)
	r.EstimatedHours = userStory.EstimatedHours
	r.ActualHours = userStory.ActualHours
	r.LearningHours = userStory.LearningHours
	r.Tags = userStory.Tags
	r.CreatedBy = userStory.CreatedBy.String()
	r.CreatedAt = userStory.CreatedAt
	r.UpdatedAt = userStory.UpdatedAt
	r.CompletedAt = userStory.CompletedAt
	r.Progress = userStory.GetProgress()

	// Convert Dependencies
	if len(userStory.Dependencies) > 0 {
		dependencies := make([]string, len(userStory.Dependencies))
		for i, dep := range userStory.Dependencies {
			dependencies[i] = dep.String()
		}
		r.Dependencies = dependencies
	}

	// Convert AcceptanceCriteria
	acceptanceCriteria := make([]AcceptanceCriterionResponse, len(userStory.AcceptanceCriteria))
	for i, criterion := range userStory.AcceptanceCriteria {
		acceptanceCriteria[i] = AcceptanceCriterionResponse{
			ID:          criterion.ID,
			Description: criterion.Description,
			IsCompleted: criterion.IsCompleted,
			TestCase:    criterion.TestCase,
		}
	}
	r.AcceptanceCriteria = acceptanceCriteria

	// Convert AcademicCriteria
	academicCriteria := make([]AcademicCriterionResponse, len(userStory.AcademicCriteria))
	for i, criterion := range userStory.AcademicCriteria {
		academicCriteria[i] = AcademicCriterionResponse{
			ID:               criterion.ID,
			Competency:       criterion.Competency,
			Description:      criterion.Description,
			EvidenceRequired: criterion.EvidenceRequired,
			IsCompleted:      criterion.IsCompleted,
			RubricScale:      criterion.RubricScale,
		}
	}
	r.AcademicCriteria = academicCriteria
}

// FromEntityList converts a slice of entities.UserStory to UserStoryListResponse
func (r *UserStoryListResponse) FromEntityList(userStories []entities.UserStory, total int64, page, pageSize int) {
	r.UserStories = make([]UserStoryResponse, len(userStories))
	for i, story := range userStories {
		r.UserStories[i].FromEntity(&story)
	}
	r.Total = total
	r.Page = page
	r.PageSize = pageSize
	if pageSize > 0 {
		r.TotalPages = int((total + int64(pageSize) - 1) / int64(pageSize))
	}
}

// ApplyToEntity applies UpdateUserStoryRequest to an existing entities.UserStory
func (r *UpdateUserStoryRequest) ApplyToEntity(userStory *entities.UserStory) error {
	if r.Title != nil {
		userStory.Title = *r.Title
	}
	if r.Description != nil {
		userStory.Description = *r.Description
	}
	if r.FunctionalObjective != nil {
		userStory.FunctionalObjective = *r.FunctionalObjective
	}
	if r.AcademicObjective != nil {
		userStory.AcademicObjective = *r.AcademicObjective
	}
	if r.StoryPoints != nil {
		userStory.StoryPoints = *r.StoryPoints
	}
	if r.Priority != nil {
		userStory.Priority = *r.Priority
	}
	if r.Type != nil {
		userStory.Type = entities.StoryType(*r.Type)
	}
	if r.Status != nil {
		newStatus := entities.StoryStatus(*r.Status)
		if !userStory.CanTransitionTo(newStatus) {
			return &entities.ValidationError{
				Field:   "status",
				Message: "invalid status transition",
			}
		}
		userStory.Status = newStatus
		if newStatus == entities.StoryStatusDone {
			userStory.MarkCompleted()
		}
	}
	if r.EstimatedHours != nil {
		userStory.EstimatedHours = *r.EstimatedHours
	}
	if r.ActualHours != nil {
		userStory.ActualHours = *r.ActualHours
	}
	if r.LearningHours != nil {
		userStory.LearningHours = *r.LearningHours
	}
	if r.Tags != nil {
		userStory.Tags = r.Tags
	}

	// Handle SprintID assignment
	if r.SprintID != nil {
		sprintID, err := uuid.Parse(*r.SprintID)
		if err != nil {
			return err
		}
		userStory.SprintID = &sprintID
	}

	// Handle AssignedTo assignment
	if r.AssignedTo != nil {
		assignedTo, err := uuid.Parse(*r.AssignedTo)
		if err != nil {
			return err
		}
		userStory.AssignedTo = &assignedTo
	}

	// Handle Dependencies
	if r.Dependencies != nil {
		dependencies := make([]uuid.UUID, len(r.Dependencies))
		for i, dep := range r.Dependencies {
			depID, err := uuid.Parse(dep)
			if err != nil {
				return err
			}
			dependencies[i] = depID
		}
		userStory.Dependencies = dependencies
	}

	// Handle AcceptanceCriteria
	if r.AcceptanceCriteria != nil {
		acceptanceCriteria := make([]entities.AcceptanceCriterion, len(r.AcceptanceCriteria))
		for i, criterion := range r.AcceptanceCriteria {
			acceptanceCriteria[i] = entities.AcceptanceCriterion{
				ID:          uuid.New().String(),
				Description: criterion.Description,
				TestCase:    criterion.TestCase,
				IsCompleted: false,
			}
		}
		userStory.AcceptanceCriteria = acceptanceCriteria
	}

	// Handle AcademicCriteria
	if r.AcademicCriteria != nil {
		academicCriteria := make([]entities.AcademicCriterion, len(r.AcademicCriteria))
		for i, criterion := range r.AcademicCriteria {
			academicCriteria[i] = entities.AcademicCriterion{
				ID:               uuid.New().String(),
				Competency:       criterion.Competency,
				Description:      criterion.Description,
				EvidenceRequired: criterion.EvidenceRequired,
				IsCompleted:      false,
				RubricScale:      criterion.RubricScale,
			}
		}
		userStory.AcademicCriteria = academicCriteria
	}

	return nil
}
