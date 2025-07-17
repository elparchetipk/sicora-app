package external

import (
	"bytes"
	"context"
	"encoding/json"
	"fmt"
	"net/http"
	"time"

	"github.com/google/uuid"
)

// NotificationServiceAdapter representa el adaptador para el servicio de notificaciones
type NotificationServiceAdapter struct {
	baseURL    string
	httpClient *http.Client
	apiKey     string
}

// NotificationRequest representa una solicitud de notificación
type NotificationRequest struct {
	RecipientID uuid.UUID `json:"recipient_id"`
	Type        string    `json:"type"`
	Title       string    `json:"title"`
	Message     string    `json:"message"`
	Data        string    `json:"data,omitempty"`
	Priority    string    `json:"priority,omitempty"`
	Channel     string    `json:"channel,omitempty"`
}

// NotificationResponse representa la respuesta del servicio de notificaciones
type NotificationResponse struct {
	ID      uuid.UUID `json:"id"`
	Message string    `json:"message"`
	Success bool      `json:"success"`
}

// BulkNotificationRequest representa una solicitud de notificación masiva
type BulkNotificationRequest struct {
	RecipientIDs []uuid.UUID `json:"recipient_ids"`
	Type         string      `json:"type"`
	Title        string      `json:"title"`
	Message      string      `json:"message"`
	Data         string      `json:"data,omitempty"`
	Priority     string      `json:"priority,omitempty"`
	Channel      string      `json:"channel,omitempty"`
}

// BulkNotificationResponse representa la respuesta de notificación masiva
type BulkNotificationResponse struct {
	SentCount   int      `json:"sent_count"`
	FailedCount int      `json:"failed_count"`
	FailedIDs   []string `json:"failed_ids,omitempty"`
	Message     string   `json:"message"`
	Success     bool     `json:"success"`
}

// NewNotificationServiceAdapter crea un nuevo adaptador para el servicio de notificaciones
func NewNotificationServiceAdapter(baseURL, apiKey string) *NotificationServiceAdapter {
	return &NotificationServiceAdapter{
		baseURL: baseURL,
		apiKey:  apiKey,
		httpClient: &http.Client{
			Timeout: 30 * time.Second,
		},
	}
}

// SendNotification envía una notificación individual
func (a *NotificationServiceAdapter) SendNotification(ctx context.Context, req *NotificationRequest) (*NotificationResponse, error) {
	url := fmt.Sprintf("%s/api/v1/notifications", a.baseURL)

	jsonData, err := json.Marshal(req)
	if err != nil {
		return nil, fmt.Errorf("failed to marshal request: %w", err)
	}

	httpReq, err := http.NewRequestWithContext(ctx, "POST", url, bytes.NewBuffer(jsonData))
	if err != nil {
		return nil, fmt.Errorf("failed to create request: %w", err)
	}

	httpReq.Header.Set("Authorization", "Bearer "+a.apiKey)
	httpReq.Header.Set("Content-Type", "application/json")

	resp, err := a.httpClient.Do(httpReq)
	if err != nil {
		return nil, fmt.Errorf("failed to make request: %w", err)
	}
	defer resp.Body.Close()

	if resp.StatusCode != http.StatusCreated {
		return nil, fmt.Errorf("notification service returned status %d", resp.StatusCode)
	}

	var response NotificationResponse
	if err := json.NewDecoder(resp.Body).Decode(&response); err != nil {
		return nil, fmt.Errorf("failed to decode response: %w", err)
	}

	if !response.Success {
		return nil, fmt.Errorf("notification service error: %s", response.Message)
	}

	return &response, nil
}

// SendBulkNotification envía notificaciones masivas
func (a *NotificationServiceAdapter) SendBulkNotification(ctx context.Context, req *BulkNotificationRequest) (*BulkNotificationResponse, error) {
	url := fmt.Sprintf("%s/api/v1/notifications/bulk", a.baseURL)

	jsonData, err := json.Marshal(req)
	if err != nil {
		return nil, fmt.Errorf("failed to marshal request: %w", err)
	}

	httpReq, err := http.NewRequestWithContext(ctx, "POST", url, bytes.NewBuffer(jsonData))
	if err != nil {
		return nil, fmt.Errorf("failed to create request: %w", err)
	}

	httpReq.Header.Set("Authorization", "Bearer "+a.apiKey)
	httpReq.Header.Set("Content-Type", "application/json")

	resp, err := a.httpClient.Do(httpReq)
	if err != nil {
		return nil, fmt.Errorf("failed to make request: %w", err)
	}
	defer resp.Body.Close()

	if resp.StatusCode != http.StatusCreated {
		return nil, fmt.Errorf("notification service returned status %d", resp.StatusCode)
	}

	var response BulkNotificationResponse
	if err := json.NewDecoder(resp.Body).Decode(&response); err != nil {
		return nil, fmt.Errorf("failed to decode response: %w", err)
	}

	if !response.Success {
		return nil, fmt.Errorf("notification service error: %s", response.Message)
	}

	return &response, nil
}

// SendEvaluationReminder envía un recordatorio de evaluación
func (a *NotificationServiceAdapter) SendEvaluationReminder(ctx context.Context, studentID uuid.UUID, instructorName, periodName string) error {
	req := &NotificationRequest{
		RecipientID: studentID,
		Type:        "evaluation_reminder",
		Title:       "Recordatorio de Evaluación",
		Message:     fmt.Sprintf("Tienes pendiente evaluar al instructor %s en el período %s", instructorName, periodName),
		Priority:    "medium",
		Channel:     "email,push",
	}

	_, err := a.SendNotification(ctx, req)
	return err
}

// SendEvaluationCompleted notifica que una evaluación fue completada
func (a *NotificationServiceAdapter) SendEvaluationCompleted(ctx context.Context, instructorID uuid.UUID, studentName, periodName string) error {
	req := &NotificationRequest{
		RecipientID: instructorID,
		Type:        "evaluation_completed",
		Title:       "Evaluación Completada",
		Message:     fmt.Sprintf("El estudiante %s ha completado tu evaluación en el período %s", studentName, periodName),
		Priority:    "low",
		Channel:     "email",
	}

	_, err := a.SendNotification(ctx, req)
	return err
}

// SendPeriodStarted notifica que un período de evaluación ha comenzado
func (a *NotificationServiceAdapter) SendPeriodStarted(ctx context.Context, userIDs []uuid.UUID, periodName string) error {
	req := &BulkNotificationRequest{
		RecipientIDs: userIDs,
		Type:         "period_started",
		Title:        "Nuevo Período de Evaluación",
		Message:      fmt.Sprintf("Ha comenzado el período de evaluación: %s", periodName),
		Priority:     "high",
		Channel:      "email,push",
	}

	_, err := a.SendBulkNotification(ctx, req)
	return err
}

// SendPeriodEnding notifica que un período está por terminar
func (a *NotificationServiceAdapter) SendPeriodEnding(ctx context.Context, userIDs []uuid.UUID, periodName string, daysLeft int) error {
	req := &BulkNotificationRequest{
		RecipientIDs: userIDs,
		Type:         "period_ending",
		Title:        "Período de Evaluación Próximo a Terminar",
		Message:      fmt.Sprintf("El período %s terminará en %d días. No olvides completar tus evaluaciones pendientes.", periodName, daysLeft),
		Priority:     "high",
		Channel:      "email,push",
	}

	_, err := a.SendBulkNotification(ctx, req)
	return err
}
