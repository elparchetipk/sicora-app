package repositories

import (
	"context"

	"github.com/google/uuid"
	"github.com/sicora-dev/evalinservice/internal/domain/entities"
	"github.com/sicora-dev/evalinservice/internal/domain/valueobjects"
)

type ReportRepository interface {
	Create(ctx context.Context, report *entities.Report) error
	GetByID(ctx context.Context, id uuid.UUID) (*entities.Report, error)
	GetByPeriodID(ctx context.Context, periodID uuid.UUID) ([]*entities.Report, error)
	GetByType(ctx context.Context, reportType valueobjects.ReportType) ([]*entities.Report, error)
	GetByStatus(ctx context.Context, status valueobjects.ReportStatus) ([]*entities.Report, error)
	GetByGeneratedBy(ctx context.Context, generatedBy uuid.UUID) ([]*entities.Report, error)
	Update(ctx context.Context, report *entities.Report) error
	Delete(ctx context.Context, id uuid.UUID) error
	GetPendingReports(ctx context.Context) ([]*entities.Report, error)
	GetCompletedReportsByPeriod(ctx context.Context, periodID uuid.UUID) ([]*entities.Report, error)
	GetReportsByDateRange(ctx context.Context, startDate, endDate string) ([]*entities.Report, error)
	CountByStatus(ctx context.Context, status valueobjects.ReportStatus) (int64, error)
}
