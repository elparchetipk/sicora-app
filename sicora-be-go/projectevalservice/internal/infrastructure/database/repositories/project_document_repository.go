package repositories

import (
	"context"
	"fmt"

	"projectevalservice/internal/domain/entities"
	"projectevalservice/internal/domain/repositories"
	"projectevalservice/internal/infrastructure/database/models"

	"github.com/google/uuid"
	"gorm.io/gorm"
)

type projectDocumentRepository struct {
	db *gorm.DB
}

func NewProjectDocumentRepository(db *gorm.DB) repositories.ProjectDocumentRepository {
	return &projectDocumentRepository{db: db}
}

func (r *projectDocumentRepository) Create(ctx context.Context, document *entities.ProjectDocument) error {
	model := models.ProjectDocumentFromEntity(document)
	return r.db.WithContext(ctx).Create(model).Error
}

func (r *projectDocumentRepository) GetByID(ctx context.Context, id uuid.UUID) (*entities.ProjectDocument, error) {
	var model models.ProjectDocument
	err := r.db.WithContext(ctx).Where("id = ?", id).First(&model).Error
	if err != nil {
		return nil, err
	}
	return model.ToEntity(), nil
}

func (r *projectDocumentRepository) GetByProjectID(ctx context.Context, projectID uuid.UUID) ([]*entities.ProjectDocument, error) {
	var modelList []models.ProjectDocument
	err := r.db.WithContext(ctx).Where("project_id = ?", projectID).Order("created_at DESC").Find(&modelList).Error
	if err != nil {
		return nil, err
	}

	var entities []*entities.ProjectDocument
	for _, model := range modelList {
		entities = append(entities, model.ToEntity())
	}
	return entities, nil
}

func (r *projectDocumentRepository) GetByUploadedBy(ctx context.Context, uploadedByID uuid.UUID) ([]*entities.ProjectDocument, error) {
	var modelList []models.ProjectDocument
	err := r.db.WithContext(ctx).Where("uploaded_by_id = ?", uploadedByID).Order("created_at DESC").Find(&modelList).Error
	if err != nil {
		return nil, err
	}

	var entities []*entities.ProjectDocument
	for _, model := range modelList {
		entities = append(entities, model.ToEntity())
	}
	return entities, nil
}

func (r *projectDocumentRepository) GetByType(ctx context.Context, projectID uuid.UUID, docType entities.DocumentType) ([]*entities.ProjectDocument, error) {
	var modelList []models.ProjectDocument
	err := r.db.WithContext(ctx).Where("project_id = ? AND type = ?", projectID, docType).Order("created_at DESC").Find(&modelList).Error
	if err != nil {
		return nil, err
	}

	var entities []*entities.ProjectDocument
	for _, model := range modelList {
		entities = append(entities, model.ToEntity())
	}
	return entities, nil
}

func (r *projectDocumentRepository) GetByStatus(ctx context.Context, status entities.DocumentStatus) ([]*entities.ProjectDocument, error) {
	var modelList []models.ProjectDocument
	err := r.db.WithContext(ctx).Where("status = ?", status).Order("created_at DESC").Find(&modelList).Error
	if err != nil {
		return nil, err
	}

	var entities []*entities.ProjectDocument
	for _, model := range modelList {
		entities = append(entities, model.ToEntity())
	}
	return entities, nil
}

func (r *projectDocumentRepository) Update(ctx context.Context, document *entities.ProjectDocument) error {
	model := models.ProjectDocumentFromEntity(document)
	return r.db.WithContext(ctx).Save(model).Error
}

func (r *projectDocumentRepository) Delete(ctx context.Context, id uuid.UUID) error {
	return r.db.WithContext(ctx).Delete(&models.ProjectDocument{}, "id = ?", id).Error
}

func (r *projectDocumentRepository) GetRequiredDocuments(ctx context.Context, projectID uuid.UUID) ([]*entities.ProjectDocument, error) {
	var modelList []models.ProjectDocument
	err := r.db.WithContext(ctx).Where("project_id = ? AND is_required = ?", projectID, true).Order("created_at DESC").Find(&modelList).Error
	if err != nil {
		return nil, err
	}

	var entities []*entities.ProjectDocument
	for _, model := range modelList {
		entities = append(entities, model.ToEntity())
	}
	return entities, nil
}

func (r *projectDocumentRepository) List(ctx context.Context, filters map[string]interface{}) ([]*entities.ProjectDocument, error) {
	var modelList []models.ProjectDocument
	query := r.db.WithContext(ctx)

	// Apply filters
	for key, value := range filters {
		switch key {
		case "project_id":
			query = query.Where("project_id = ?", value)
		case "uploaded_by_id":
			query = query.Where("uploaded_by_id = ?", value)
		case "type":
			query = query.Where("type = ?", value)
		case "status":
			query = query.Where("status = ?", value)
		case "visibility":
			query = query.Where("visibility = ?", value)
		case "is_required":
			query = query.Where("is_required = ?", value)
		case "is_template":
			query = query.Where("is_template = ?", value)
		case "title":
			query = query.Where("title ILIKE ?", fmt.Sprintf("%%%s%%", value))
		case "tags":
			if tags, ok := value.([]string); ok {
				for _, tag := range tags {
					query = query.Where("tags::text ILIKE ?", fmt.Sprintf("%%%s%%", tag))
				}
			}
		case "created_after":
			query = query.Where("created_at >= ?", value)
		case "created_before":
			query = query.Where("created_at <= ?", value)
		case "limit":
			if limit, ok := value.(int); ok {
				query = query.Limit(limit)
			}
		case "offset":
			if offset, ok := value.(int); ok {
				query = query.Offset(offset)
			}
		case "order_by":
			if orderBy, ok := value.(string); ok {
				switch orderBy {
				case "title":
					query = query.Order("title ASC")
				case "created_at":
					query = query.Order("created_at DESC")
				case "updated_at":
					query = query.Order("updated_at DESC")
				case "download_count":
					query = query.Order("download_count DESC")
				default:
					query = query.Order("created_at DESC")
				}
			}
		}
	}

	// Default ordering if not specified
	if _, hasOrder := filters["order_by"]; !hasOrder {
		query = query.Order("created_at DESC")
	}

	err := query.Find(&modelList).Error
	if err != nil {
		return nil, err
	}

	var entities []*entities.ProjectDocument
	for _, model := range modelList {
		entities = append(entities, model.ToEntity())
	}
	return entities, nil
}
