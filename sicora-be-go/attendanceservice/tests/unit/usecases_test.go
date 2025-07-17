package unit

import (
	"errors"
	"testing"
	"time"

	"attendanceservice/internal/application/dtos"
	"attendanceservice/internal/application/usecases"
	"attendanceservice/internal/domain/entities"
	"attendanceservice/tests/mocks"

	"github.com/google/uuid"
	"github.com/stretchr/testify/assert"
	"github.com/stretchr/testify/mock"
)

func TestAttendanceUseCase_CreateAttendance(t *testing.T) {
	mockRepo := new(mocks.MockAttendanceRepository)
	mockAlertRepo := new(mocks.MockAttendanceAlertRepository)
	useCase := usecases.NewAttendanceUseCase(mockRepo, mockAlertRepo)

	tests := []struct {
		name          string
		request       *dtos.CreateAttendanceRequest
		mockSetup     func()
		expectError   bool
		expectedError string
	}{
		{
			name: "Successful attendance creation",
			request: &dtos.CreateAttendanceRequest{
				UserID:  uuid.New(),
				ClassID: uuid.New(),
				InTime:  time.Now(),
				Status:  "present",
			},
			mockSetup: func() {
				mockRepo.On("Create", mock.AnythingOfType("*entities.AttendanceRecord")).Return(nil).Once()
			},
			expectError: false,
		},
		{
			name: "Repository error",
			request: &dtos.CreateAttendanceRequest{
				UserID:  uuid.New(),
				ClassID: uuid.New(),
				InTime:  time.Now(),
				Status:  "present",
			},
			mockSetup: func() {
				mockRepo.On("Create", mock.AnythingOfType("*entities.AttendanceRecord")).Return(errors.New("database error")).Once()
			},
			expectError:   true,
			expectedError: "database error",
		},
	}

	for _, tt := range tests {
		t.Run(tt.name, func(t *testing.T) {
			mockRepo.ExpectedCalls = nil
			mockAlertRepo.ExpectedCalls = nil

			tt.mockSetup()

			response, err := useCase.CreateAttendance(tt.request)

			if tt.expectError {
				assert.Error(t, err)
				assert.Contains(t, err.Error(), tt.expectedError)
				assert.Nil(t, response)
			} else {
				assert.NoError(t, err)
				assert.NotNil(t, response)
				assert.Equal(t, tt.request.UserID, response.UserID)
				assert.Equal(t, tt.request.Status, response.Status)
			}

			mockRepo.AssertExpectations(t)
			mockAlertRepo.AssertExpectations(t)
		})
	}
}

func TestAttendanceUseCase_GetAttendanceByID(t *testing.T) {
	mockRepo := new(mocks.MockAttendanceRepository)
	mockAlertRepo := new(mocks.MockAttendanceAlertRepository)
	useCase := usecases.NewAttendanceUseCase(mockRepo, mockAlertRepo)

	attendanceID := uuid.New()
	attendance := &entities.AttendanceRecord{
		ID:      attendanceID,
		UserID:  uuid.New(),
		ClassID: uuid.New(),
		Status:  "present",
		InTime:  time.Now(),
	}

	tests := []struct {
		name        string
		id          uuid.UUID
		mockSetup   func()
		expectError bool
	}{
		{
			name: "Successful retrieval",
			id:   attendanceID,
			mockSetup: func() {
				mockRepo.On("GetByID", attendanceID).Return(attendance, nil).Once()
			},
			expectError: false,
		},
		{
			name: "Not found",
			id:   attendanceID,
			mockSetup: func() {
				mockRepo.On("GetByID", attendanceID).Return(nil, errors.New("not found")).Once()
			},
			expectError: true,
		},
	}

	for _, tt := range tests {
		t.Run(tt.name, func(t *testing.T) {
			mockRepo.ExpectedCalls = nil
			mockAlertRepo.ExpectedCalls = nil

			tt.mockSetup()

			response, err := useCase.GetAttendanceByID(tt.id)

			if tt.expectError {
				assert.Error(t, err)
				assert.Nil(t, response)
			} else {
				assert.NoError(t, err)
				assert.NotNil(t, response)
				assert.Equal(t, attendanceID, response.ID)
			}

			mockRepo.AssertExpectations(t)
		})
	}
}
