package usecases

import (
	"context"
	"errors"
	"time"

	"attendanceservice/internal/application/dtos"
	"attendanceservice/internal/domain/entities"
	"attendanceservice/internal/domain/repositories"

	"github.com/google/uuid"
)

type AlertUseCase struct {
	alertRepo repositories.AttendanceAlertRepository
}

func NewAlertUseCase(alertRepo repositories.AttendanceAlertRepository) *AlertUseCase {
	return &AlertUseCase{
		alertRepo: alertRepo,
	}
}

// CreateAlert crea una nueva alerta
func (uc *AlertUseCase) CreateAlert(ctx context.Context, req *dtos.CreateAlertRequest) (*dtos.AlertResponse, error) {
	alert := &entities.AttendanceAlert{
		ID:          uuid.New(),
		StudentID:   req.UserID,
		Type:        entities.AlertType(req.Type),
		Level:       entities.AlertLevel(req.Level),
		Title:       req.Title,
		Description: req.Message,
		Metadata:    req.Metadata,
		IsRead:      false,
		IsActive:    true,
		CreatedAt:   time.Now(),
		UpdatedAt:   time.Now(),
	}

	// Validar la alerta
	if !alert.IsValidAlertType() {
		return nil, errors.New("invalid alert type")
	}
	if !alert.IsValidAlertLevel() {
		return nil, errors.New("invalid alert level")
	}

	// Guardar en el repositorio
	if err := uc.alertRepo.Create(ctx, alert); err != nil {
		return nil, err
	}

	return uc.mapToAlertResponse(alert), nil
}

// UpdateAlert actualiza una alerta existente
func (uc *AlertUseCase) UpdateAlert(ctx context.Context, id uuid.UUID, req *dtos.UpdateAlertRequest) (*dtos.AlertResponse, error) {
	// Obtener la alerta existente
	alert, err := uc.alertRepo.GetByID(ctx, id)
	if err != nil {
		return nil, err
	}
	if alert == nil {
		return nil, errors.New("alert not found")
	}

	// Actualizar campos si están presentes
	if req.Title != nil {
		alert.Title = *req.Title
	}
	if req.Message != nil {
		alert.Description = *req.Message
	}
	if req.Metadata != nil {
		alert.Metadata = *req.Metadata
	}

	alert.UpdatedAt = time.Now()

	// Guardar cambios
	if err := uc.alertRepo.Update(ctx, alert); err != nil {
		return nil, err
	}

	return uc.mapToAlertResponse(alert), nil
}

// GetAlertByID obtiene una alerta por ID
func (uc *AlertUseCase) GetAlertByID(ctx context.Context, id uuid.UUID) (*dtos.AlertResponse, error) {
	alert, err := uc.alertRepo.GetByID(ctx, id)
	if err != nil {
		return nil, err
	}
	if alert == nil {
		return nil, errors.New("alert not found")
	}

	return uc.mapToAlertResponse(alert), nil
}

// GetAlertsByUser obtiene las alertas de un usuario
func (uc *AlertUseCase) GetAlertsByUser(ctx context.Context, req *dtos.AlertListRequest) (*dtos.AlertListResponse, error) {
	if req.UserID == nil {
		return nil, errors.New("user ID is required")
	}

	alerts, err := uc.alertRepo.GetByUserID(ctx, *req.UserID, req.Limit, req.Offset)
	if err != nil {
		return nil, err
	}

	// Aplicar filtros
	filteredAlerts := uc.applyFilters(alerts, req)

	responses := make([]dtos.AlertResponse, len(filteredAlerts))
	for i, alert := range filteredAlerts {
		responses[i] = *uc.mapToAlertResponse(alert)
	}

	return &dtos.AlertListResponse{
		Alerts: responses,
		Total:  len(filteredAlerts),
		Limit:  req.Limit,
		Offset: req.Offset,
	}, nil
}

// GetActiveAlerts obtiene las alertas activas
func (uc *AlertUseCase) GetActiveAlerts(ctx context.Context, req *dtos.AlertListRequest) (*dtos.AlertListResponse, error) {
	alerts, err := uc.alertRepo.GetActiveAlerts(ctx, req.Limit, req.Offset)
	if err != nil {
		return nil, err
	}

	// Aplicar filtros
	filteredAlerts := uc.applyFilters(alerts, req)

	responses := make([]dtos.AlertResponse, len(filteredAlerts))
	for i, alert := range filteredAlerts {
		responses[i] = *uc.mapToAlertResponse(alert)
	}

	return &dtos.AlertListResponse{
		Alerts: responses,
		Total:  len(filteredAlerts),
		Limit:  req.Limit,
		Offset: req.Offset,
	}, nil
}

// MarkAlertAsRead marca una alerta como leída
func (uc *AlertUseCase) MarkAlertAsRead(ctx context.Context, id uuid.UUID, req *dtos.MarkAlertAsReadRequest) (*dtos.AlertResponse, error) {
	// Obtener la alerta
	alert, err := uc.alertRepo.GetByID(ctx, id)
	if err != nil {
		return nil, err
	}
	if alert == nil {
		return nil, errors.New("alert not found")
	}

	// Marcar como leída
	alert.MarkAsRead(req.UserID)

	// Guardar cambios
	if err := uc.alertRepo.Update(ctx, alert); err != nil {
		return nil, err
	}

	return uc.mapToAlertResponse(alert), nil
}

// GetUnreadCount obtiene el número de alertas no leídas
func (uc *AlertUseCase) GetUnreadCount(ctx context.Context, userID uuid.UUID) (int, error) {
	return uc.alertRepo.GetUnreadCount(ctx, userID)
}

// GetAlertStats obtiene estadísticas de alertas
func (uc *AlertUseCase) GetAlertStats(ctx context.Context, userID uuid.UUID) (*dtos.AlertStatsResponse, error) {
	// Obtener todas las alertas del usuario
	alerts, err := uc.alertRepo.GetByUserID(ctx, userID, 1000, 0) // Obtener hasta 1000 alertas
	if err != nil {
		return nil, err
	}

	stats := &dtos.AlertStatsResponse{
		TotalAlerts:    len(alerts),
		UnreadAlerts:   0,
		CriticalAlerts: 0,
		AlertsByType:   make(map[string]int),
		AlertsByLevel:  make(map[string]int),
	}

	for _, alert := range alerts {
		// Contar no leídas
		if !alert.IsRead {
			stats.UnreadAlerts++
		}

		// Contar críticas
		if alert.IsCritical() {
			stats.CriticalAlerts++
		}

		// Contar por tipo
		alertType := string(alert.Type)
		stats.AlertsByType[alertType]++

		// Contar por nivel
		alertLevel := string(alert.Level)
		stats.AlertsByLevel[alertLevel]++
	}

	return stats, nil
}

// DeleteAlert elimina una alerta
func (uc *AlertUseCase) DeleteAlert(ctx context.Context, id uuid.UUID) error {
	// Verificar que la alerta existe
	alert, err := uc.alertRepo.GetByID(ctx, id)
	if err != nil {
		return err
	}
	if alert == nil {
		return errors.New("alert not found")
	}

	return uc.alertRepo.Delete(ctx, id)
}

// applyFilters aplica filtros a una lista de alertas
func (uc *AlertUseCase) applyFilters(alerts []*entities.AttendanceAlert, req *dtos.AlertListRequest) []*entities.AttendanceAlert {
	filtered := make([]*entities.AttendanceAlert, 0)

	for _, alert := range alerts {
		// Filtrar por tipo
		if req.Type != nil && string(alert.Type) != *req.Type {
			continue
		}

		// Filtrar por nivel
		if req.Level != nil && string(alert.Level) != *req.Level {
			continue
		}

		// Filtrar por estado de lectura
		if req.IsRead != nil && alert.IsRead != *req.IsRead {
			continue
		}

		// Filtrar por estado activo
		if req.IsActive != nil && alert.IsActive != *req.IsActive {
			continue
		}

		filtered = append(filtered, alert)
	}

	return filtered
}

// mapToAlertResponse convierte una entidad a DTO de respuesta
func (uc *AlertUseCase) mapToAlertResponse(alert *entities.AttendanceAlert) *dtos.AlertResponse {
	return &dtos.AlertResponse{
		ID:        alert.ID,
		UserID:    alert.StudentID,
		Type:      string(alert.Type),
		Level:     string(alert.Level),
		Title:     alert.Title,
		Message:   alert.Description,
		Metadata:  alert.Metadata,
		IsRead:    alert.IsRead,
		ReadBy:    alert.ReadBy,
		ReadAt:    alert.ReadAt,
		IsActive:  alert.IsActive,
		CreatedAt: alert.CreatedAt,
		UpdatedAt: alert.UpdatedAt,
	}
}
