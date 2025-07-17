package dtos

import (
	"time"

	"github.com/google/uuid"
)

// CreateJustificationRequest representa la solicitud para crear una justificación
type CreateJustificationRequest struct {
	AttendanceID uuid.UUID `json:"attendance_id" validate:"required"`
	StudentID    uuid.UUID `json:"student_id" validate:"required"`
	Reason       string    `json:"reason" validate:"required,min=10,max=500"`
	Description  string    `json:"description,omitempty" validate:"max=1000"`
}

// UpdateJustificationRequest representa la solicitud para actualizar una justificación
type UpdateJustificationRequest struct {
	Reason      *string `json:"reason,omitempty" validate:"omitempty,min=10,max=500"`
	Description *string `json:"description,omitempty" validate:"omitempty,max=1000"`
}

// JustificationResponse representa la respuesta de una justificación
type JustificationResponse struct {
	ID              uuid.UUID  `json:"id"`
	AttendanceID    uuid.UUID  `json:"attendance_id"`
	StudentID       uuid.UUID  `json:"student_id"`
	Reason          string     `json:"reason"`
	Description     string     `json:"description,omitempty"`
	Status          string     `json:"status"`
	SubmittedAt     time.Time  `json:"submitted_at"`
	ReviewedAt      *time.Time `json:"reviewed_at,omitempty"`
	ReviewedBy      *uuid.UUID `json:"reviewed_by,omitempty"`
	RejectionReason string     `json:"rejection_reason,omitempty"`
	IsActive        bool       `json:"is_active"`
	CreatedAt       time.Time  `json:"created_at"`
	UpdatedAt       time.Time  `json:"updated_at"`
}

// ApproveJustificationRequest representa la solicitud para aprobar una justificación
type ApproveJustificationRequest struct {
	ApproverID uuid.UUID `json:"approver_id" validate:"required"`
}

// RejectJustificationRequest representa la solicitud para rechazar una justificación
type RejectJustificationRequest struct {
	ApproverID uuid.UUID `json:"approver_id" validate:"required"`
	Reason     string    `json:"reason" validate:"required,min=10,max=500"`
}

// JustificationListRequest representa la solicitud para listar justificaciones
type JustificationListRequest struct {
	UserID *uuid.UUID `json:"user_id,omitempty"`
	Status *string    `json:"status,omitempty" validate:"omitempty,oneof=PENDING APPROVED REJECTED"`
	Limit  int        `json:"limit" validate:"min=1,max=100"`
	Offset int        `json:"offset" validate:"min=0"`
}

// JustificationListResponse representa la respuesta de la lista de justificaciones
type JustificationListResponse struct {
	Justifications []JustificationResponse `json:"justifications"`
	Total          int                     `json:"total"`
	Limit          int                     `json:"limit"`
	Offset         int                     `json:"offset"`
}
