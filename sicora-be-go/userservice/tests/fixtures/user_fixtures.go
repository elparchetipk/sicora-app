package fixtures

import (
	"fmt"
	"time"

	"userservice/internal/application/dtos"
	"userservice/internal/domain/entities"

	"github.com/google/uuid"
)

// NewValidUser crea un usuario válido para testing
func NewValidUser() *entities.User {
	return &entities.User{
		ID:                uuid.New(),
		Nombre:            "Juan",
		Apellido:          "Perez",
		Email:             "juan.perez@sena.edu.co",
		Password:          "$2a$10$92IXUNpkjO0rOQ5byMi.Ye4oKoEa3Ro9llC/.og/at2.uheWG/igi", // password
		Documento:         "12345678",
		Rol:               entities.RoleAprendiz,
		FichaID:           StringPtr("FIC001"),
		ProgramaFormacion: "Análisis y Desarrollo de Software",
		IsActive:          true,
		CreatedAt:         time.Now(),
		UpdatedAt:         time.Now(),
	}
}

// NewValidInstructor crea un instructor válido para testing
func NewValidInstructor() *entities.User {
	return &entities.User{
		ID:                uuid.New(),
		Nombre:            "Maria",
		Apellido:          "Garcia",
		Email:             "maria.garcia@sena.edu.co",
		Password:          "$2a$10$92IXUNpkjO0rOQ5byMi.Ye4oKoEa3Ro9llC/.og/at2.uheWG/igi", // password
		Documento:         "87654321",
		Rol:               entities.RoleInstructor,
		ProgramaFormacion: "Sistemas de Información",
		IsActive:          true,
		CreatedAt:         time.Now(),
		UpdatedAt:         time.Now(),
	}
}

// NewValidAdmin crea un admin válido para testing
func NewValidAdmin() *entities.User {
	return &entities.User{
		ID:                uuid.New(),
		Nombre:            "Admin",
		Apellido:          "Sistema",
		Email:             "admin@sena.edu.co",
		Password:          "$2a$10$92IXUNpkjO0rOQ5byMi.Ye4oKoEa3Ro9llC/.og/at2.uheWG/igi", // password
		Documento:         "00000000",
		Rol:               entities.RoleAdmin,
		ProgramaFormacion: "Administración",
		IsActive:          true,
		CreatedAt:         time.Now(),
		UpdatedAt:         time.Now(),
	}
}

// NewCreateUserRequest crea una solicitud de creación de usuario válida
func NewCreateUserRequest() *dtos.CreateUserRequest {
	return &dtos.CreateUserRequest{
		Nombre:            "Carlos",
		Apellido:          "Rodriguez",
		Email:             "carlos.rodriguez@sena.edu.co",
		Password:          "Password123!",
		Documento:         "11111111",
		Rol:               "aprendiz",
		FichaID:           StringPtr("FIC002"),
		ProgramaFormacion: "Desarrollo de Software",
	}
}

// NewBulkCreateUserRequest crea una solicitud bulk válida
func NewBulkCreateUserRequest() *dtos.BulkCreateUserRequest {
	return &dtos.BulkCreateUserRequest{
		Users: []dtos.CreateUserRequest{
			{
				Nombre:            "Test1",
				Apellido:          "User1",
				Email:             "test1@sena.edu.co",
				Password:          "Password123!",
				Documento:         "20000001",
				Rol:               "aprendiz",
				FichaID:           StringPtr("FIC001"),
				ProgramaFormacion: "Test Program",
			},
			{
				Nombre:            "Test2",
				Apellido:          "User2",
				Email:             "test2@sena.edu.co",
				Password:          "Password123!",
				Documento:         "20000002",
				Rol:               "aprendiz",
				FichaID:           StringPtr("FIC001"),
				ProgramaFormacion: "Test Program",
			},
		},
	}
}

// NewUpdateUserRequest crea una solicitud de actualización válida
func NewUpdateUserRequest() *dtos.UpdateUserRequestDTO {
	return &dtos.UpdateUserRequestDTO{
		Nombre:            "Carlos Updated",
		Apellido:          "Rodriguez Updated",
		Documento:         "11111112",
		FichaID:           StringPtr("FIC003"),
		ProgramaFormacion: "Software Avanzado",
	}
}

// NewBulkUpdateUserRequest crea una solicitud de actualización masiva válida
func NewBulkUpdateUserRequest() *dtos.BulkUpdateUserRequest {
	return &dtos.BulkUpdateUserRequest{
		Users: []dtos.BulkUpdateUserItem{
			{
				Email:             "test1@sena.edu.co",
				Nombre:            StringPtr("Updated Test1"),
				ProgramaFormacion: StringPtr("Updated Program"),
			},
			{
				Email:    "test2@sena.edu.co",
				IsActive: BoolPtr(false),
			},
		},
	}
}

// NewBulkDeleteRequest crea una solicitud de eliminación masiva válida
func NewBulkDeleteRequest() *dtos.BulkDeleteRequest {
	return &dtos.BulkDeleteRequest{
		Emails: []string{
			"test1@sena.edu.co",
			"test2@sena.edu.co",
		},
	}
}

// NewBulkStatusRequest crea una solicitud de cambio de estado masivo válida
func NewBulkStatusRequest(isActive bool) *dtos.BulkStatusRequest {
	return &dtos.BulkStatusRequest{
		Emails: []string{
			"test1@sena.edu.co",
			"test2@sena.edu.co",
		},
		IsActive: isActive,
	}
}

// NewUsersList crea una lista de usuarios para testing
func NewUsersList(count int) []*entities.User {
	users := make([]*entities.User, count)
	for i := 0; i < count; i++ {
		user := NewValidUser()
		user.Email = fmt.Sprintf("user%d@sena.edu.co", i+1)
		user.Documento = fmt.Sprintf("1000000%d", i+1)
		users[i] = user
	}
	return users
}

// StringPtr returns a pointer to string
func StringPtr(s string) *string {
	return &s
}

// BoolPtr returns a pointer to bool
func BoolPtr(b bool) *bool {
	return &b
}

// IntPtr returns a pointer to int
func IntPtr(i int) *int {
	return &i
}
