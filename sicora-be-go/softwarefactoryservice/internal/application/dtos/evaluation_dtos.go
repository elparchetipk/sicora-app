package dtos

import (
	"time"

	"softwarefactoryservice/internal/domain/entities"

	"github.com/google/uuid"
)

// CreateEvaluationRequest represents the request to create a new evaluation
type CreateEvaluationRequest struct {
	ApprenticeID         string                      `json:"apprentice_id" binding:"required" validate:"uuid"`
	ProjectID            string                      `json:"project_id" binding:"required" validate:"uuid"`
	SprintID             *string                     `json:"sprint_id,omitempty" validate:"omitempty,uuid"`
	EvaluatorID          string                      `json:"evaluator_id" binding:"required" validate:"uuid"`
	EvaluationType       string                      `json:"evaluation_type" binding:"required,oneof=self instructor peer comprehensive"`
	EvaluationDate       time.Time                   `json:"evaluation_date" binding:"required"`
	TechnicalSkills      TechnicalSkillsRequest      `json:"technical_skills" binding:"required"`
	SoftSkills           SoftSkillsRequest           `json:"soft_skills" binding:"required"`
	LearningObjectivesMet []string                   `json:"learning_objectives_met,omitempty"`
	AreasForImprovement   []string                   `json:"areas_for_improvement,omitempty"`
	Recommendations      string                      `json:"recommendations,omitempty"`
	Notes                string                      `json:"notes,omitempty"`
}

// TechnicalSkillsRequest represents technical skills evaluation
type TechnicalSkillsRequest struct {
	CodingQuality      int `json:"coding_quality" binding:"required,min=1,max=5"`
	ProblemSolving     int `json:"problem_solving" binding:"required,min=1,max=5"`
	TechnologyAdoption int `json:"technology_adoption" binding:"required,min=1,max=5"`
	TestingPractices   int `json:"testing_practices" binding:"required,min=1,max=5"`
}

// SoftSkillsRequest represents soft skills evaluation
type SoftSkillsRequest struct {
	Communication int `json:"communication" binding:"required,min=1,max=5"`
	Teamwork      int `json:"teamwork" binding:"required,min=1,max=5"`
	Leadership    int `json:"leadership" binding:"required,min=1,max=5"`
	Adaptability  int `json:"adaptability" binding:"required,min=1,max=5"`
}

// UpdateEvaluationRequest represents the request to update an evaluation
type UpdateEvaluationRequest struct {
	EvaluationType        *string                     `json:"evaluation_type,omitempty" validate:"omitempty,oneof=self instructor peer comprehensive"`
	EvaluationDate        *time.Time                  `json:"evaluation_date,omitempty"`
	TechnicalSkills       *TechnicalSkillsRequest     `json:"technical_skills,omitempty"`
	SoftSkills            *SoftSkillsRequest          `json:"soft_skills,omitempty"`
	LearningObjectivesMet []string                    `json:"learning_objectives_met,omitempty"`
	AreasForImprovement   []string                    `json:"areas_for_improvement,omitempty"`
	Recommendations       *string                     `json:"recommendations,omitempty"`
	Notes                 *string                     `json:"notes,omitempty"`
}

// EvaluationResponse represents an evaluation in API responses
type EvaluationResponse struct {
	ID                   string                     `json:"id"`
	ApprenticeID         string                     `json:"apprentice_id"`
	ProjectID            string                     `json:"project_id"`
	SprintID             *string                    `json:"sprint_id,omitempty"`
	EvaluatorID          string                     `json:"evaluator_id"`
	EvaluationType       string                     `json:"evaluation_type"`
	EvaluationDate       time.Time                  `json:"evaluation_date"`
	TechnicalSkills      TechnicalSkillsResponse    `json:"technical_skills"`
	SoftSkills           SoftSkillsResponse         `json:"soft_skills"`
	LearningObjectivesMet []string                  `json:"learning_objectives_met"`
	AreasForImprovement   []string                  `json:"areas_for_improvement"`
	Recommendations      string                     `json:"recommendations"`
	OverallScore         float64                    `json:"overall_score"`
	TechnicalAverage     float64                    `json:"technical_average"`
	SoftSkillsAverage    float64                    `json:"soft_skills_average"`
	Notes                string                     `json:"notes"`
	NeedsImprovement     bool                       `json:"needs_improvement"`
	WeakAreas            []string                   `json:"weak_areas"`
	CreatedAt            time.Time                  `json:"created_at"`
	UpdatedAt            time.Time                  `json:"updated_at"`
}

// TechnicalSkillsResponse represents technical skills in response
type TechnicalSkillsResponse struct {
	CodingQuality      int `json:"coding_quality"`
	ProblemSolving     int `json:"problem_solving"`
	TechnologyAdoption int `json:"technology_adoption"`
	TestingPractices   int `json:"testing_practices"`
}

// SoftSkillsResponse represents soft skills in response
type SoftSkillsResponse struct {
	Communication int `json:"communication"`
	Teamwork      int `json:"teamwork"`
	Leadership    int `json:"leadership"`
	Adaptability  int `json:"adaptability"`
}

// EvaluationListResponse represents a paginated list of evaluations
type EvaluationListResponse struct {
	Evaluations []EvaluationResponse `json:"evaluations"`
	Total       int64                `json:"total"`
	Page        int                  `json:"page"`
	PageSize    int                  `json:"page_size"`
	TotalPages  int                  `json:"total_pages"`
}

// EvaluationFilterRequest represents filters for evaluation queries
type EvaluationFilterRequest struct {
	ApprenticeID   *string    `form:"apprentice_id" validate:"omitempty,uuid"`
	ProjectID      *string    `form:"project_id" validate:"omitempty,uuid"`
	SprintID       *string    `form:"sprint_id" validate:"omitempty,uuid"`
	EvaluatorID    *string    `form:"evaluator_id" validate:"omitempty,uuid"`
	EvaluationType *string    `form:"evaluation_type" validate:"omitempty,oneof=self instructor peer comprehensive"`
	DateFrom       *time.Time `form:"date_from,omitempty" time_format:"2006-01-02"`
	DateTo         *time.Time `form:"date_to,omitempty" time_format:"2006-01-02"`
	MinScore       *float64   `form:"min_score" validate:"omitempty,min=1,max=5"`
	MaxScore       *float64   `form:"max_score" validate:"omitempty,min=1,max=5"`
	NeedsImprovement *bool    `form:"needs_improvement"`
	Page           int        `form:"page" validate:"min=1"`
	PageSize       int        `form:"page_size" validate:"min=1,max=100"`
}

// EvaluationStatsResponse represents statistics about evaluations
type EvaluationStatsResponse struct {
	TotalEvaluations       int64                   `json:"total_evaluations"`
	EvaluationsByType      map[string]int64        `json:"evaluations_by_type"`
	AverageOverallScore    float64                 `json:"average_overall_score"`
	AverageTechnicalScore  float64                 `json:"average_technical_score"`
	AverageSoftSkillsScore float64                 `json:"average_soft_skills_score"`
	NeedingImprovement     int64                   `json:"needing_improvement"`
	ImprovementRate        float64                 `json:"improvement_rate"`
	ScoreDistribution      map[string]int64        `json:"score_distribution"`
	WeakestAreas           []WeakAreaStat          `json:"weakest_areas"`
	StrongestAreas         []StrongAreaStat        `json:"strongest_areas"`
}

// WeakAreaStat represents statistics for weak areas
type WeakAreaStat struct {
	Area         string  `json:"area"`
	AverageScore float64 `json:"average_score"`
	Count        int64   `json:"count"`
}

// StrongAreaStat represents statistics for strong areas
type StrongAreaStat struct {
	Area         string  `json:"area"`
	AverageScore float64 `json:"average_score"`
	Count        int64   `json:"count"`
}

// CreateImprovementPlanRequest represents the request to create an improvement plan
type CreateImprovementPlanRequest struct {
	EvaluationID   string                      `json:"evaluation_id" binding:"required" validate:"uuid"`
	CompetencyArea string                      `json:"competency_area" binding:"required,min=3,max=100"`
	CurrentLevel   int                         `json:"current_level" binding:"required,min=1,max=5"`
	TargetLevel    int                         `json:"target_level" binding:"required,min=1,max=5"`
	Activities     []ActivityRequest           `json:"activities" binding:"required,min=1"`
	Resources      []ResourceRequest           `json:"resources" binding:"required,min=1"`
	Timeline       TimelineRequest             `json:"timeline" binding:"required"`
}

// ActivityRequest represents an activity in improvement plan
type ActivityRequest struct {
	Name        string    `json:"name" binding:"required"`
	Description string    `json:"description" binding:"required"`
	Type        string    `json:"type" binding:"required,oneof=practice study mentoring project"`
	Duration    int       `json:"duration" binding:"required,min=1"`
	DueDate     time.Time `json:"due_date" binding:"required"`
}

// ResourceRequest represents a learning resource
type ResourceRequest struct {
	Type        string `json:"type" binding:"required,oneof=article video course book documentation"`
	Title       string `json:"title" binding:"required"`
	URL         string `json:"url" binding:"required,url"`
	Description string `json:"description,omitempty"`
}

// TimelineRequest represents the timeline for improvement plan
type TimelineRequest struct {
	StartDate     time.Time  `json:"start_date" binding:"required"`
	EndDate       time.Time  `json:"end_date" binding:"required"`
	MilestoneDate *time.Time `json:"milestone_date,omitempty"`
	ReviewDate    time.Time  `json:"review_date" binding:"required"`
}

// ImprovementPlanResponse represents an improvement plan in API responses
type ImprovementPlanResponse struct {
	ID              string                 `json:"id"`
	EvaluationID    string                 `json:"evaluation_id"`
	CompetencyArea  string                 `json:"competency_area"`
	CurrentLevel    int                    `json:"current_level"`
	TargetLevel     int                    `json:"target_level"`
	Activities      []ActivityResponse     `json:"activities"`
	Resources       []ResourceResponse     `json:"resources"`
	Timeline        TimelineResponse       `json:"timeline"`
	Status          string                 `json:"status"`
	Progress        int                    `json:"progress"`
	IsActive        bool                   `json:"is_active"`
	IsOverdue       bool                   `json:"is_overdue"`
	CanComplete     bool                   `json:"can_complete"`
	CreatedAt       time.Time              `json:"created_at"`
	UpdatedAt       time.Time              `json:"updated_at"`
}

// ActivityResponse represents an activity in response
type ActivityResponse struct {
	Name        string    `json:"name"`
	Description string    `json:"description"`
	Type        string    `json:"type"`
	Duration    int       `json:"duration"`
	IsCompleted bool      `json:"is_completed"`
	DueDate     time.Time `json:"due_date"`
}

// ResourceResponse represents a resource in response
type ResourceResponse struct {
	Type        string `json:"type"`
	Title       string `json:"title"`
	URL         string `json:"url"`
	Description string `json:"description"`
	IsAccessed  bool   `json:"is_accessed"`
}

// TimelineResponse represents timeline in response
type TimelineResponse struct {
	StartDate     time.Time  `json:"start_date"`
	EndDate       time.Time  `json:"end_date"`
	MilestoneDate *time.Time `json:"milestone_date,omitempty"`
	ReviewDate    time.Time  `json:"review_date"`
}

// Conversion methods

// ToEntity converts CreateEvaluationRequest to entities.Evaluation
func (r *CreateEvaluationRequest) ToEntity() (*entities.Evaluation, error) {
	apprenticeID, err := uuid.Parse(r.ApprenticeID)
	if err != nil {
		return nil, err
	}

	projectID, err := uuid.Parse(r.ProjectID)
	if err != nil {
		return nil, err
	}

	evaluatorID, err := uuid.Parse(r.EvaluatorID)
	if err != nil {
		return nil, err
	}

	evaluation := &entities.Evaluation{
		ApprenticeID:   apprenticeID,
		ProjectID:      projectID,
		EvaluatorID:    evaluatorID,
		EvaluationType: entities.EvaluationType(r.EvaluationType),
		EvaluationDate: r.EvaluationDate,
		TechnicalSkills: entities.TechnicalSkills{
			CodingQuality:      r.TechnicalSkills.CodingQuality,
			ProblemSolving:     r.TechnicalSkills.ProblemSolving,
			TechnologyAdoption: r.TechnicalSkills.TechnologyAdoption,
			TestingPractices:   r.TechnicalSkills.TestingPractices,
		},
		SoftSkills: entities.SoftSkills{
			Communication: r.SoftSkills.Communication,
			Teamwork:      r.SoftSkills.Teamwork,
			Leadership:    r.SoftSkills.Leadership,
			Adaptability:  r.SoftSkills.Adaptability,
		},
		LearningObjectivesMet: r.LearningObjectivesMet,
		AreasForImprovement:   r.AreasForImprovement,
		Recommendations:       r.Recommendations,
		Notes:                 r.Notes,
	}

	// Convert SprintID if provided
	if r.SprintID != nil {
		sprintID, err := uuid.Parse(*r.SprintID)
		if err != nil {
			return nil, err
		}
		evaluation.SprintID = &sprintID
	}

	// Calculate overall score
	evaluation.OverallScore = evaluation.CalculateOverallScore()

	return evaluation, nil
}

// FromEntity converts entities.Evaluation to EvaluationResponse
func (r *EvaluationResponse) FromEntity(evaluation *entities.Evaluation) {
	r.ID = evaluation.ID.String()
	r.ApprenticeID = evaluation.ApprenticeID.String()
	r.ProjectID = evaluation.ProjectID.String()
	r.EvaluatorID = evaluation.EvaluatorID.String()
	
	if evaluation.SprintID != nil {
		sprintIDStr := evaluation.SprintID.String()
		r.SprintID = &sprintIDStr
	}

	r.EvaluationType = string(evaluation.EvaluationType)
	r.EvaluationDate = evaluation.EvaluationDate
	
	r.TechnicalSkills = TechnicalSkillsResponse{
		CodingQuality:      evaluation.TechnicalSkills.CodingQuality,
		ProblemSolving:     evaluation.TechnicalSkills.ProblemSolving,
		TechnologyAdoption: evaluation.TechnicalSkills.TechnologyAdoption,
		TestingPractices:   evaluation.TechnicalSkills.TestingPractices,
	}
	
	r.SoftSkills = SoftSkillsResponse{
		Communication: evaluation.SoftSkills.Communication,
		Teamwork:      evaluation.SoftSkills.Teamwork,
		Leadership:    evaluation.SoftSkills.Leadership,
		Adaptability:  evaluation.SoftSkills.Adaptability,
	}

	r.LearningObjectivesMet = evaluation.LearningObjectivesMet
	r.AreasForImprovement = evaluation.AreasForImprovement
	r.Recommendations = evaluation.Recommendations
	r.OverallScore = evaluation.OverallScore
	r.TechnicalAverage = evaluation.GetTechnicalAverage()
	r.SoftSkillsAverage = evaluation.GetSoftSkillsAverage()
	r.Notes = evaluation.Notes
	r.NeedsImprovement = evaluation.NeedsImprovement()
	r.WeakAreas = evaluation.GetWeakAreas()
	r.CreatedAt = evaluation.CreatedAt
	r.UpdatedAt = evaluation.UpdatedAt
}

// FromEntityList converts a slice of entities.Evaluation to EvaluationListResponse
func (r *EvaluationListResponse) FromEntityList(evaluations []entities.Evaluation, total int64, page, pageSize int) {
	r.Evaluations = make([]EvaluationResponse, len(evaluations))
	for i, evaluation := range evaluations {
		r.Evaluations[i].FromEntity(&evaluation)
	}
	r.Total = total
	r.Page = page
	r.PageSize = pageSize
	if pageSize > 0 {
		r.TotalPages = int((total + int64(pageSize) - 1) / int64(pageSize))
	}
}

// ApplyToEntity applies UpdateEvaluationRequest to an existing entities.Evaluation
func (r *UpdateEvaluationRequest) ApplyToEntity(evaluation *entities.Evaluation) error {
	if r.EvaluationType != nil {
		evaluation.EvaluationType = entities.EvaluationType(*r.EvaluationType)
	}
	if r.EvaluationDate != nil {
		evaluation.EvaluationDate = *r.EvaluationDate
	}
	if r.TechnicalSkills != nil {
		evaluation.TechnicalSkills = entities.TechnicalSkills{
			CodingQuality:      r.TechnicalSkills.CodingQuality,
			ProblemSolving:     r.TechnicalSkills.ProblemSolving,
			TechnologyAdoption: r.TechnicalSkills.TechnologyAdoption,
			TestingPractices:   r.TechnicalSkills.TestingPractices,
		}
	}
	if r.SoftSkills != nil {
		evaluation.SoftSkills = entities.SoftSkills{
			Communication: r.SoftSkills.Communication,
			Teamwork:      r.SoftSkills.Teamwork,
			Leadership:    r.SoftSkills.Leadership,
			Adaptability:  r.SoftSkills.Adaptability,
		}
	}
	if r.LearningObjectivesMet != nil {
		evaluation.LearningObjectivesMet = r.LearningObjectivesMet
	}
	if r.AreasForImprovement != nil {
		evaluation.AreasForImprovement = r.AreasForImprovement
	}
	if r.Recommendations != nil {
		evaluation.Recommendations = *r.Recommendations
	}
	if r.Notes != nil {
		evaluation.Notes = *r.Notes
	}

	// Recalculate overall score if technical or soft skills were updated
	if r.TechnicalSkills != nil || r.SoftSkills != nil {
		evaluation.OverallScore = evaluation.CalculateOverallScore()
	}

	return nil
}

// ToEntity converts CreateImprovementPlanRequest to entities.ImprovementPlan
func (r *CreateImprovementPlanRequest) ToEntity() (*entities.ImprovementPlan, error) {
	evaluationID, err := uuid.Parse(r.EvaluationID)
	if err != nil {
		return nil, err
	}

	activities := make([]entities.Activity, len(r.Activities))
	for i, activity := range r.Activities {
		activities[i] = entities.Activity{
			Name:        activity.Name,
			Description: activity.Description,
			Type:        activity.Type,
			Duration:    activity.Duration,
			IsCompleted: false,
			DueDate:     activity.DueDate,
		}
	}

	resources := make([]entities.Resource, len(r.Resources))
	for i, resource := range r.Resources {
		resources[i] = entities.Resource{
			Type:        resource.Type,
			Title:       resource.Title,
			URL:         resource.URL,
			Description: resource.Description,
			IsAccessed:  false,
		}
	}

	plan := &entities.ImprovementPlan{
		EvaluationID:   evaluationID,
		CompetencyArea: r.CompetencyArea,
		CurrentLevel:   r.CurrentLevel,
		TargetLevel:    r.TargetLevel,
		Activities:     activities,
		Resources:      resources,
		Timeline: entities.Timeline{
			StartDate:     r.Timeline.StartDate,
			EndDate:       r.Timeline.EndDate,
			MilestoneDate: r.Timeline.MilestoneDate,
			ReviewDate:    r.Timeline.ReviewDate,
		},
		Status:   entities.PlanStatusActive,
		Progress: 0,
	}

	return plan, nil
}

// FromEntity converts entities.ImprovementPlan to ImprovementPlanResponse
func (r *ImprovementPlanResponse) FromEntity(plan *entities.ImprovementPlan) {
	r.ID = plan.ID.String()
	r.EvaluationID = plan.EvaluationID.String()
	r.CompetencyArea = plan.CompetencyArea
	r.CurrentLevel = plan.CurrentLevel
	r.TargetLevel = plan.TargetLevel
	r.Status = string(plan.Status)
	r.Progress = plan.Progress
	r.IsActive = plan.IsActive()
	r.IsOverdue = plan.IsOverdue()
	r.CanComplete = plan.CanComplete()
	r.CreatedAt = plan.CreatedAt
	r.UpdatedAt = plan.UpdatedAt

	// Convert Activities
	r.Activities = make([]ActivityResponse, len(plan.Activities))
	for i, activity := range plan.Activities {
		r.Activities[i] = ActivityResponse{
			Name:        activity.Name,
			Description: activity.Description,
			Type:        activity.Type,
			Duration:    activity.Duration,
			IsCompleted: activity.IsCompleted,
			DueDate:     activity.DueDate,
		}
	}

	// Convert Resources
	r.Resources = make([]ResourceResponse, len(plan.Resources))
	for i, resource := range plan.Resources {
		r.Resources[i] = ResourceResponse{
			Type:        resource.Type,
			Title:       resource.Title,
			URL:         resource.URL,
			Description: resource.Description,
			IsAccessed:  resource.IsAccessed,
		}
	}

	// Convert Timeline
	r.Timeline = TimelineResponse{
		StartDate:     plan.Timeline.StartDate,
		EndDate:       plan.Timeline.EndDate,
		MilestoneDate: plan.Timeline.MilestoneDate,
		ReviewDate:    plan.Timeline.ReviewDate,
	}
}
