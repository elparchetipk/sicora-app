package repositories

import (
	"context"
	"fmt"

	"scheduleservice/internal/domain/entities"
	"scheduleservice/internal/domain/repositories"
	"scheduleservice/internal/infrastructure/database/models"

	"github.com/google/uuid"
	"gorm.io/gorm"
)

// AcademicProgramRepositoryImpl implementa AcademicProgramRepository usando GORM
type AcademicProgramRepositoryImpl struct {
	db *gorm.DB
}

// NewAcademicProgramRepository crea una nueva instancia del repositorio
func NewAcademicProgramRepository(db *gorm.DB) repositories.AcademicProgramRepository {
	return &AcademicProgramRepositoryImpl{
		db: db,
	}
}

// Create implementa la creación de un programa académico
func (r *AcademicProgramRepositoryImpl) Create(ctx context.Context, program *entities.AcademicProgram) (*entities.AcademicProgram, error) {
	model := &models.AcademicProgramModel{}
	model.FromEntity(program)

	if err := r.db.WithContext(ctx).Create(model).Error; err != nil {
		return nil, fmt.Errorf("error creating academic program: %w", err)
	}

	return model.ToEntity(), nil
}

// GetByID implementa la búsqueda por ID
func (r *AcademicProgramRepositoryImpl) GetByID(ctx context.Context, id uuid.UUID) (*entities.AcademicProgram, error) {
	var model models.AcademicProgramModel

	if err := r.db.WithContext(ctx).First(&model, "id = ?", id).Error; err != nil {
		if err == gorm.ErrRecordNotFound {
			return nil, nil
		}
		return nil, fmt.Errorf("error getting academic program by ID: %w", err)
	}

	return model.ToEntity(), nil
}

// GetByCode implementa la búsqueda por código
func (r *AcademicProgramRepositoryImpl) GetByCode(ctx context.Context, code string) (*entities.AcademicProgram, error) {
	var model models.AcademicProgramModel

	if err := r.db.WithContext(ctx).First(&model, "code = ?", code).Error; err != nil {
		if err == gorm.ErrRecordNotFound {
			return nil, nil
		}
		return nil, fmt.Errorf("error getting academic program by code: %w", err)
	}

	return model.ToEntity(), nil
}

// Update implementa la actualización de un programa académico
func (r *AcademicProgramRepositoryImpl) Update(ctx context.Context, program *entities.AcademicProgram) (*entities.AcademicProgram, error) {
	model := &models.AcademicProgramModel{}
	model.FromEntity(program)

	if err := r.db.WithContext(ctx).
		Where("id = ?", program.ID).
		Updates(model).Error; err != nil {
		return nil, fmt.Errorf("error updating academic program: %w", err)
	}

	return model.ToEntity(), nil
}

// Delete implementa la eliminación de un programa académico
func (r *AcademicProgramRepositoryImpl) Delete(ctx context.Context, id uuid.UUID) error {
	if err := r.db.WithContext(ctx).Delete(&models.AcademicProgramModel{}, "id = ?", id).Error; err != nil {
		return fmt.Errorf("error deleting academic program: %w", err)
	}
	return nil
}

// List implementa el listado con filtros
func (r *AcademicProgramRepositoryImpl) List(ctx context.Context, filter repositories.BaseFilter) ([]*entities.AcademicProgram, int64, error) {
	var modelList []models.AcademicProgramModel
	var total int64

	query := r.db.WithContext(ctx).Model(&models.AcademicProgramModel{})

	// Aplicar filtros
	if filter.Search != "" {
		query = query.Where("name ILIKE ? OR code ILIKE ?",
			"%"+filter.Search+"%", "%"+filter.Search+"%")
	}
	if filter.IsActive != nil {
		query = query.Where("is_active = ?", *filter.IsActive)
	}

	// Contar total
	if err := query.Count(&total).Error; err != nil {
		return nil, 0, fmt.Errorf("error counting academic programs: %w", err)
	}

	// Aplicar paginación
	if filter.GetLimit() > 0 {
		query = query.Limit(filter.GetLimit())
	}
	if filter.GetOffset() > 0 {
		query = query.Offset(filter.GetOffset())
	}

	// Aplicar ordenamiento
	query = query.Order("name ASC")

	// Ejecutar consulta
	if err := query.Find(&modelList).Error; err != nil {
		return nil, 0, fmt.Errorf("error listing academic programs: %w", err)
	}

	// Convertir a entidades
	programs := make([]*entities.AcademicProgram, len(modelList))
	for i, model := range modelList {
		programs[i] = model.ToEntity()
	}

	return programs, total, nil
}

// ListActive implementa el listado de programas activos
func (r *AcademicProgramRepositoryImpl) ListActive(ctx context.Context) ([]*entities.AcademicProgram, error) {
	var modelList []models.AcademicProgramModel

	if err := r.db.WithContext(ctx).
		Where("is_active = true").
		Order("name ASC").
		Find(&modelList).Error; err != nil {
		return nil, fmt.Errorf("error listing active academic programs: %w", err)
	}

	programs := make([]*entities.AcademicProgram, len(modelList))
	for i, model := range modelList {
		programs[i] = model.ToEntity()
	}

	return programs, nil
}
