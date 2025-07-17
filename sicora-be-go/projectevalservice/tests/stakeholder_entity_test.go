package tests

import (
	"testing"

	"projectevalservice/internal/domain/entities"

	"github.com/stretchr/testify/assert"
)

func TestStakeholderRoleValidation(t *testing.T) {
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

func TestStakeholderTypeValidation(t *testing.T) {
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

func TestStakeholderStatusValidation(t *testing.T) {
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

func TestStakeholderCanPerformAction(t *testing.T) {
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

	stakeholder.Status = entities.StakeholderStatusInactive
	assert.False(t, stakeholder.CanPerformAction("evaluate"))
	assert.False(t, stakeholder.CanPerformAction("review"))
}

func TestStakeholderActivation(t *testing.T) {
	stakeholder := &entities.Stakeholder{
		Status: entities.StakeholderStatusPending,
	}

	err := stakeholder.Activate()
	assert.NoError(t, err)
	assert.Equal(t, entities.StakeholderStatusActive, stakeholder.Status)

	stakeholder.Status = entities.StakeholderStatusBlocked
	err = stakeholder.Activate()
	assert.Error(t, err)
	assert.Contains(t, err.Error(), "cannot activate blocked stakeholder")
}

func TestStakeholderRoleCheckers(t *testing.T) {
	stakeholder := &entities.Stakeholder{}

	stakeholder.Role = entities.StakeholderRoleCoordinator
	assert.True(t, stakeholder.IsCoordinator())
	assert.False(t, stakeholder.IsJuror())

	stakeholder.Role = entities.StakeholderRoleJuror
	assert.False(t, stakeholder.IsCoordinator())
	assert.True(t, stakeholder.IsJuror())
}

func TestStakeholderIsExternal(t *testing.T) {
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
