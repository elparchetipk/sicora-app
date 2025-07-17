package entities

import (
	"testing"

	"userservice/internal/domain/entities"
	"userservice/tests/fixtures"

	"github.com/stretchr/testify/assert"
)

func TestUser_NewUser(t *testing.T) {
	t.Run("create valid user", func(t *testing.T) {
		// Arrange
		nombre := "Juan"
		apellido := "Perez"
		email := "juan.perez@sena.edu.co"
		documento := "12345678"
		rol := entities.RoleAprendiz
		programa := "Análisis y Desarrollo de Software"

		// Act
		user, err := entities.NewUser(nombre, apellido, email, documento, rol, programa)

		// Assert
		assert.NoError(t, err)
		assert.NotNil(t, user)
		assert.Equal(t, nombre, user.Nombre)
		assert.Equal(t, apellido, user.Apellido)
		assert.Equal(t, email, user.Email)
		assert.Equal(t, documento, user.Documento)
		assert.Equal(t, rol, user.Rol)
		assert.Equal(t, programa, user.ProgramaFormacion)
		assert.True(t, user.IsActive)
		assert.False(t, user.MustChangePassword)
		assert.NotEqual(t, "", user.ID.String())
	})

	t.Run("create user with empty nombre fails", func(t *testing.T) {
		// Arrange
		nombre := ""
		apellido := "Perez"
		email := "juan.perez@sena.edu.co"
		documento := "12345678"
		rol := entities.RoleAprendiz
		programa := "Análisis y Desarrollo de Software"

		// Act
		user, err := entities.NewUser(nombre, apellido, email, documento, rol, programa)

		// Assert
		assert.Error(t, err)
		assert.Nil(t, user)
		assert.Contains(t, err.Error(), "nombre")
	})

	t.Run("create user with invalid email fails", func(t *testing.T) {
		// Arrange
		nombre := "Juan"
		apellido := "Perez"
		email := "invalid-email"
		documento := "12345678"
		rol := entities.RoleAprendiz
		programa := "Análisis y Desarrollo de Software"

		// Act
		user, err := entities.NewUser(nombre, apellido, email, documento, rol, programa)

		// Assert
		assert.Error(t, err)
		assert.Nil(t, user)
		assert.Contains(t, err.Error(), "email")
	})

	t.Run("create user with invalid role fails", func(t *testing.T) {
		// Arrange
		nombre := "Juan"
		apellido := "Perez"
		email := "juan.perez@sena.edu.co"
		documento := "12345678"
		rol := entities.UserRole("invalid_role")
		programa := "Análisis y Desarrollo de Software"

		// Act
		user, err := entities.NewUser(nombre, apellido, email, documento, rol, programa)

		// Assert
		assert.Error(t, err)
		assert.Nil(t, user)
		assert.Contains(t, err.Error(), "rol")
	})
}

func TestUser_GetFullName(t *testing.T) {
	t.Run("get full name", func(t *testing.T) {
		// Arrange
		user := fixtures.NewValidUser()
		expected := user.Nombre + " " + user.Apellido

		// Act
		fullName := user.GetFullName()

		// Assert
		assert.Equal(t, expected, fullName)
	})
}

func TestUser_Activate(t *testing.T) {
	t.Run("activate user", func(t *testing.T) {
		// Arrange
		user := fixtures.NewValidUser()
		user.IsActive = false

		// Act
		user.Activate()

		// Assert
		assert.True(t, user.IsActive)
	})
}

func TestUser_Deactivate(t *testing.T) {
	t.Run("deactivate user", func(t *testing.T) {
		// Arrange
		user := fixtures.NewValidUser()
		user.IsActive = true

		// Act
		user.Deactivate()

		// Assert
		assert.False(t, user.IsActive)
	})
}

func TestUser_SetPassword(t *testing.T) {
	t.Run("set password successfully", func(t *testing.T) {
		// Arrange
		user := fixtures.NewValidUser()
		newPassword := "NewPassword123!"

		// Act
		err := user.SetPassword(newPassword)

		// Assert
		assert.NoError(t, err)
		assert.NotEqual(t, newPassword, user.Password) // Should be hashed
		assert.NotEmpty(t, user.Password)
	})

	t.Run("set empty password fails", func(t *testing.T) {
		// Arrange
		user := fixtures.NewValidUser()
		newPassword := ""

		// Act
		err := user.SetPassword(newPassword)

		// Assert
		assert.Error(t, err)
		assert.Contains(t, err.Error(), "password")
	})
}

func TestUser_CheckPassword(t *testing.T) {
	t.Run("check correct password", func(t *testing.T) {
		// Arrange
		user := fixtures.NewValidUser()
		password := "Password123!"
		user.SetPassword(password)

		// Act
		isValid := user.CheckPassword(password)

		// Assert
		assert.True(t, isValid)
	})

	t.Run("check incorrect password", func(t *testing.T) {
		// Arrange
		user := fixtures.NewValidUser()
		correctPassword := "Password123!"
		wrongPassword := "WrongPassword123!"
		user.SetPassword(correctPassword)

		// Act
		isValid := user.CheckPassword(wrongPassword)

		// Assert
		assert.False(t, isValid)
	})
}

func TestUser_IsAprendiz(t *testing.T) {
	t.Run("user is aprendiz", func(t *testing.T) {
		// Arrange
		user := fixtures.NewValidUser()
		user.Rol = entities.RoleAprendiz

		// Act & Assert
		assert.True(t, user.IsAprendiz())
		assert.False(t, user.IsInstructor())
		assert.False(t, user.IsAdmin())
		assert.False(t, user.IsCoordinador())
	})
}

func TestUser_IsInstructor(t *testing.T) {
	t.Run("user is instructor", func(t *testing.T) {
		// Arrange
		user := fixtures.NewValidInstructor()
		user.Rol = entities.RoleInstructor

		// Act & Assert
		assert.False(t, user.IsAprendiz())
		assert.True(t, user.IsInstructor())
		assert.False(t, user.IsAdmin())
		assert.False(t, user.IsCoordinador())
	})
}

func TestUser_IsAdmin(t *testing.T) {
	t.Run("user is admin", func(t *testing.T) {
		// Arrange
		user := fixtures.NewValidAdmin()
		user.Rol = entities.RoleAdmin

		// Act & Assert
		assert.False(t, user.IsAprendiz())
		assert.False(t, user.IsInstructor())
		assert.True(t, user.IsAdmin())
		assert.False(t, user.IsCoordinador())
	})
}

func TestUser_CanManageUsers(t *testing.T) {
	t.Run("admin can manage users", func(t *testing.T) {
		// Arrange
		user := fixtures.NewValidAdmin()

		// Act & Assert
		assert.True(t, user.CanManageUsers())
	})

	t.Run("coordinador can manage users", func(t *testing.T) {
		// Arrange
		user := fixtures.NewValidUser()
		user.Rol = entities.RoleCoordinador

		// Act & Assert
		assert.True(t, user.CanManageUsers())
	})

	t.Run("instructor cannot manage users", func(t *testing.T) {
		// Arrange
		user := fixtures.NewValidInstructor()

		// Act & Assert
		assert.False(t, user.CanManageUsers())
	})

	t.Run("aprendiz cannot manage users", func(t *testing.T) {
		// Arrange
		user := fixtures.NewValidUser()

		// Act & Assert
		assert.False(t, user.CanManageUsers())
	})
}

func TestUserRole_IsValid(t *testing.T) {
	validRoles := []entities.UserRole{
		entities.RoleAprendiz,
		entities.RoleInstructor,
		entities.RoleAdmin,
		entities.RoleCoordinador,
	}

	for _, role := range validRoles {
		t.Run("valid role: "+string(role), func(t *testing.T) {
			assert.True(t, role.IsValid())
		})
	}

	t.Run("invalid role", func(t *testing.T) {
		invalidRole := entities.UserRole("invalid_role")
		assert.False(t, invalidRole.IsValid())
	})
}
