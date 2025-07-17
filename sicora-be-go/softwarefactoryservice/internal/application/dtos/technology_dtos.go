package dtos

import (
	"time"

	"softwarefactoryservice/internal/domain/entities"

	"github.com/google/uuid"
)

// CreateTechnologyRequest represents the request to create a new technology
type CreateTechnologyRequest struct {
	Name              string                       `json:"name" binding:"required,min=2,max=100"`
	Version           string                       `json:"version" binding:"required,max=50"`
	Category          string                       `json:"category" binding:"required,oneof=frontend backend database devops testing mobile tools"`
	Level             string                       `json:"level" binding:"required,oneof=beginner intermediate advanced expert"`
	Description       string                       `json:"description" binding:"required,min=10"`
	LicenseType       string                       `json:"license_type" binding:"required,oneof=opensource educational commercial free"`
	Status            string                       `json:"status" binding:"required,oneof=active deprecated experimental planned"`
	LogoURL           string                       `json:"logo_url,omitempty" validate:"omitempty,url"`
	DocumentationURL  string                       `json:"documentation_url,omitempty" validate:"omitempty,url"`
	LearningResources []LearningResourceRequest    `json:"learning_resources,omitempty"`
	Tags              []string                     `json:"tags,omitempty"`
	Compatibility     []string                     `json:"compatibility,omitempty" validate:"dive,uuid"`
	Prerequisites     []string                     `json:"prerequisites,omitempty"`
	LicenseLimit      int                          `json:"license_limit" binding:"min=0"`
	RenewalDate       *time.Time                   `json:"renewal_date,omitempty"`
	Cost              float64                      `json:"cost" binding:"min=0"`
	CreatedBy         string                       `json:"created_by" binding:"required" validate:"uuid"`
}

// LearningResourceRequest represents a learning resource in request
type LearningResourceRequest struct {
	Type        string  `json:"type" binding:"required,oneof=tutorial course documentation video book"`
	Title       string  `json:"title" binding:"required"`
	URL         string  `json:"url" binding:"required,url"`
	Duration    string  `json:"duration,omitempty"`
	Level       string  `json:"level" binding:"required,oneof=beginner intermediate advanced"`
	Language    string  `json:"language" binding:"required,len=2"`
	IsFree      bool    `json:"is_free"`
	Rating      float64 `json:"rating,omitempty" validate:"omitempty,min=1,max=5"`
}

// UpdateTechnologyRequest represents the request to update a technology
type UpdateTechnologyRequest struct {
	Name              *string                      `json:"name,omitempty" validate:"omitempty,min=2,max=100"`
	Version           *string                      `json:"version,omitempty" validate:"omitempty,max=50"`
	Category          *string                      `json:"category,omitempty" validate:"omitempty,oneof=frontend backend database devops testing mobile tools"`
	Level             *string                      `json:"level,omitempty" validate:"omitempty,oneof=beginner intermediate advanced expert"`
	Description       *string                      `json:"description,omitempty" validate:"omitempty,min=10"`
	LicenseType       *string                      `json:"license_type,omitempty" validate:"omitempty,oneof=opensource educational commercial free"`
	Status            *string                      `json:"status,omitempty" validate:"omitempty,oneof=active deprecated experimental planned"`
	LogoURL           *string                      `json:"logo_url,omitempty" validate:"omitempty,url"`
	DocumentationURL  *string                      `json:"documentation_url,omitempty" validate:"omitempty,url"`
	LearningResources []LearningResourceRequest    `json:"learning_resources,omitempty"`
	Tags              []string                     `json:"tags,omitempty"`
	Compatibility     []string                     `json:"compatibility,omitempty" validate:"dive,uuid"`
	Prerequisites     []string                     `json:"prerequisites,omitempty"`
	LicenseLimit      *int                         `json:"license_limit,omitempty" validate:"omitempty,min=0"`
	RenewalDate       *time.Time                   `json:"renewal_date,omitempty"`
	Cost              *float64                     `json:"cost,omitempty" validate:"omitempty,min=0"`
}

// TechnologyResponse represents a technology in API responses
type TechnologyResponse struct {
	ID                string                    `json:"id"`
	Name              string                    `json:"name"`
	Version           string                    `json:"version"`
	Category          string                    `json:"category"`
	Level             string                    `json:"level"`
	Description       string                    `json:"description"`
	LicenseType       string                    `json:"license_type"`
	Status            string                    `json:"status"`
	LogoURL           string                    `json:"logo_url"`
	DocumentationURL  string                    `json:"documentation_url"`
	LearningResources []LearningResourceResponse `json:"learning_resources"`
	Tags              []string                  `json:"tags"`
	Compatibility     []string                  `json:"compatibility"`
	Prerequisites     []string                  `json:"prerequisites"`
	LicenseLimit      int                       `json:"license_limit"`
	LicenseUsed       int                       `json:"license_used"`
	LicenseAvailable  int                       `json:"license_available"`
	RenewalDate       *time.Time                `json:"renewal_date,omitempty"`
	Cost              float64                   `json:"cost"`
	PopularityScore   int                       `json:"popularity_score"`
	CreatedBy         string                    `json:"created_by"`
	CreatedAt         time.Time                 `json:"created_at"`
	UpdatedAt         time.Time                 `json:"updated_at"`
}

// LearningResourceResponse represents a learning resource in response
type LearningResourceResponse struct {
	Type        string  `json:"type"`
	Title       string  `json:"title"`
	URL         string  `json:"url"`
	Duration    string  `json:"duration,omitempty"`
	Level       string  `json:"level"`
	Language    string  `json:"language"`
	IsFree      bool    `json:"is_free"`
	Rating      float64 `json:"rating,omitempty"`
}

// TechnologyListResponse represents a paginated list of technologies
type TechnologyListResponse struct {
	Technologies []TechnologyResponse `json:"technologies"`
	Total        int64                `json:"total"`
	Page         int                  `json:"page"`
	PageSize     int                  `json:"page_size"`
	TotalPages   int                  `json:"total_pages"`
}

// TechnologyFilterRequest represents filters for technology queries
type TechnologyFilterRequest struct {
	Category        *string `form:"category" validate:"omitempty,oneof=frontend backend database devops testing mobile tools"`
	Level           *string `form:"level" validate:"omitempty,oneof=beginner intermediate advanced expert"`
	LicenseType     *string `form:"license_type" validate:"omitempty,oneof=opensource educational commercial free"`
	Status          *string `form:"status" validate:"omitempty,oneof=active deprecated experimental planned"`
	Tags            *string `form:"tags"` // Comma-separated tags
	MinCost         *float64 `form:"min_cost" validate:"omitempty,min=0"`
	MaxCost         *float64 `form:"max_cost" validate:"omitempty,min=0"`
	FreeOnly        *bool   `form:"free_only"`
	LicenseAvailable *bool  `form:"license_available"`
	Search          *string `form:"search"`
	Page            int     `form:"page" validate:"min=1"`
	PageSize        int     `form:"page_size" validate:"min=1,max=100"`
}

// TechnologyStatsResponse represents statistics about technologies
type TechnologyStatsResponse struct {
	TotalTechnologies     int64                   `json:"total_technologies"`
	TechnologiesByCategory map[string]int64       `json:"technologies_by_category"`
	TechnologiesByLevel   map[string]int64        `json:"technologies_by_level"`
	TechnologiesByLicense map[string]int64        `json:"technologies_by_license"`
	TechnologiesByStatus  map[string]int64        `json:"technologies_by_status"`
	MostPopular           []PopularTechnologyStat `json:"most_popular"`
	LicenseUtilization    []LicenseUtilizationStat `json:"license_utilization"`
	AverageCost           float64                 `json:"average_cost"`
	TotalLicenseCost      float64                 `json:"total_license_cost"`
}

// PopularTechnologyStat represents popularity statistics
type PopularTechnologyStat struct {
	TechnologyID    string `json:"technology_id"`
	Name            string `json:"name"`
	PopularityScore int    `json:"popularity_score"`
	UsageCount      int64  `json:"usage_count"`
}

// LicenseUtilizationStat represents license utilization statistics
type LicenseUtilizationStat struct {
	TechnologyID     string  `json:"technology_id"`
	Name             string  `json:"name"`
	LicenseLimit     int     `json:"license_limit"`
	LicenseUsed      int     `json:"license_used"`
	UtilizationRate  float64 `json:"utilization_rate"`
	Cost             float64 `json:"cost"`
}

// CreateTechnologyUsageRequest represents the request to create a technology usage record
type CreateTechnologyUsageRequest struct {
	TechnologyID string    `json:"technology_id" binding:"required" validate:"uuid"`
	ProjectID    string    `json:"project_id" binding:"required" validate:"uuid"`
	TeamID       string    `json:"team_id" binding:"required" validate:"uuid"`
	StartDate    time.Time `json:"start_date" binding:"required"`
}

// UpdateTechnologyUsageRequest represents the request to update a technology usage record
type UpdateTechnologyUsageRequest struct {
	EndDate      *time.Time `json:"end_date,omitempty"`
	SuccessRate  *float64   `json:"success_rate,omitempty" validate:"omitempty,min=0,max=100"`
	Satisfaction *int       `json:"satisfaction,omitempty" validate:"omitempty,min=1,max=5"`
	Feedback     *string    `json:"feedback,omitempty"`
}

// TechnologyUsageResponse represents a technology usage record in API responses
type TechnologyUsageResponse struct {
	ID           string    `json:"id"`
	TechnologyID string    `json:"technology_id"`
	ProjectID    string    `json:"project_id"`
	TeamID       string    `json:"team_id"`
	StartDate    time.Time `json:"start_date"`
	EndDate      *time.Time `json:"end_date,omitempty"`
	SuccessRate  float64   `json:"success_rate"`
	Satisfaction int       `json:"satisfaction"`
	Feedback     string    `json:"feedback"`
	CreatedAt    time.Time `json:"created_at"`
}

// TechnologyRecommendationRequest represents a request for technology recommendations
type TechnologyRecommendationRequest struct {
	ProjectType    string   `json:"project_type" binding:"required"`
	TeamSize       int      `json:"team_size" binding:"required,min=1"`
	ExperienceLevel string  `json:"experience_level" binding:"required,oneof=beginner intermediate advanced"`
	Budget         float64  `json:"budget" binding:"min=0"`
	Timeline       string   `json:"timeline" binding:"required"` // "1 month", "3 months", etc.
	RequiredSkills []string `json:"required_skills,omitempty"`
	Preferences    []string `json:"preferences,omitempty"`
}

// TechnologyRecommendationResponse represents technology recommendations
type TechnologyRecommendationResponse struct {
	RecommendedTechnologies []TechnologyRecommendation `json:"recommended_technologies"`
	AlternativeTechnologies []TechnologyRecommendation `json:"alternative_technologies"`
	TotalCost               float64                    `json:"total_cost"`
	LearningPath            []LearningPathStep         `json:"learning_path"`
	RiskAssessment          string                     `json:"risk_assessment"`
	EstimatedLearningTime   string                     `json:"estimated_learning_time"`
}

// TechnologyRecommendation represents a single technology recommendation
type TechnologyRecommendation struct {
	Technology    TechnologyResponse `json:"technology"`
	ReasonScore   float64           `json:"reason_score"`
	Reasons       []string          `json:"reasons"`
	Prerequisites []string          `json:"prerequisites"`
	LearningTime  string            `json:"learning_time"`
}

// LearningPathStep represents a step in the learning path
type LearningPathStep struct {
	Order        int    `json:"order"`
	Technology   string `json:"technology"`
	Description  string `json:"description"`
	Duration     string `json:"duration"`
	IsOptional   bool   `json:"is_optional"`
	Dependencies []string `json:"dependencies"`
}

// Conversion methods

// ToEntity converts CreateTechnologyRequest to entities.Technology
func (r *CreateTechnologyRequest) ToEntity() (*entities.Technology, error) {
	createdBy, err := uuid.Parse(r.CreatedBy)
	if err != nil {
		return nil, err
	}

	technology := &entities.Technology{
		Name:             r.Name,
		Version:          r.Version,
		Category:         entities.TechnologyCategory(r.Category),
		Level:            entities.TechnologyLevel(r.Level),
		Description:      r.Description,
		LicenseType:      entities.LicenseType(r.LicenseType),
		Status:           entities.TechnologyStatus(r.Status),
		LogoURL:          r.LogoURL,
		DocumentationURL: r.DocumentationURL,
		Tags:             r.Tags,
		Compatibility:    r.Compatibility,
		Prerequisites:    r.Prerequisites,
		LicenseLimit:     r.LicenseLimit,
		RenewalDate:      r.RenewalDate,
		Cost:             r.Cost,
		CreatedBy:        createdBy,
	}

	// Convert LearningResources
	if len(r.LearningResources) > 0 {
		learningResources := make([]entities.LearningResource, len(r.LearningResources))
		for i, resource := range r.LearningResources {
			learningResources[i] = entities.LearningResource{
				Type:     resource.Type,
				Title:    resource.Title,
				URL:      resource.URL,
				Duration: resource.Duration,
				Level:    resource.Level,
				Language: resource.Language,
				IsFree:   resource.IsFree,
				Rating:   resource.Rating,
			}
		}
		technology.LearningResources = learningResources
	}

	return technology, nil
}

// FromEntity converts entities.Technology to TechnologyResponse
func (r *TechnologyResponse) FromEntity(technology *entities.Technology) {
	r.ID = technology.ID.String()
	r.Name = technology.Name
	r.Version = technology.Version
	r.Category = string(technology.Category)
	r.Level = string(technology.Level)
	r.Description = technology.Description
	r.LicenseType = string(technology.LicenseType)
	r.Status = string(technology.Status)
	r.LogoURL = technology.LogoURL
	r.DocumentationURL = technology.DocumentationURL
	r.Tags = technology.Tags
	r.Compatibility = technology.Compatibility
	r.Prerequisites = technology.Prerequisites
	r.LicenseLimit = technology.LicenseLimit
	r.LicenseUsed = technology.LicenseUsed
	r.RenewalDate = technology.RenewalDate
	r.Cost = technology.Cost
	r.PopularityScore = technology.PopularityScore
	r.CreatedBy = technology.CreatedBy.String()
	r.CreatedAt = technology.CreatedAt
	r.UpdatedAt = technology.UpdatedAt

	// Calculate available licenses
	if technology.LicenseLimit > 0 {
		r.LicenseAvailable = technology.LicenseLimit - technology.LicenseUsed
	} else {
		r.LicenseAvailable = -1 // Unlimited
	}

	// Convert LearningResources
	if len(technology.LearningResources) > 0 {
		learningResources := make([]LearningResourceResponse, len(technology.LearningResources))
		for i, resource := range technology.LearningResources {
			learningResources[i] = LearningResourceResponse{
				Type:     resource.Type,
				Title:    resource.Title,
				URL:      resource.URL,
				Duration: resource.Duration,
				Level:    resource.Level,
				Language: resource.Language,
				IsFree:   resource.IsFree,
				Rating:   resource.Rating,
			}
		}
		r.LearningResources = learningResources
	}
}

// FromEntityList converts a slice of entities.Technology to TechnologyListResponse
func (r *TechnologyListResponse) FromEntityList(technologies []entities.Technology, total int64, page, pageSize int) {
	r.Technologies = make([]TechnologyResponse, len(technologies))
	for i, technology := range technologies {
		r.Technologies[i].FromEntity(&technology)
	}
	r.Total = total
	r.Page = page
	r.PageSize = pageSize
	if pageSize > 0 {
		r.TotalPages = int((total + int64(pageSize) - 1) / int64(pageSize))
	}
}

// ApplyToEntity applies UpdateTechnologyRequest to an existing entities.Technology
func (r *UpdateTechnologyRequest) ApplyToEntity(technology *entities.Technology) error {
	if r.Name != nil {
		technology.Name = *r.Name
	}
	if r.Version != nil {
		technology.Version = *r.Version
	}
	if r.Category != nil {
		technology.Category = entities.TechnologyCategory(*r.Category)
	}
	if r.Level != nil {
		technology.Level = entities.TechnologyLevel(*r.Level)
	}
	if r.Description != nil {
		technology.Description = *r.Description
	}
	if r.LicenseType != nil {
		technology.LicenseType = entities.LicenseType(*r.LicenseType)
	}
	if r.Status != nil {
		technology.Status = entities.TechnologyStatus(*r.Status)
	}
	if r.LogoURL != nil {
		technology.LogoURL = *r.LogoURL
	}
	if r.DocumentationURL != nil {
		technology.DocumentationURL = *r.DocumentationURL
	}
	if r.Tags != nil {
		technology.Tags = r.Tags
	}
	if r.Compatibility != nil {
		technology.Compatibility = r.Compatibility
	}
	if r.Prerequisites != nil {
		technology.Prerequisites = r.Prerequisites
	}
	if r.LicenseLimit != nil {
		technology.LicenseLimit = *r.LicenseLimit
	}
	if r.RenewalDate != nil {
		technology.RenewalDate = r.RenewalDate
	}
	if r.Cost != nil {
		technology.Cost = *r.Cost
	}

	// Convert LearningResources if provided
	if r.LearningResources != nil {
		learningResources := make([]entities.LearningResource, len(r.LearningResources))
		for i, resource := range r.LearningResources {
			learningResources[i] = entities.LearningResource{
				Type:     resource.Type,
				Title:    resource.Title,
				URL:      resource.URL,
				Duration: resource.Duration,
				Level:    resource.Level,
				Language: resource.Language,
				IsFree:   resource.IsFree,
				Rating:   resource.Rating,
			}
		}
		technology.LearningResources = learningResources
	}

	return nil
}

// ToEntity converts CreateTechnologyUsageRequest to entities.TechnologyUsage
func (r *CreateTechnologyUsageRequest) ToEntity() (*entities.TechnologyUsage, error) {
	technologyID, err := uuid.Parse(r.TechnologyID)
	if err != nil {
		return nil, err
	}

	projectID, err := uuid.Parse(r.ProjectID)
	if err != nil {
		return nil, err
	}

	teamID, err := uuid.Parse(r.TeamID)
	if err != nil {
		return nil, err
	}

	usage := &entities.TechnologyUsage{
		TechnologyID: technologyID,
		ProjectID:    projectID,
		TeamID:       teamID,
		StartDate:    r.StartDate,
		SuccessRate:  0.0,
		Satisfaction: 0,
	}

	return usage, nil
}

// FromEntity converts entities.TechnologyUsage to TechnologyUsageResponse
func (r *TechnologyUsageResponse) FromEntity(usage *entities.TechnologyUsage) {
	r.ID = usage.ID.String()
	r.TechnologyID = usage.TechnologyID.String()
	r.ProjectID = usage.ProjectID.String()
	r.TeamID = usage.TeamID.String()
	r.StartDate = usage.StartDate
	r.EndDate = usage.EndDate
	r.SuccessRate = usage.SuccessRate
	r.Satisfaction = usage.Satisfaction
	r.Feedback = usage.Feedback
	r.CreatedAt = usage.CreatedAt
}

// ApplyToEntity applies UpdateTechnologyUsageRequest to an existing entities.TechnologyUsage
func (r *UpdateTechnologyUsageRequest) ApplyToEntity(usage *entities.TechnologyUsage) error {
	if r.EndDate != nil {
		usage.EndDate = r.EndDate
	}
	if r.SuccessRate != nil {
		usage.SuccessRate = *r.SuccessRate
	}
	if r.Satisfaction != nil {
		usage.Satisfaction = *r.Satisfaction
	}
	if r.Feedback != nil {
		usage.Feedback = *r.Feedback
	}
	return nil
}
