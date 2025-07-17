package usecases

import (
	"context"
	"errors"
	"testing"

	"userservice/internal/application/dtos"
	"userservice/internal/domain/entities"
	"userservice/internal/domain/repositories"
	"userservice/tests/fixtures"
	"userservice/tests/mocks"

	"github.com/go-playground/validator/v10"
	"github.com/stretchr/testify/assert"
	"github.com/stretchr/testify/mock"
)

func TestBulkUserUseCases_BulkCreateUsers(t *testing.T) {
	// Setup
	mockRepo := new(mocks.MockUserRepository)
	validate := validator.New()
	useCase := NewBulkUserUseCases(mockRepo, validate)
	ctx := context.Background()

	t.Run("successful bulk user creation", func(t *testing.T) {
		// Arrange
		request := fixtures.NewBulkCreateUserRequest()

		// Mock expectations - check existing users
		for _, userReq := range request.Users {
			mockRepo.On("GetByEmail", ctx, userReq.Email).Return(nil, nil).Once()
			mockRepo.On("GetByDocumento", ctx, userReq.Documento).Return(nil, nil).Once()
		}

		// Mock bulk create
		mockRepo.On("BulkCreate", ctx, mock.AnythingOfType("[]*entities.User")).Return(nil).Once()

		// Act
		result, err := useCase.BulkCreateUsers(ctx, request)

		// Assert
		assert.NoError(t, err)
		assert.NotNil(t, result)
		assert.Equal(t, len(request.Users), result.TotalProcessed)
		assert.Equal(t, len(request.Users), result.SuccessCount)
		assert.Equal(t, 0, result.FailureCount)
		assert.Len(t, result.Results, len(request.Users))

		for _, res := range result.Results {
			assert.True(t, res.Success)
			assert.NotNil(t, res.UserID)
		}

		mockRepo.AssertExpectations(t)
	})

	t.Run("bulk creation with duplicate email", func(t *testing.T) {
		// Arrange
		request := fixtures.NewBulkCreateUserRequest()
		existingUser := fixtures.NewValidUser()

		// Mock expectations - first user exists, second doesn't
		mockRepo.On("GetByEmail", ctx, request.Users[0].Email).Return(existingUser, nil).Once()
		mockRepo.On("GetByEmail", ctx, request.Users[1].Email).Return(nil, nil).Once()
		mockRepo.On("GetByDocumento", ctx, request.Users[1].Documento).Return(nil, nil).Once()

		// Mock bulk create for the valid user
		mockRepo.On("BulkCreate", ctx, mock.AnythingOfType("[]*entities.User")).Return(nil).Once()

		// Act
		result, err := useCase.BulkCreateUsers(ctx, request)

		// Assert
		assert.NoError(t, err)
		assert.NotNil(t, result)
		assert.Equal(t, len(request.Users), result.TotalProcessed)
		assert.Equal(t, 1, result.SuccessCount)
		assert.Equal(t, 1, result.FailureCount)

		// Check specific results
		failedResult := result.Results[0]
		assert.False(t, failedResult.Success)
		assert.Contains(t, failedResult.Message, "already exists")

		successResult := result.Results[1]
		assert.True(t, successResult.Success)
		assert.NotNil(t, successResult.UserID)

		mockRepo.AssertExpectations(t)
	})

	t.Run("bulk creation fails when repository fails", func(t *testing.T) {
		// Arrange
		request := fixtures.NewBulkCreateUserRequest()
		repoError := errors.New("database connection error")

		// Mock expectations - all users are valid
		for _, userReq := range request.Users {
			mockRepo.On("GetByEmail", ctx, userReq.Email).Return(nil, nil).Once()
			mockRepo.On("GetByDocumento", ctx, userReq.Documento).Return(nil, nil).Once()
		}

		// Mock bulk create failure
		mockRepo.On("BulkCreate", ctx, mock.AnythingOfType("[]*entities.User")).Return(repoError).Once()

		// Act
		result, err := useCase.BulkCreateUsers(ctx, request)

		// Assert
		assert.NoError(t, err)
		assert.NotNil(t, result)
		assert.Equal(t, len(request.Users), result.TotalProcessed)
		assert.Equal(t, 0, result.SuccessCount)
		assert.Equal(t, len(request.Users), result.FailureCount)

		for _, res := range result.Results {
			assert.False(t, res.Success)
			assert.Contains(t, res.Message, "bulk creation failed")
		}

		mockRepo.AssertExpectations(t)
	})

	t.Run("invalid request validation", func(t *testing.T) {
		// Arrange
		request := &dtos.BulkCreateUserRequest{
			Users: []dtos.CreateUserRequest{}, // Empty users array
		}

		// Act
		result, err := useCase.BulkCreateUsers(ctx, request)

		// Assert
		assert.Error(t, err)
		assert.Nil(t, result)
		assert.Contains(t, err.Error(), "validation error")

		// No repository calls should be made
		mockRepo.AssertExpectations(t)
	})
}

func TestBulkUserUseCases_BulkUpdateUsers(t *testing.T) {
	// Setup
	mockRepo := new(mocks.MockUserRepository)
	validate := validator.New()
	useCase := NewBulkUserUseCases(mockRepo, validate)
	ctx := context.Background()

	t.Run("successful bulk user update", func(t *testing.T) {
		// Arrange
		request := fixtures.NewBulkUpdateUserRequest()
		existingUsers := []*entities.User{
			fixtures.NewValidUser(),
			fixtures.NewValidUser(),
		}
		existingUsers[0].Email = request.Users[0].Email
		existingUsers[1].Email = request.Users[1].Email

		bulkResult := &repositories.BulkOperationResult{
			Total:   len(request.Users),
			Success: len(request.Users),
			Failed:  0,
			Errors:  []repositories.BulkOperationError{},
		}

		// Mock expectations
		for i, updateReq := range request.Users {
			mockRepo.On("GetByEmail", ctx, updateReq.Email).Return(existingUsers[i], nil).Once()
		}
		mockRepo.On("BulkUpdate", ctx, mock.AnythingOfType("map[string]*entities.User")).Return(bulkResult, nil).Once()

		// Act
		result, err := useCase.BulkUpdateUsers(ctx, request)

		// Assert
		assert.NoError(t, err)
		assert.NotNil(t, result)
		assert.Equal(t, len(request.Users), result.TotalProcessed)
		assert.Equal(t, len(request.Users), result.SuccessCount)
		assert.Equal(t, 0, result.FailureCount)

		mockRepo.AssertExpectations(t)
	})

	t.Run("bulk update with non-existent user", func(t *testing.T) {
		// Arrange
		request := fixtures.NewBulkUpdateUserRequest()
		existingUser := fixtures.NewValidUser()
		existingUser.Email = request.Users[0].Email

		// Mock expectations - first user exists, second doesn't
		mockRepo.On("GetByEmail", ctx, request.Users[0].Email).Return(existingUser, nil).Once()
		mockRepo.On("GetByEmail", ctx, request.Users[1].Email).Return(nil, nil).Once()

		bulkResult := &repositories.BulkOperationResult{
			Total:   1,
			Success: 1,
			Failed:  0,
			Errors:  []repositories.BulkOperationError{},
		}
		mockRepo.On("BulkUpdate", ctx, mock.AnythingOfType("map[string]*entities.User")).Return(bulkResult, nil).Once()

		// Act
		result, err := useCase.BulkUpdateUsers(ctx, request)

		// Assert
		assert.NoError(t, err)
		assert.NotNil(t, result)
		assert.Equal(t, len(request.Users), result.TotalProcessed)
		assert.Equal(t, 1, result.SuccessCount)
		assert.Equal(t, 1, result.FailureCount)

		mockRepo.AssertExpectations(t)
	})
}

func TestBulkUserUseCases_BulkDeleteUsers(t *testing.T) {
	// Setup
	mockRepo := new(mocks.MockUserRepository)
	validate := validator.New()
	useCase := NewBulkUserUseCases(mockRepo, validate)
	ctx := context.Background()

	t.Run("successful bulk user deletion", func(t *testing.T) {
		// Arrange
		request := fixtures.NewBulkDeleteRequest()
		bulkResult := &repositories.BulkOperationResult{
			Total:   len(request.Emails),
			Success: len(request.Emails),
			Failed:  0,
			Errors:  []repositories.BulkOperationError{},
		}

		// Mock expectations
		mockRepo.On("BulkDelete", ctx, request.Emails).Return(bulkResult, nil).Once()

		// Act
		result, err := useCase.BulkDeleteUsers(ctx, request)

		// Assert
		assert.NoError(t, err)
		assert.NotNil(t, result)
		assert.Equal(t, len(request.Emails), result.TotalProcessed)
		assert.Equal(t, len(request.Emails), result.SuccessCount)
		assert.Equal(t, 0, result.FailureCount)

		for _, res := range result.Results {
			assert.True(t, res.Success)
			assert.Contains(t, res.Message, "deleted successfully")
		}

		mockRepo.AssertExpectations(t)
	})

	t.Run("bulk deletion with repository errors", func(t *testing.T) {
		// Arrange
		request := fixtures.NewBulkDeleteRequest()
		bulkResult := &repositories.BulkOperationResult{
			Total:   len(request.Emails),
			Success: 1,
			Failed:  1,
			Errors: []repositories.BulkOperationError{
				{
					User:  request.Emails[1],
					Error: "user not found",
				},
			},
		}

		// Mock expectations
		mockRepo.On("BulkDelete", ctx, request.Emails).Return(bulkResult, nil).Once()

		// Act
		result, err := useCase.BulkDeleteUsers(ctx, request)

		// Assert
		assert.NoError(t, err)
		assert.NotNil(t, result)
		assert.Equal(t, len(request.Emails), result.TotalProcessed)
		assert.Equal(t, 1, result.SuccessCount)
		assert.Equal(t, 1, result.FailureCount)

		mockRepo.AssertExpectations(t)
	})
}

func TestBulkUserUseCases_BulkChangeStatus(t *testing.T) {
	// Setup
	mockRepo := new(mocks.MockUserRepository)
	validate := validator.New()
	useCase := NewBulkUserUseCases(mockRepo, validate)
	ctx := context.Background()

	t.Run("successful bulk status change", func(t *testing.T) {
		// Arrange
		request := fixtures.NewBulkStatusRequest(false) // Deactivate users
		bulkResult := &repositories.BulkOperationResult{
			Total:   len(request.Emails),
			Success: len(request.Emails),
			Failed:  0,
			Errors:  []repositories.BulkOperationError{},
		}

		// Mock expectations
		mockRepo.On("BulkStatusChange", ctx, request.Emails, request.IsActive).Return(bulkResult, nil).Once()

		// Act
		result, err := useCase.BulkChangeStatus(ctx, request)

		// Assert
		assert.NoError(t, err)
		assert.NotNil(t, result)
		assert.Equal(t, len(request.Emails), result.TotalProcessed)
		assert.Equal(t, len(request.Emails), result.SuccessCount)
		assert.Equal(t, 0, result.FailureCount)

		for _, res := range result.Results {
			assert.True(t, res.Success)
			assert.Contains(t, res.Message, "deactivated successfully")
		}

		mockRepo.AssertExpectations(t)
	})

	t.Run("bulk status change activation", func(t *testing.T) {
		// Arrange
		request := fixtures.NewBulkStatusRequest(true) // Activate users
		bulkResult := &repositories.BulkOperationResult{
			Total:   len(request.Emails),
			Success: len(request.Emails),
			Failed:  0,
			Errors:  []repositories.BulkOperationError{},
		}

		// Mock expectations
		mockRepo.On("BulkStatusChange", ctx, request.Emails, request.IsActive).Return(bulkResult, nil).Once()

		// Act
		result, err := useCase.BulkChangeStatus(ctx, request)

		// Assert
		assert.NoError(t, err)
		assert.NotNil(t, result)
		assert.Equal(t, len(request.Emails), result.TotalProcessed)
		assert.Equal(t, len(request.Emails), result.SuccessCount)
		assert.Equal(t, 0, result.FailureCount)

		for _, res := range result.Results {
			assert.True(t, res.Success)
			assert.Contains(t, res.Message, "activated successfully")
		}

		mockRepo.AssertExpectations(t)
	})
}
