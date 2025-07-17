package entities_test

import (
	"testing"

	"github.com/google/uuid"

	"softwarefactoryservice/internal/domain/entities"
)

func TestProject_Validate(t *testing.T) {
	tests := []struct {
		name        string
		project     *entities.Project
		expectError bool
	}{
		{
			name: "valid project",
			project: &entities.Project{
				Name:                   "Test Project",
				Description:            "A test project description that is long enough to pass validation",
				TechStack:              []string{"Go", "PostgreSQL", "React"},
				LearningObjectives:     []string{"Learn Go development", "Database design"},
				ComplexityLevel:        entities.ComplexityIntermediate,
				EstimatedDurationWeeks: 12,
				Status:                 entities.ProjectStatusPlanning,
				CreatedBy:             uuid.New(),
			},
			expectError: false,
		},
		{
			name: "invalid project - no tech stack",
			project: &entities.Project{
				Name:                   "Test Project",
				Description:            "A test project description that is long enough to pass validation",
				TechStack:              []string{},
				LearningObjectives:     []string{"Learn Go development", "Database design"},
				ComplexityLevel:        entities.ComplexityIntermediate,
				EstimatedDurationWeeks: 12,
				Status:                 entities.ProjectStatusPlanning,
				CreatedBy:             uuid.New(),
			},
			expectError: true,
		},
		{
			name: "invalid project - no learning objectives",
			project: &entities.Project{
				Name:                   "Test Project",
				Description:            "A test project description that is long enough to pass validation",
				TechStack:              []string{"Go", "PostgreSQL", "React"},
				LearningObjectives:     []string{},
				ComplexityLevel:        entities.ComplexityIntermediate,
				EstimatedDurationWeeks: 12,
				Status:                 entities.ProjectStatusPlanning,
				CreatedBy:             uuid.New(),
			},
			expectError: true,
		},
		{
			name: "invalid project - duration too short",
			project: &entities.Project{
				Name:                   "Test Project",
				Description:            "A test project description that is long enough to pass validation",
				TechStack:              []string{"Go", "PostgreSQL", "React"},
				LearningObjectives:     []string{"Learn Go development", "Database design"},
				ComplexityLevel:        entities.ComplexityIntermediate,
				EstimatedDurationWeeks: 2,
				Status:                 entities.ProjectStatusPlanning,
				CreatedBy:             uuid.New(),
			},
			expectError: true,
		},
	}

	for _, tt := range tests {
		t.Run(tt.name, func(t *testing.T) {
			err := tt.project.Validate()
			if tt.expectError && err == nil {
				t.Errorf("Expected error but got none")
			}
			if !tt.expectError && err != nil {
				t.Errorf("Expected no error but got: %v", err)
			}
		})
	}
}

func TestProject_IsActive(t *testing.T) {
	tests := []struct {
		name     string
		status   entities.ProjectStatus
		expected bool
	}{
		{"active project", entities.ProjectStatusActive, true},
		{"planning project", entities.ProjectStatusPlanning, false},
		{"completed project", entities.ProjectStatusCompleted, false},
		{"cancelled project", entities.ProjectStatusCancelled, false},
	}

	for _, tt := range tests {
		t.Run(tt.name, func(t *testing.T) {
			project := &entities.Project{Status: tt.status}
			if result := project.IsActive(); result != tt.expected {
				t.Errorf("Expected %v but got %v", tt.expected, result)
			}
		})
	}
}
