package mocks

import (
	"context"

	"userservice/internal/domain/entities"
	"userservice/internal/domain/repositories"

	"github.com/google/uuid"
	"github.com/stretchr/testify/mock"
)

// MockUserRepository es un mock del UserRepository para testing
type MockUserRepository struct {
	mock.Mock
}

// Create mock implementation
func (m *MockUserRepository) Create(ctx context.Context, user *entities.User) error {
	args := m.Called(ctx, user)
	return args.Error(0)
}

// GetByID mock implementation
func (m *MockUserRepository) GetByID(ctx context.Context, id uuid.UUID) (*entities.User, error) {
	args := m.Called(ctx, id)
	if args.Get(0) == nil {
		return nil, args.Error(1)
	}
	return args.Get(0).(*entities.User), args.Error(1)
}

// GetByEmail mock implementation
func (m *MockUserRepository) GetByEmail(ctx context.Context, email string) (*entities.User, error) {
	args := m.Called(ctx, email)
	if args.Get(0) == nil {
		return nil, args.Error(1)
	}
	return args.Get(0).(*entities.User), args.Error(1)
}

// GetByDocumento mock implementation
func (m *MockUserRepository) GetByDocumento(ctx context.Context, documento string) (*entities.User, error) {
	args := m.Called(ctx, documento)
	if args.Get(0) == nil {
		return nil, args.Error(1)
	}
	return args.Get(0).(*entities.User), args.Error(1)
}

// Update mock implementation
func (m *MockUserRepository) Update(ctx context.Context, user *entities.User) error {
	args := m.Called(ctx, user)
	return args.Error(0)
}

// Delete mock implementation
func (m *MockUserRepository) Delete(ctx context.Context, id uuid.UUID) error {
	args := m.Called(ctx, id)
	return args.Error(0)
}

// List mock implementation
func (m *MockUserRepository) List(ctx context.Context, filters repositories.UserFilters) (*repositories.PaginatedUsers, error) {
	args := m.Called(ctx, filters)
	if args.Get(0) == nil {
		return nil, args.Error(1)
	}
	return args.Get(0).(*repositories.PaginatedUsers), args.Error(1)
}

// GetByFicha mock implementation
func (m *MockUserRepository) GetByFicha(ctx context.Context, fichaID string) ([]*entities.User, error) {
	args := m.Called(ctx, fichaID)
	if args.Get(0) == nil {
		return nil, args.Error(1)
	}
	return args.Get(0).([]*entities.User), args.Error(1)
}

// ExistsByEmail mock implementation
func (m *MockUserRepository) ExistsByEmail(ctx context.Context, email string) (bool, error) {
	args := m.Called(ctx, email)
	return args.Bool(0), args.Error(1)
}

// ExistsByDocumento mock implementation
func (m *MockUserRepository) ExistsByDocumento(ctx context.Context, documento string) (bool, error) {
	args := m.Called(ctx, documento)
	return args.Bool(0), args.Error(1)
}

// BulkCreate mock implementation
func (m *MockUserRepository) BulkCreate(ctx context.Context, users []*entities.User) error {
	args := m.Called(ctx, users)
	return args.Error(0)
}

// BulkUpdate mock implementation
func (m *MockUserRepository) BulkUpdate(ctx context.Context, updates map[string]*entities.User) (*repositories.BulkOperationResult, error) {
	args := m.Called(ctx, updates)
	if args.Get(0) == nil {
		return nil, args.Error(1)
	}
	return args.Get(0).(*repositories.BulkOperationResult), args.Error(1)
}

// BulkDelete mock implementation
func (m *MockUserRepository) BulkDelete(ctx context.Context, emails []string) (*repositories.BulkOperationResult, error) {
	args := m.Called(ctx, emails)
	if args.Get(0) == nil {
		return nil, args.Error(1)
	}
	return args.Get(0).(*repositories.BulkOperationResult), args.Error(1)
}

// BulkStatusChange mock implementation
func (m *MockUserRepository) BulkStatusChange(ctx context.Context, emails []string, isActive bool) (*repositories.BulkOperationResult, error) {
	args := m.Called(ctx, emails)
	if args.Get(0) == nil {
		return nil, args.Error(1)
	}
	return args.Get(0).(*repositories.BulkOperationResult), args.Error(1)
}

// GetMultipleByEmails mock implementation
func (m *MockUserRepository) GetMultipleByEmails(ctx context.Context, emails []string) ([]*entities.User, error) {
	args := m.Called(ctx, emails)
	if args.Get(0) == nil {
		return nil, args.Error(1)
	}
	return args.Get(0).([]*entities.User), args.Error(1)
}

// GetActiveInstructors mock implementation
func (m *MockUserRepository) GetActiveInstructors(ctx context.Context) ([]*entities.User, error) {
	args := m.Called(ctx)
	if args.Get(0) == nil {
		return nil, args.Error(1)
	}
	return args.Get(0).([]*entities.User), args.Error(1)
}

// GetInactiveUsers mock implementation
func (m *MockUserRepository) GetInactiveUsers(ctx context.Context, daysInactive int) ([]*entities.User, error) {
	args := m.Called(ctx, daysInactive)
	if args.Get(0) == nil {
		return nil, args.Error(1)
	}
	return args.Get(0).([]*entities.User), args.Error(1)
}
