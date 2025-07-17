package models

import (
	"time"

	"userservice/internal/domain/entities"

	"github.com/google/uuid"
	"gorm.io/gorm"
)

// UserModel represents the database model for users
// This is the infrastructure layer representation
type UserModel struct {
	ID                 uuid.UUID      `gorm:"type:uuid;primaryKey;default:gen_random_uuid()" json:"id"`
	Nombre             string         `gorm:"type:varchar(50);not null" json:"nombre"`
	Apellido           string         `gorm:"type:varchar(50);not null" json:"apellido"`
	Email              string         `gorm:"type:varchar(100);uniqueIndex;not null" json:"email"`
	Documento          string         `gorm:"type:varchar(15);uniqueIndex;not null" json:"documento"`
	Rol                string         `gorm:"type:varchar(20);not null" json:"rol"`
	Password           string         `gorm:"type:varchar(255);not null;column:password_hash" json:"-"`
	FichaID            *string        `gorm:"type:varchar(10);index" json:"ficha_id"`
	ProgramaFormacion  string         `gorm:"type:varchar(200)" json:"programa_formacion"`
	IsActive           bool           `gorm:"default:true;not null" json:"is_active"`
	MustChangePassword bool           `gorm:"default:true;not null" json:"must_change_password"`
	CreatedAt          time.Time      `gorm:"not null" json:"created_at"`
	UpdatedAt          time.Time      `gorm:"not null" json:"updated_at"`
	DeletedAt          gorm.DeletedAt `gorm:"index" json:"deleted_at,omitempty"`
	LastLogin          *time.Time     `gorm:"index" json:"last_login"`
}

// TableName returns the table name for GORM
func (UserModel) TableName() string {
	return "users"
}

// BeforeCreate sets UUID if not provided
func (u *UserModel) BeforeCreate(tx *gorm.DB) error {
	if u.ID == uuid.Nil {
		u.ID = uuid.New()
	}
	u.CreatedAt = time.Now()
	u.UpdatedAt = time.Now()
	return nil
}

// BeforeUpdate sets updated timestamp
func (u *UserModel) BeforeUpdate(tx *gorm.DB) error {
	u.UpdatedAt = time.Now()
	return nil
}

// ToEntity converts database model to domain entity
func (u *UserModel) ToEntity() (*entities.User, error) {
	return &entities.User{
		ID:                 u.ID,
		Nombre:             u.Nombre,
		Apellido:           u.Apellido,
		Email:              u.Email,
		Documento:          u.Documento,
		Rol:                entities.UserRole(u.Rol),
		Password:           u.Password,
		FichaID:            u.FichaID,
		ProgramaFormacion:  u.ProgramaFormacion,
		IsActive:           u.IsActive,
		MustChangePassword: u.MustChangePassword,
		CreatedAt:          u.CreatedAt,
		UpdatedAt:          u.UpdatedAt,
		LastLogin:          u.LastLogin,
	}, nil
}

// FromEntity converts domain entity to database model
func (u *UserModel) FromEntity(entity *entities.User) {
	u.ID = entity.ID
	u.Nombre = entity.Nombre
	u.Apellido = entity.Apellido
	u.Email = entity.Email
	u.Documento = entity.Documento
	u.Rol = string(entity.Rol)
	u.Password = entity.Password
	u.FichaID = entity.FichaID
	u.ProgramaFormacion = entity.ProgramaFormacion
	u.IsActive = entity.IsActive
	u.MustChangePassword = entity.MustChangePassword
	u.CreatedAt = entity.CreatedAt
	u.UpdatedAt = entity.UpdatedAt
	u.LastLogin = entity.LastLogin
}

// NewUserModelFromEntity creates a new UserModel from domain entity
func NewUserModelFromEntity(entity *entities.User) *UserModel {
	model := &UserModel{}
	model.FromEntity(entity)
	return model
}
