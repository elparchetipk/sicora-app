package mocks

import (
	"attendanceservice/internal/domain/entities"
	"time"

	"github.com/google/uuid"
	"github.com/stretchr/testify/mock"
)

// MockAttendanceRepository mock del repositorio de asistencia
type MockAttendanceRepository struct {
	mock.Mock
}

func (m *MockAttendanceRepository) Create(attendance *entities.AttendanceRecord) error {
	args := m.Called(attendance)
	return args.Error(0)
}

func (m *MockAttendanceRepository) GetByID(id uuid.UUID) (*entities.AttendanceRecord, error) {
	args := m.Called(id)
	if args.Get(0) == nil {
		return nil, args.Error(1)
	}
	return args.Get(0).(*entities.AttendanceRecord), args.Error(1)
}

func (m *MockAttendanceRepository) Update(attendance *entities.AttendanceRecord) error {
	args := m.Called(attendance)
	return args.Error(0)
}

func (m *MockAttendanceRepository) Delete(id uuid.UUID) error {
	args := m.Called(id)
	return args.Error(0)
}

func (m *MockAttendanceRepository) GetByUserAndDateRange(userID uuid.UUID, startDate, endDate time.Time) ([]*entities.AttendanceRecord, error) {
	args := m.Called(userID, startDate, endDate)
	if args.Get(0) == nil {
		return nil, args.Error(1)
	}
	return args.Get(0).([]*entities.AttendanceRecord), args.Error(1)
}

func (m *MockAttendanceRepository) GetByClassAndDate(classID uuid.UUID, date time.Time) ([]*entities.AttendanceRecord, error) {
	args := m.Called(classID, date)
	if args.Get(0) == nil {
		return nil, args.Error(1)
	}
	return args.Get(0).([]*entities.AttendanceRecord), args.Error(1)
}

func (m *MockAttendanceRepository) BulkCreate(attendances []*entities.AttendanceRecord) error {
	args := m.Called(attendances)
	return args.Error(0)
}

// MockAttendanceAlertRepository mock del repositorio de alertas
type MockAttendanceAlertRepository struct {
	mock.Mock
}

func (m *MockAttendanceAlertRepository) Create(alert *entities.AttendanceAlert) error {
	args := m.Called(alert)
	return args.Error(0)
}

func (m *MockAttendanceAlertRepository) GetByID(id uuid.UUID) (*entities.AttendanceAlert, error) {
	args := m.Called(id)
	if args.Get(0) == nil {
		return nil, args.Error(1)
	}
	return args.Get(0).(*entities.AttendanceAlert), args.Error(1)
}

func (m *MockAttendanceAlertRepository) Update(alert *entities.AttendanceAlert) error {
	args := m.Called(alert)
	return args.Error(0)
}

func (m *MockAttendanceAlertRepository) Delete(id uuid.UUID) error {
	args := m.Called(id)
	return args.Error(0)
}

func (m *MockAttendanceAlertRepository) GetByUserID(userID uuid.UUID) ([]*entities.AttendanceAlert, error) {
	args := m.Called(userID)
	if args.Get(0) == nil {
		return nil, args.Error(1)
	}
	return args.Get(0).([]*entities.AttendanceAlert), args.Error(1)
}

func (m *MockAttendanceAlertRepository) GetActiveAlerts() ([]*entities.AttendanceAlert, error) {
	args := m.Called()
	if args.Get(0) == nil {
		return nil, args.Error(1)
	}
	return args.Get(0).([]*entities.AttendanceAlert), args.Error(1)
}

func (m *MockAttendanceAlertRepository) MarkAsRead(id uuid.UUID) error {
	args := m.Called(id)
	return args.Error(0)
}

func (m *MockAttendanceAlertRepository) GetUnreadCount(userID uuid.UUID) (int64, error) {
	args := m.Called(userID)
	return args.Get(0).(int64), args.Error(1)
}
