package entities

import (
	"time"

	"github.com/google/uuid"
)

// UserRole representa los roles disponibles en el sistema SICORA
type UserRole string

const (
	RoleAprendiz     UserRole = "aprendiz"
	RoleInstructor   UserRole = "instructor"
	RoleAdmin        UserRole = "admin"
	RoleCoordinador  UserRole = "coordinador"
)

// User representa la entidad de usuario en el dominio SICORA
// Contiene las reglas de negocio fundamentales para usuarios
type User struct {
	ID                  uuid.UUID `json:"id"`
	Nombre              string    `json:"nombre"`
	Apellido            string    `json:"apellido"`
	Email               string    `json:"email"`
	Documento           string    `json:"documento"`
	Rol                 UserRole  `json:"rol"`
	Password            string    `json:"-"` // Never serialize password
	FichaID             *string   `json:"ficha_id,omitempty"` // Solo para aprendices
	ProgramaFormacion   string    `json:"programa_formacion"`
	IsActive            bool      `json:"is_active"`
	MustChangePassword  bool      `json:"must_change_password"`
	CreatedAt           time.Time `json:"created_at"`
	UpdatedAt           time.Time `json:"updated_at"`
	LastLogin           *time.Time `json:"last_login,omitempty"`
}

// NewUser crea una nueva instancia de User con validaciones de dominio
func NewUser(nombre, apellido, email, documento string, rol UserRole, programaFormacion string) (*User, error) {
	if err := validateUserData(nombre, apellido, email, documento, rol); err != nil {
		return nil, err
	}

	now := time.Now()
	user := &User{
		ID:                 uuid.New(),
		Nombre:             nombre,
		Apellido:           apellido,
		Email:              email,
		Documento:          documento,
		Rol:                rol,
		ProgramaFormacion:  programaFormacion,
		IsActive:           true,
		MustChangePassword: true,
		CreatedAt:          now,
		UpdatedAt:          now,
	}

	return user, nil
}

// GetFullName retorna el nombre completo del usuario
func (u *User) GetFullName() string {
	return u.Nombre + " " + u.Apellido
}

// IsAprendiz verifica si el usuario es un aprendiz
func (u *User) IsAprendiz() bool {
	return u.Rol == RoleAprendiz
}

// IsInstructor verifica si el usuario es un instructor
func (u *User) IsInstructor() bool {
	return u.Rol == RoleInstructor
}

// IsAdmin verifica si el usuario es administrador
func (u *User) IsAdmin() bool {
	return u.Rol == RoleAdmin
}

// CanAccessFicha valida si el usuario puede acceder a información de fichas
func (u *User) CanAccessFicha(fichaID string) bool {
	switch u.Rol {
	case RoleAdmin, RoleCoordinador:
		return true
	case RoleAprendiz:
		return u.FichaID != nil && *u.FichaID == fichaID
	case RoleInstructor:
		// Los instructores pueden acceder a fichas donde enseñan
		// Esta lógica se implementará en los casos de uso
		return true
	default:
		return false
	}
}

// AssignFicha asigna una ficha a un aprendiz
func (u *User) AssignFicha(fichaID string) error {
	if !u.IsAprendiz() {
		return NewDomainError("solo los aprendices pueden tener fichas asignadas")
	}
	
	if u.FichaID != nil {
		return NewDomainError("el aprendiz ya tiene una ficha asignada")
	}
	
	u.FichaID = &fichaID
	u.UpdatedAt = time.Now()
	return nil
}

// MarkAsLoggedIn actualiza el timestamp del último login
func (u *User) MarkAsLoggedIn() {
	now := time.Now()
	u.LastLogin = &now
	u.UpdatedAt = now
}

// Deactivate desactiva el usuario
func (u *User) Deactivate() {
	u.IsActive = false
	u.UpdatedAt = time.Now()
}

// Activate activa el usuario
func (u *User) Activate() {
	u.IsActive = true
	u.UpdatedAt = time.Now()
}

// UpdatePassword actualiza la contraseña del usuario
func (u *User) UpdatePassword(hashedPassword string) {
	u.Password = hashedPassword
	u.MustChangePassword = false
	u.UpdatedAt = time.Now()
}
