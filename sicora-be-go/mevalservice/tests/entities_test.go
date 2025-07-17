package tests

import (
	"testing"
	"time"

	"github.com/stretchr/testify/assert"

	"mevalservice/internal/domain/entities"
)

func TestCommitteeCreation(t *testing.T) {
	committee := &entities.Committee{
		CommitteeDate: time.Now(),
		CommitteeType: entities.CommitteeTypeMonthly,
		Status:        entities.CommitteeStatusScheduled,
		CreatedAt:     time.Now(),
		UpdatedAt:     time.Now(),
	}

	assert.NotNil(t, committee)
	assert.Equal(t, entities.CommitteeTypeMonthly, committee.CommitteeType)
	assert.Equal(t, entities.CommitteeStatusScheduled, committee.Status)
	assert.False(t, committee.AgendaGenerated)
	assert.False(t, committee.QuorumAchieved)
}

func TestStudentCaseCreation(t *testing.T) {
	studentCase := &entities.StudentCase{
		CaseType:   entities.CaseTypeImprovementPlan,
		CaseStatus: entities.CaseStatusPending,
		CreatedAt:  time.Now(),
		UpdatedAt:  time.Now(),
	}

	assert.NotNil(t, studentCase)
	assert.Equal(t, entities.CaseTypeImprovementPlan, studentCase.CaseType)
	assert.Equal(t, entities.CaseStatusPending, studentCase.CaseStatus)
}
