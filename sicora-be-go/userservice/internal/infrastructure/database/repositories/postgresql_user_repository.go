package repositories

import (
	"context"
	"fmt"
	"time"

	"userservice/internal/domain/entities"
	"userservice/internal/domain/repositories"
	"userservice/internal/infrastructure/database/models"

	"github.com/google/uuid"
	"gorm.io/gorm"
)

// PostgreSQLUserRepository implements UserRepository interface for PostgreSQL
type PostgreSQLUserRepository struct {
	db *gorm.DB
}

// NewPostgreSQLUserRepository creates a new PostgreSQL user repository
func NewPostgreSQLUserRepository(db *gorm.DB) repositories.UserRepository {
	return &PostgreSQLUserRepository{
		db: db,
	}
}

// Create creates a new user in the database
func (r *PostgreSQLUserRepository) Create(ctx context.Context, user *entities.User) error {
	model := models.NewUserModelFromEntity(user)

	if err := r.db.WithContext(ctx).Create(model).Error; err != nil {
		return fmt.Errorf("failed to create user: %w", err)
	}

	// Update entity with generated timestamps and ID
	entity, err := model.ToEntity()
	if err != nil {
		return fmt.Errorf("failed to convert model to entity: %w", err)
	}

	*user = *entity
	return nil
}

// GetByID retrieves a user by ID
func (r *PostgreSQLUserRepository) GetByID(ctx context.Context, id uuid.UUID) (*entities.User, error) {
	var model models.UserModel

	if err := r.db.WithContext(ctx).Where("id = ?", id).First(&model).Error; err != nil {
		if err == gorm.ErrRecordNotFound {
			return nil, nil
		}
		return nil, fmt.Errorf("failed to get user by ID: %w", err)
	}

	return model.ToEntity()
}

// GetByEmail retrieves a user by email
func (r *PostgreSQLUserRepository) GetByEmail(ctx context.Context, email string) (*entities.User, error) {
	var model models.UserModel

	if err := r.db.WithContext(ctx).Where("email = ?", email).First(&model).Error; err != nil {
		if err == gorm.ErrRecordNotFound {
			return nil, nil
		}
		return nil, fmt.Errorf("failed to get user by email: %w", err)
	}

	return model.ToEntity()
}

// GetByDocumento retrieves a user by document number
func (r *PostgreSQLUserRepository) GetByDocumento(ctx context.Context, documento string) (*entities.User, error) {
	var model models.UserModel

	if err := r.db.WithContext(ctx).Where("documento = ?", documento).First(&model).Error; err != nil {
		if err == gorm.ErrRecordNotFound {
			return nil, nil
		}
		return nil, fmt.Errorf("failed to get user by documento: %w", err)
	}

	return model.ToEntity()
}

// Update updates an existing user
func (r *PostgreSQLUserRepository) Update(ctx context.Context, user *entities.User) error {
	model := models.NewUserModelFromEntity(user)

	if err := r.db.WithContext(ctx).Save(model).Error; err != nil {
		return fmt.Errorf("failed to update user: %w", err)
	}

	// Update entity with new timestamps
	entity, err := model.ToEntity()
	if err != nil {
		return fmt.Errorf("failed to convert model to entity: %w", err)
	}

	*user = *entity
	return nil
}

// Delete soft deletes a user
func (r *PostgreSQLUserRepository) Delete(ctx context.Context, id uuid.UUID) error {
	if err := r.db.WithContext(ctx).Where("id = ?", id).Delete(&models.UserModel{}).Error; err != nil {
		return fmt.Errorf("failed to delete user: %w", err)
	}
	return nil
}

// List retrieves users with filters and pagination
func (r *PostgreSQLUserRepository) List(ctx context.Context, filters repositories.UserFilters) (*repositories.PaginatedUsers, error) {
	var userModels []models.UserModel
	query := r.db.WithContext(ctx)

	// Apply filters
	if filters.Rol != nil {
		query = query.Where("rol = ?", string(*filters.Rol))
	}

	if filters.IsActive != nil {
		query = query.Where("is_active = ?", *filters.IsActive)
	}

	if filters.FichaID != nil {
		query = query.Where("ficha_id = ?", *filters.FichaID)
	}

	if filters.Programa != nil {
		query = query.Where("programa_formacion = ?", *filters.Programa)
	}

	if filters.Search != nil && *filters.Search != "" {
		searchPattern := "%" + *filters.Search + "%"
		query = query.Where(
			"LOWER(nombre) LIKE LOWER(?) OR LOWER(apellido) LIKE LOWER(?) OR LOWER(email) LIKE LOWER(?) OR documento LIKE ?",
			searchPattern, searchPattern, searchPattern, searchPattern,
		)
	}

	// Count total before pagination
	var total int64
	if err := query.Model(&models.UserModel{}).Count(&total).Error; err != nil {
		return nil, fmt.Errorf("failed to count users: %w", err)
	}

	// Apply ordering
	sortBy := "created_at"
	sortDirection := "DESC"

	if filters.SortBy != "" {
		sortBy = filters.SortBy
	}

	if filters.SortDirection == "asc" {
		sortDirection = "ASC"
	}

	query = query.Order(fmt.Sprintf("%s %s", sortBy, sortDirection))

	// Apply pagination
	pageSize := filters.PageSize
	if pageSize <= 0 {
		pageSize = 20 // Default page size
	}

	page := filters.Page
	if page <= 0 {
		page = 1
	}

	offset := (page - 1) * pageSize
	query = query.Offset(offset).Limit(pageSize)

	if err := query.Find(&userModels).Error; err != nil {
		return nil, fmt.Errorf("failed to list users: %w", err)
	}

	// Convert to entities
	users := make([]*entities.User, len(userModels))
	for i, model := range userModels {
		entity, err := model.ToEntity()
		if err != nil {
			return nil, fmt.Errorf("failed to convert model to entity at index %d: %w", i, err)
		}
		users[i] = entity
	}

	// Calculate pagination info
	totalPages := int((total + int64(pageSize) - 1) / int64(pageSize))
	hasNext := page < totalPages
	hasPrevious := page > 1

	return &repositories.PaginatedUsers{
		Users:       users,
		Total:       total,
		Page:        page,
		PageSize:    pageSize,
		TotalPages:  totalPages,
		HasNext:     hasNext,
		HasPrevious: hasPrevious,
	}, nil
}

// Count returns the total number of users matching filters
func (r *PostgreSQLUserRepository) Count(ctx context.Context, filters repositories.UserFilters) (int64, error) {
	query := r.db.WithContext(ctx).Model(&models.UserModel{})

	// Apply same filters as List
	if filters.Rol != nil {
		query = query.Where("rol = ?", string(*filters.Rol))
	}

	if filters.IsActive != nil {
		query = query.Where("is_active = ?", *filters.IsActive)
	}

	if filters.FichaID != nil {
		query = query.Where("ficha_id = ?", *filters.FichaID)
	}

	if filters.Programa != nil {
		query = query.Where("programa_formacion = ?", *filters.Programa)
	}

	if filters.Search != nil && *filters.Search != "" {
		searchPattern := "%" + *filters.Search + "%"
		query = query.Where(
			"LOWER(nombre) LIKE LOWER(?) OR LOWER(apellido) LIKE LOWER(?) OR LOWER(email) LIKE LOWER(?) OR documento LIKE ?",
			searchPattern, searchPattern, searchPattern, searchPattern,
		)
	}

	var count int64
	if err := query.Count(&count).Error; err != nil {
		return 0, fmt.Errorf("failed to count users: %w", err)
	}

	return count, nil
}

// ExistsByEmail checks if a user exists with the given email
func (r *PostgreSQLUserRepository) ExistsByEmail(ctx context.Context, email string) (bool, error) {
	var count int64
	if err := r.db.WithContext(ctx).Model(&models.UserModel{}).Where("email = ?", email).Count(&count).Error; err != nil {
		return false, fmt.Errorf("failed to check email existence: %w", err)
	}
	return count > 0, nil
}

// ExistsByDocumento checks if a user exists with the given document number
func (r *PostgreSQLUserRepository) ExistsByDocumento(ctx context.Context, documento string) (bool, error) {
	var count int64
	if err := r.db.WithContext(ctx).Model(&models.UserModel{}).Where("documento = ?", documento).Count(&count).Error; err != nil {
		return false, fmt.Errorf("failed to check document existence: %w", err)
	}
	return count > 0, nil
}

// GetByRol retrieves users by role
func (r *PostgreSQLUserRepository) GetByRol(ctx context.Context, rol entities.UserRole) ([]*entities.User, error) {
	rolPtr := &rol
	filters := repositories.UserFilters{
		Rol: rolPtr,
	}
	result, err := r.List(ctx, filters)
	if err != nil {
		return nil, err
	}
	return result.Users, nil
}

// GetByFicha retrieves users by ficha ID (implementation of GetByFichaID)
func (r *PostgreSQLUserRepository) GetByFicha(ctx context.Context, fichaID string) ([]*entities.User, error) {
	filters := repositories.UserFilters{
		FichaID: &fichaID,
	}
	result, err := r.List(ctx, filters)
	if err != nil {
		return nil, err
	}
	return result.Users, nil
}

// GetActiveUsers retrieves all active users
func (r *PostgreSQLUserRepository) GetActiveUsers(ctx context.Context) ([]*entities.User, error) {
	isActive := true
	filters := repositories.UserFilters{
		IsActive: &isActive,
	}
	result, err := r.List(ctx, filters)
	if err != nil {
		return nil, err
	}
	return result.Users, nil
}

// GetActiveInstructors retrieves all active instructors
func (r *PostgreSQLUserRepository) GetActiveInstructors(ctx context.Context) ([]*entities.User, error) {
	isActive := true
	rol := entities.RoleInstructor
	filters := repositories.UserFilters{
		IsActive: &isActive,
		Rol:      &rol,
	}
	result, err := r.List(ctx, filters)
	if err != nil {
		return nil, err
	}
	return result.Users, nil
}

// GetInactiveUsers retrieves users inactive for specified days
func (r *PostgreSQLUserRepository) GetInactiveUsers(ctx context.Context, daysInactive int) ([]*entities.User, error) {
	var userModels []models.UserModel

	cutoffDate := time.Now().AddDate(0, 0, -daysInactive)

	query := r.db.WithContext(ctx).Where(
		"is_active = ? OR (last_login IS NOT NULL AND last_login < ?) OR (last_login IS NULL AND created_at < ?)",
		false, cutoffDate, cutoffDate,
	)

	if err := query.Find(&userModels).Error; err != nil {
		return nil, fmt.Errorf("failed to get inactive users: %w", err)
	}

	// Convert to entities
	users := make([]*entities.User, len(userModels))
	for i, model := range userModels {
		entity, err := model.ToEntity()
		if err != nil {
			return nil, fmt.Errorf("failed to convert model to entity at index %d: %w", i, err)
		}
		users[i] = entity
	}

	return users, nil
}

// CountByRol returns the count of users by role
func (r *PostgreSQLUserRepository) CountByRol(ctx context.Context, rol entities.UserRole) (int64, error) {
	rolPtr := &rol
	filters := repositories.UserFilters{
		Rol: rolPtr,
	}
	return r.Count(ctx, filters)
}

// BulkCreate creates multiple users in a transaction
func (r *PostgreSQLUserRepository) BulkCreate(ctx context.Context, users []*entities.User) error {
	return r.db.WithContext(ctx).Transaction(func(tx *gorm.DB) error {
		for _, user := range users {
			model := models.NewUserModelFromEntity(user)
			if err := tx.Create(model).Error; err != nil {
				return fmt.Errorf("failed to create user in bulk: %w", err)
			}

			// Update entity with generated data
			entity, err := model.ToEntity()
			if err != nil {
				return fmt.Errorf("failed to convert model to entity in bulk: %w", err)
			}
			*user = *entity
		}
		return nil
	})
}

// BulkUpdate actualiza múltiples usuarios en una operación
func (r *PostgreSQLUserRepository) BulkUpdate(ctx context.Context, updates map[string]*entities.User) (*repositories.BulkOperationResult, error) {
	result := &repositories.BulkOperationResult{
		Total:  len(updates),
		Errors: make([]repositories.BulkOperationError, 0),
	}

	return result, r.db.WithContext(ctx).Transaction(func(tx *gorm.DB) error {
		for email, user := range updates {
			model := models.NewUserModelFromEntity(user)

			if err := tx.Where("email = ?", email).Save(model).Error; err != nil {
				result.Failed++
				result.Errors = append(result.Errors, repositories.BulkOperationError{
					User:  email,
					Error: err.Error(),
				})
				continue
			}
			result.Success++
		}
		return nil
	})
}

// BulkDelete elimina múltiples usuarios por emails
func (r *PostgreSQLUserRepository) BulkDelete(ctx context.Context, emails []string) (*repositories.BulkOperationResult, error) {
	result := &repositories.BulkOperationResult{
		Total:  len(emails),
		Errors: make([]repositories.BulkOperationError, 0),
	}

	return result, r.db.WithContext(ctx).Transaction(func(tx *gorm.DB) error {
		for _, email := range emails {
			deleteResult := tx.Where("email = ?", email).Delete(&models.UserModel{})

			if deleteResult.Error != nil {
				result.Failed++
				result.Errors = append(result.Errors, repositories.BulkOperationError{
					User:  email,
					Error: deleteResult.Error.Error(),
				})
				continue
			}

			if deleteResult.RowsAffected == 0 {
				result.Failed++
				result.Errors = append(result.Errors, repositories.BulkOperationError{
					User:  email,
					Error: "user not found",
				})
				continue
			}

			result.Success++
		}
		return nil
	})
}

// BulkStatusChange cambia el estado de múltiples usuarios
func (r *PostgreSQLUserRepository) BulkStatusChange(ctx context.Context, emails []string, isActive bool) (*repositories.BulkOperationResult, error) {
	result := &repositories.BulkOperationResult{
		Total:  len(emails),
		Errors: make([]repositories.BulkOperationError, 0),
	}

	return result, r.db.WithContext(ctx).Transaction(func(tx *gorm.DB) error {
		for _, email := range emails {
			updateResult := tx.Model(&models.UserModel{}).
				Where("email = ?", email).
				Updates(map[string]interface{}{
					"is_active":  isActive,
					"updated_at": time.Now(),
				})

			if updateResult.Error != nil {
				result.Failed++
				result.Errors = append(result.Errors, repositories.BulkOperationError{
					User:  email,
					Error: updateResult.Error.Error(),
				})
				continue
			}

			if updateResult.RowsAffected == 0 {
				result.Failed++
				result.Errors = append(result.Errors, repositories.BulkOperationError{
					User:  email,
					Error: "user not found",
				})
				continue
			}

			result.Success++
		}
		return nil
	})
}

// GetMultipleByEmails obtiene múltiples usuarios por sus emails
func (r *PostgreSQLUserRepository) GetMultipleByEmails(ctx context.Context, emails []string) ([]*entities.User, error) {
	var models []models.UserModel

	if err := r.db.WithContext(ctx).Where("email IN ?", emails).Find(&models).Error; err != nil {
		return nil, fmt.Errorf("failed to get multiple users by emails: %w", err)
	}

	users := make([]*entities.User, len(models))
	for i, model := range models {
		user, err := model.ToEntity()
		if err != nil {
			return nil, fmt.Errorf("failed to convert model to entity: %w", err)
		}
		users[i] = user
	}

	return users, nil
}
