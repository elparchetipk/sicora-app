package repositories

import (
	"context"
	"time"

	"scheduleservice/internal/domain/entities"

	"github.com/google/uuid"
)

// ScheduleRepository define las operaciones para gestionar horarios
type ScheduleRepository interface {
	// CRUD básico
	Create(ctx context.Context, schedule *entities.Schedule) (*entities.Schedule, error)
	GetByID(ctx context.Context, id uuid.UUID) (*entities.Schedule, error)
	Update(ctx context.Context, schedule *entities.Schedule) (*entities.Schedule, error)
	Delete(ctx context.Context, id uuid.UUID) error

	// Listado con filtros
	List(ctx context.Context, filter ScheduleFilter) ([]*entities.Schedule, int64, error)

	// Búsquedas específicas
	GetByInstructor(ctx context.Context, instructorID uuid.UUID, date time.Time) ([]*entities.Schedule, error)
	GetByAcademicGroup(ctx context.Context, groupID uuid.UUID, startDate, endDate time.Time) ([]*entities.Schedule, error)
	GetByVenue(ctx context.Context, venueID uuid.UUID, date time.Time) ([]*entities.Schedule, error)

	// Validaciones de conflictos
	CheckInstructorConflict(ctx context.Context, instructorID uuid.UUID, dayOfWeek int, startTime, endTime time.Time, excludeID *uuid.UUID) (bool, error)
	CheckVenueConflict(ctx context.Context, venueID uuid.UUID, dayOfWeek int, startTime, endTime time.Time, excludeID *uuid.UUID) (bool, error)
	CheckGroupConflict(ctx context.Context, groupID uuid.UUID, dayOfWeek int, startTime, endTime time.Time, excludeID *uuid.UUID) (bool, error)

	// Operaciones masivas
	CreateBatch(ctx context.Context, schedules []*entities.Schedule) ([]*entities.Schedule, error)
	UpdateBatch(ctx context.Context, schedules []*entities.Schedule) ([]*entities.Schedule, error)
	DeleteBatch(ctx context.Context, ids []uuid.UUID) error
}

// AcademicProgramRepository define las operaciones para programas académicos
type AcademicProgramRepository interface {
	Create(ctx context.Context, program *entities.AcademicProgram) (*entities.AcademicProgram, error)
	GetByID(ctx context.Context, id uuid.UUID) (*entities.AcademicProgram, error)
	GetByCode(ctx context.Context, code string) (*entities.AcademicProgram, error)
	Update(ctx context.Context, program *entities.AcademicProgram) (*entities.AcademicProgram, error)
	Delete(ctx context.Context, id uuid.UUID) error
	List(ctx context.Context, filter BaseFilter) ([]*entities.AcademicProgram, int64, error)
	ListActive(ctx context.Context) ([]*entities.AcademicProgram, error)
}

// AcademicGroupRepository define las operaciones para fichas/grupos
type AcademicGroupRepository interface {
	Create(ctx context.Context, group *entities.AcademicGroup) (*entities.AcademicGroup, error)
	GetByID(ctx context.Context, id uuid.UUID) (*entities.AcademicGroup, error)
	GetByNumber(ctx context.Context, number string) (*entities.AcademicGroup, error)
	Update(ctx context.Context, group *entities.AcademicGroup) (*entities.AcademicGroup, error)
	Delete(ctx context.Context, id uuid.UUID) error
	List(ctx context.Context, filter AcademicGroupFilter) ([]*entities.AcademicGroup, int64, error)
	ListActive(ctx context.Context) ([]*entities.AcademicGroup, error)
	GetByProgram(ctx context.Context, programID uuid.UUID) ([]*entities.AcademicGroup, error)
}

// VenueRepository define las operaciones para ambientes/aulas
type VenueRepository interface {
	Create(ctx context.Context, venue *entities.Venue) (*entities.Venue, error)
	GetByID(ctx context.Context, id uuid.UUID) (*entities.Venue, error)
	GetByCode(ctx context.Context, code string) (*entities.Venue, error)
	Update(ctx context.Context, venue *entities.Venue) (*entities.Venue, error)
	Delete(ctx context.Context, id uuid.UUID) error
	List(ctx context.Context, filter VenueFilter) ([]*entities.Venue, int64, error)
	ListActive(ctx context.Context) ([]*entities.Venue, error)
	GetByCampus(ctx context.Context, campusID uuid.UUID) ([]*entities.Venue, error)
}

// CampusRepository define las operaciones para sedes
type CampusRepository interface {
	Create(ctx context.Context, campus *entities.Campus) (*entities.Campus, error)
	GetByID(ctx context.Context, id uuid.UUID) (*entities.Campus, error)
	GetByCode(ctx context.Context, code string) (*entities.Campus, error)
	Update(ctx context.Context, campus *entities.Campus) (*entities.Campus, error)
	Delete(ctx context.Context, id uuid.UUID) error
	List(ctx context.Context, filter BaseFilter) ([]*entities.Campus, int64, error)
	ListActive(ctx context.Context) ([]*entities.Campus, error)
}

// Estructuras de filtro para queries

// BaseFilter filtro básico compartido
type BaseFilter struct {
	Page     int    `json:"page" form:"page" validate:"min=1"`
	PageSize int    `json:"page_size" form:"page_size" validate:"min=1,max=100"`
	Search   string `json:"search" form:"search" validate:"max=100"`
	IsActive *bool  `json:"is_active" form:"is_active"`
}

// ScheduleFilter filtro específico para horarios
type ScheduleFilter struct {
	BaseFilter
	InstructorID    *uuid.UUID `json:"instructor_id" form:"instructor_id"`
	AcademicGroupID *uuid.UUID `json:"academic_group_id" form:"academic_group_id"`
	VenueID         *uuid.UUID `json:"venue_id" form:"venue_id"`
	DayOfWeek       *int       `json:"day_of_week" form:"day_of_week" validate:"omitempty,min=1,max=7"`
	StartDate       *time.Time `json:"start_date" form:"start_date"`
	EndDate         *time.Time `json:"end_date" form:"end_date"`
	Status          string     `json:"status" form:"status" validate:"omitempty,oneof=ACTIVE CANCELLED SUSPENDED"`
	Subject         string     `json:"subject" form:"subject" validate:"max=200"`
	BlockIdentifier string     `json:"block_identifier" form:"block_identifier" validate:"max=10"`
}

// AcademicGroupFilter filtro específico para fichas
type AcademicGroupFilter struct {
	BaseFilter
	AcademicProgramID *uuid.UUID `json:"academic_program_id" form:"academic_program_id"`
	Quarter           *int       `json:"quarter" form:"quarter" validate:"omitempty,min=1,max=10"`
	Year              *int       `json:"year" form:"year" validate:"omitempty,min=2020,max=2030"`
	Shift             string     `json:"shift" form:"shift" validate:"omitempty,oneof=MANANA TARDE NOCHE"`
}

// VenueFilter filtro específico para ambientes
type VenueFilter struct {
	BaseFilter
	CampusID *uuid.UUID `json:"campus_id" form:"campus_id"`
	Type     string     `json:"type" form:"type" validate:"omitempty,oneof=AULA LABORATORIO TALLER AUDITORIO BIBLIOTECA"`
	Floor    string     `json:"floor" form:"floor" validate:"max=10"`
}

// Métodos de utilidad para filtros

// SetDefaults establece valores por defecto para BaseFilter
func (f *BaseFilter) SetDefaults() {
	if f.Page <= 0 {
		f.Page = 1
	}
	if f.PageSize <= 0 {
		f.PageSize = 20
	}
	if f.PageSize > 100 {
		f.PageSize = 100
	}
}

// GetOffset calcula el offset para paginación
func (f *BaseFilter) GetOffset() int {
	return (f.Page - 1) * f.PageSize
}

// GetLimit retorna el límite para paginación
func (f *BaseFilter) GetLimit() int {
	return f.PageSize
}
