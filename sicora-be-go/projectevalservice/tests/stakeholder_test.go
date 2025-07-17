package tests

import (
	"testing"
	"time"

	"projectevalservice/internal/domain/entities"

	"github.com/google/uuid"
	"github.com/stretchr/testify/assert"
)

func TestNewStakeholder(t *testing.T) {
	projectID := uuid.New()
	userID := uuid.New()
	role := entities.StakeholderRoleCoordinator
	stakeholderType := entities.StakeholderTypeInternal

	stakeholder := entities.NewStakeholder(projectID, userID, role, stakeholderType)

	assert.Equal(t, projectID, stakeholder.ProjectID)
	assert.Equal(t, userID, stakeholder.UserID)
	assert.Equal(t, role, stakeholder.Role)
	assert.Equal(t, stakeholderType, stakeholder.Type)
	assert.Equal(t, entities.StakeholderStatusActive, stakeholder.Status)
	assert.Equal(t, 1, stakeholder.AccessLevel)
	assert.False(t, stakeholder.CanEvaluate)
	assert.False(t, stakeholder.CanReview)
	assert.False(t, stakeholder.CanApprove)
	assert.NotEqual(t, uuid.Nil, stakeholder.ID)
}

func TestStakeholder_IsValid(t *testing.T) {
	t.Run("Valid stakeholder", func(t *testing.T) {
		stakeholder := entities.NewStakeholder(
			uuid.New(),
			uuid.New(),
			entities.StakeholderRoleCoordinator,
			entities.StakeholderTypeInternal,
		)

		err := stakeholder.IsValid()
		assert.NoError(t, err)
	})

	t.Run("Invalid project ID", func(t *testing.T) {
		stakeholder := entities.NewStakeholder(
			uuid.Nil,
			uuid.New(),
			entities.StakeholderRoleCoordinator,
			entities.StakeholderTypeInternal,
		)

		err := stakeholder.IsValid()
		assert.Error(t, err)
		assert.Contains(t, err.Error(), "project ID is required")
	})

	t.Run("Invalid user ID", func(t *testing.T) {
		stakeholder := entities.NewStakeholder(
			uuid.New(),
			uuid.Nil,
			entities.StakeholderRoleCoordinator,
			entities.StakeholderTypeInternal,
		)

		err := stakeholder.IsValid()
		assert.Error(t, err)
		assert.Contains(t, err.Error(), "user ID is required")
	})

	t.Run("Invalid role", func(t *testing.T) {
		stakeholder := entities.NewStakeholder(
			uuid.New(),
			uuid.New(),
			"invalid_role",
			entities.StakeholderTypeInternal,
		)

		err := stakeholder.IsValid()
		assert.Error(t, err)
		assert.Contains(t, err.Error(), "invalid stakeholder role")
	})

	t.Run("Invalid access level", func(t *testing.T) {
		stakeholder := entities.NewStakeholder(
			uuid.New(),
			uuid.New(),
			entities.StakeholderRoleCoordinator,
			entities.StakeholderTypeInternal,
		)
		stakeholder.AccessLevel = 6

		err := stakeholder.IsValid()
		assert.Error(t, err)
		assert.Contains(t, err.Error(), "access level must be between 1 and 5")
	})
}

func TestStakeholder_IsValidRole(t *testing.T) {
	stakeholder := &entities.Stakeholder{}

	validRoles := []entities.StakeholderRole{
		entities.StakeholderRoleCoordinator,
		entities.StakeholderRoleJuror,
		entities.StakeholderRoleManager,
		entities.StakeholderRoleExternal,
		entities.StakeholderRoleObserver,
	}

	for _, role := range validRoles {
		assert.True(t, stakeholder.IsValidRole(role))
	}

	assert.False(t, stakeholder.IsValidRole("invalid_role"))
}

func TestStakeholder_IsValidType(t *testing.T) {
	stakeholder := &entities.Stakeholder{}

	validTypes := []entities.StakeholderType{
		entities.StakeholderTypeInternal,
		entities.StakeholderTypeExternal,
		entities.StakeholderTypeIndustry,
		entities.StakeholderTypeAcademic,
	}

	for _, stakeholderType := range validTypes {
		assert.True(t, stakeholder.IsValidType(stakeholderType))
	}

	assert.False(t, stakeholder.IsValidType("invalid_type"))
}

func TestStakeholder_IsValidStatus(t *testing.T) {
	stakeholder := &entities.Stakeholder{}

	validStatuses := []entities.StakeholderStatus{
		entities.StakeholderStatusActive,
		entities.StakeholderStatusInactive,
		entities.StakeholderStatusPending,
		entities.StakeholderStatusBlocked,
	}

	for _, status := range validStatuses {
		assert.True(t, stakeholder.IsValidStatus(status))
	}

	assert.False(t, stakeholder.IsValidStatus("invalid_status"))
}

func TestStakeholder_CanPerformAction(t *testing.T) {
	stakeholder := &entities.Stakeholder{
		Status:      entities.StakeholderStatusActive,
		CanEvaluate: true,
		CanReview:   true,
		CanApprove:  false,
	}

	assert.True(t, stakeholder.CanPerformAction("evaluate"))
	assert.True(t, stakeholder.CanPerformAction("review"))
	assert.False(t, stakeholder.CanPerformAction("approve"))
	assert.False(t, stakeholder.CanPerformAction("invalid_action"))

	// Test inactive stakeholder
	stakeholder.Status = entities.StakeholderStatusInactive
	assert.False(t, stakeholder.CanPerformAction("evaluate"))
	assert.False(t, stakeholder.CanPerformAction("review"))
}

func TestStakeholder_UpdateLastActive(t *testing.T) {
	stakeholder := &entities.Stakeholder{}
	originalLastActive := stakeholder.LastActiveAt

	stakeholder.UpdateLastActive()

	assert.NotEqual(t, originalLastActive, stakeholder.LastActiveAt)
	assert.NotNil(t, stakeholder.LastActiveAt)
	assert.True(t, time.Since(*stakeholder.LastActiveAt) < time.Second)
}

func TestStakeholder_Activate(t *testing.T) {
	t.Run("Activate pending stakeholder", func(t *testing.T) {
		stakeholder := &entities.Stakeholder{
			Status: entities.StakeholderStatusPending,
		}

		err := stakeholder.Activate()
		assert.NoError(t, err)
		assert.Equal(t, entities.StakeholderStatusActive, stakeholder.Status)
	})

	t.Run("Cannot activate blocked stakeholder", func(t *testing.T) {
		stakeholder := &entities.Stakeholder{
			Status: entities.StakeholderStatusBlocked,
		}

		err := stakeholder.Activate()
		assert.Error(t, err)
		assert.Contains(t, err.Error(), "cannot activate blocked stakeholder")
		assert.Equal(t, entities.StakeholderStatusBlocked, stakeholder.Status)
	})
}

func TestStakeholder_Deactivate(t *testing.T) {
	stakeholder := &entities.Stakeholder{
		Status: entities.StakeholderStatusActive,
	}

	stakeholder.Deactivate()
	assert.Equal(t, entities.StakeholderStatusInactive, stakeholder.Status)
}

func TestStakeholder_Block(t *testing.T) {
	stakeholder := &entities.Stakeholder{
		Status: entities.StakeholderStatusActive,
	}

	reason := "Inappropriate behavior"
	stakeholder.Block(reason)

	assert.Equal(t, entities.StakeholderStatusBlocked, stakeholder.Status)
	assert.Equal(t, reason, stakeholder.Notes)
}

func TestStakeholder_HasHighAccessLevel(t *testing.T) {
	stakeholder := &entities.Stakeholder{}

	stakeholder.AccessLevel = 3
	assert.False(t, stakeholder.HasHighAccessLevel())

	stakeholder.AccessLevel = 4
	assert.True(t, stakeholder.HasHighAccessLevel())

	stakeholder.AccessLevel = 5
	assert.True(t, stakeholder.HasHighAccessLevel())
}

func TestStakeholder_RoleCheckers(t *testing.T) {
	stakeholder := &entities.Stakeholder{}

	stakeholder.Role = entities.StakeholderRoleCoordinator
	assert.True(t, stakeholder.IsCoordinator())
	assert.False(t, stakeholder.IsJuror())

	stakeholder.Role = entities.StakeholderRoleJuror
	assert.False(t, stakeholder.IsCoordinator())
	assert.True(t, stakeholder.IsJuror())
}

func TestStakeholder_IsExternal(t *testing.T) {
	stakeholder := &entities.Stakeholder{}

	stakeholder.Type = entities.StakeholderTypeInternal
	assert.False(t, stakeholder.IsExternal())

	stakeholder.Type = entities.StakeholderTypeExternal
	assert.True(t, stakeholder.IsExternal())

	stakeholder.Type = entities.StakeholderTypeIndustry
	assert.True(t, stakeholder.IsExternal())

	stakeholder.Type = entities.StakeholderTypeAcademic
	assert.False(t, stakeholder.IsExternal())
}
