package usecases

import (
	"context"
	"errors"
	"log"
	"os"
	"testing"

	"userservice/tests/fixtures"
	"userservice/tests/mocks"

	"github.com/google/uuid"
	"github.com/stretchr/testify/assert"
	"github.com/stretchr/testify/mock"
)

func TestCreateUserUseCase_Execute(t *testing.T) {
	// Setup
	mockRepo := new(mocks.MockUserRepository)
	logger := log.New(os.Stdout, "", log.LstdFlags)
	useCase := NewCreateUserUseCase(mockRepo, logger)
	ctx := context.Background()

	t.Run("successful user creation", func(t *testing.T) {
		// Arrange
		request := fixtures.NewCreateUserRequest()

		// Mock expectations
		mockRepo.On("GetByEmail", ctx, request.Email).Return(nil, nil).Once()
		mockRepo.On("GetByDocumento", ctx, request.Documento).Return(nil, nil).Once()
		mockRepo.On("Create", ctx, mock.AnythingOfType("*entities.User")).Return(nil).Once()

		// Act
		result, err := useCase.Execute(ctx, request)

		// Assert
		assert.NoError(t, err)
		assert.NotNil(t, result)
		assert.Equal(t, request.Email, result.Email)
		assert.Equal(t, request.Nombre, result.Nombre)
		assert.Equal(t, request.Apellido, result.Apellido)
		assert.True(t, result.IsActive)
		mockRepo.AssertExpectations(t)
	})

	t.Run("user creation fails when email already exists", func(t *testing.T) {
		// Arrange
		request := fixtures.NewCreateUserRequest()
		existingUser := fixtures.NewValidUser()

		// Mock expectations
		mockRepo.On("GetByEmail", ctx, request.Email).Return(existingUser, nil).Once()

		// Act
		result, err := useCase.Execute(ctx, request)

		// Assert
		assert.Error(t, err)
		assert.Nil(t, result)
		assert.Contains(t, err.Error(), "email already exists")
		mockRepo.AssertExpectations(t)
	})

	t.Run("user creation fails when documento already exists", func(t *testing.T) {
		// Arrange
		request := fixtures.NewCreateUserRequest()
		existingUser := fixtures.NewValidUser()

		// Mock expectations
		mockRepo.On("GetByEmail", ctx, request.Email).Return(nil, nil).Once()
		mockRepo.On("GetByDocumento", ctx, request.Documento).Return(existingUser, nil).Once()

		// Act
		result, err := useCase.Execute(ctx, request)

		// Assert
		assert.Error(t, err)
		assert.Nil(t, result)
		assert.Contains(t, err.Error(), "documento already exists")
		mockRepo.AssertExpectations(t)
	})

	t.Run("user creation fails when repository create fails", func(t *testing.T) {
		// Arrange
		request := fixtures.NewCreateUserRequest()
		repoError := errors.New("database connection error")

		// Mock expectations
		mockRepo.On("GetByEmail", ctx, request.Email).Return(nil, nil).Once()
		mockRepo.On("GetByDocumento", ctx, request.Documento).Return(nil, nil).Once()
		mockRepo.On("Create", ctx, mock.AnythingOfType("*entities.User")).Return(repoError).Once()

		// Act
		result, err := useCase.Execute(ctx, request)

		// Assert
		assert.Error(t, err)
		assert.Nil(t, result)
		assert.Contains(t, err.Error(), "database connection error")
		mockRepo.AssertExpectations(t)
	})
}

func TestGetUserUseCase_Execute(t *testing.T) {
	// Setup
	mockRepo := new(mocks.MockUserRepository)
	logger := log.New(os.Stdout, "", log.LstdFlags)
	useCase := NewGetUserUseCase(mockRepo, logger)
	ctx := context.Background()

	t.Run("successful user retrieval", func(t *testing.T) {
		// Arrange
		userID := uuid.New()
		expectedUser := fixtures.NewValidUser()
		expectedUser.ID = userID

		// Mock expectations
		mockRepo.On("GetByID", ctx, userID).Return(expectedUser, nil).Once()

		// Act
		result, err := useCase.Execute(ctx, userID)

		// Assert
		assert.NoError(t, err)
		assert.NotNil(t, result)
		assert.Equal(t, expectedUser.ID, result.ID)
		assert.Equal(t, expectedUser.Email, result.Email)
		assert.Equal(t, expectedUser.Nombre, result.Nombre)
		mockRepo.AssertExpectations(t)
	})

	t.Run("user not found", func(t *testing.T) {
		// Arrange
		userID := uuid.New()

		// Mock expectations
		mockRepo.On("GetByID", ctx, userID).Return(nil, nil).Once()

		// Act
		result, err := useCase.Execute(ctx, userID)

		// Assert
		assert.Error(t, err)
		assert.Nil(t, result)
		assert.Contains(t, err.Error(), "user not found")
		mockRepo.AssertExpectations(t)
	})

	t.Run("repository error", func(t *testing.T) {
		// Arrange
		userID := uuid.New()
		repoError := errors.New("database connection error")

		// Mock expectations
		mockRepo.On("GetByID", ctx, userID).Return(nil, repoError).Once()

		// Act
		result, err := useCase.Execute(ctx, userID)

		// Assert
		assert.Error(t, err)
		assert.Nil(t, result)
		assert.Contains(t, err.Error(), "database connection error")
		mockRepo.AssertExpectations(t)
	})
}
