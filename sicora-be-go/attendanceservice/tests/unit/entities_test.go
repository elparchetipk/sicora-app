package unit

import (
	"testing"
	"time"

	"attendanceservice/internal/domain/entities"

	"github.com/google/uuid"
	"github.com/stretchr/testify/assert"
)

func TestAttendanceRecord_ValidateFields(t *testing.T) {
	tests := []struct {
		name        string
		attendance  *entities.AttendanceRecord
		expectError bool
	}{
		{
			name: "Valid attendance record",
			attendance: &entities.AttendanceRecord{
				ID:         uuid.New(),
				UserID:     uuid.New(),
				ClassID:    uuid.New(),
				InTime:     time.Now(),
				Status:     "present",
				RecordedBy: uuid.New(),
				CreatedAt:  time.Now(),
				UpdatedAt:  time.Now(),
			},
			expectError: false,
		},
		{
			name: "Invalid status",
			attendance: &entities.AttendanceRecord{
				ID:         uuid.New(),
				UserID:     uuid.New(),
				ClassID:    uuid.New(),
				InTime:     time.Now(),
				Status:     "invalid_status",
				RecordedBy: uuid.New(),
				CreatedAt:  time.Now(),
				UpdatedAt:  time.Now(),
			},
			expectError: true,
		},
		{
			name: "Missing required fields",
			attendance: &entities.AttendanceRecord{
				ID:     uuid.New(),
				Status: "present",
			},
			expectError: true,
		},
	}

	for _, tt := range tests {
		t.Run(tt.name, func(t *testing.T) {
			err := tt.attendance.Validate()
			if tt.expectError {
				assert.Error(t, err)
			} else {
				assert.NoError(t, err)
			}
		})
	}
}

func TestAttendanceRecord_IsLate(t *testing.T) {
	now := time.Now()
	classTime := now.Add(-30 * time.Minute) // Clase empezó hace 30 minutos

	tests := []struct {
		name       string
		inTime     time.Time
		classTime  time.Time
		threshold  time.Duration
		expectLate bool
	}{
		{
			name:       "On time",
			inTime:     classTime.Add(5 * time.Minute),
			classTime:  classTime,
			threshold:  15 * time.Minute,
			expectLate: false,
		},
		{
			name:       "Late arrival",
			inTime:     classTime.Add(20 * time.Minute),
			classTime:  classTime,
			threshold:  15 * time.Minute,
			expectLate: true,
		},
	}

	for _, tt := range tests {
		t.Run(tt.name, func(t *testing.T) {
			attendance := &entities.AttendanceRecord{
				InTime: tt.inTime,
			}

			isLate := attendance.IsLate(tt.classTime, tt.threshold)
			assert.Equal(t, tt.expectLate, isLate)
		})
	}
}

func TestJustification_ValidateFields(t *testing.T) {
	tests := []struct {
		name          string
		justification *entities.Justification
		expectError   bool
	}{
		{
			name: "Valid justification",
			justification: &entities.Justification{
				ID:           uuid.New(),
				UserID:       uuid.New(),
				AttendanceID: uuid.New(),
				Reason:       "Medical appointment",
				Status:       "pending",
				CreatedAt:    time.Now(),
				UpdatedAt:    time.Now(),
			},
			expectError: false,
		},
		{
			name: "Empty reason",
			justification: &entities.Justification{
				ID:           uuid.New(),
				UserID:       uuid.New(),
				AttendanceID: uuid.New(),
				Reason:       "",
				Status:       "pending",
			},
			expectError: true,
		},
	}

	for _, tt := range tests {
		t.Run(tt.name, func(t *testing.T) {
			err := tt.justification.Validate()
			if tt.expectError {
				assert.Error(t, err)
			} else {
				assert.NoError(t, err)
			}
		})
	}
}
