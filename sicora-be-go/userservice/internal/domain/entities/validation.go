package entities

import (
	"regexp"
	"strings"
)

// DomainError representa un error del dominio
type DomainError struct {
	Message string
}

func (e *DomainError) Error() string {
	return e.Message
}

// NewDomainError crea un nuevo error de dominio
func NewDomainError(message string) *DomainError {
	return &DomainError{Message: message}
}

// validateUserData valida los datos básicos del usuario según reglas de dominio
func validateUserData(nombre, apellido, email, documento string, rol UserRole) error {
	if err := validateNombre(nombre); err != nil {
		return err
	}

	if err := validateApellido(apellido); err != nil {
		return err
	}

	if err := validateEmail(email); err != nil {
		return err
	}

	if err := validateDocumento(documento); err != nil {
		return err
	}

	if err := validateRol(rol); err != nil {
		return err
	}

	return nil
}

// validateNombre valida el nombre del usuario
func validateNombre(nombre string) error {
	nombre = strings.TrimSpace(nombre)
	if len(nombre) < 2 {
		return NewDomainError("el nombre debe tener al menos 2 caracteres")
	}
	if len(nombre) > 50 {
		return NewDomainError("el nombre no puede exceder 50 caracteres")
	}

	// Solo letras, espacios y acentos
	matched, _ := regexp.MatchString(`^[a-zA-ZáéíóúüñÁÉÍÓÚÜÑ\s]+$`, nombre)
	if !matched {
		return NewDomainError("el nombre solo puede contener letras y espacios")
	}

	return nil
}

// validateApellido valida el apellido del usuario
func validateApellido(apellido string) error {
	apellido = strings.TrimSpace(apellido)
	if len(apellido) < 2 {
		return NewDomainError("el apellido debe tener al menos 2 caracteres")
	}
	if len(apellido) > 50 {
		return NewDomainError("el apellido no puede exceder 50 caracteres")
	}

	// Solo letras, espacios y acentos
	matched, _ := regexp.MatchString(`^[a-zA-ZáéíóúüñÁÉÍÓÚÜÑ\s]+$`, apellido)
	if !matched {
		return NewDomainError("el apellido solo puede contener letras y espacios")
	}

	return nil
}

// validateEmail valida el formato del email
func validateEmail(email string) error {
	email = strings.TrimSpace(strings.ToLower(email))
	if len(email) == 0 {
		return NewDomainError("el email es obligatorio")
	}
	if len(email) > 100 {
		return NewDomainError("el email no puede exceder 100 caracteres")
	}

	// Validación básica de email
	emailRegex := `^[a-z0-9._%+\-]+@[a-z0-9.\-]+\.[a-z]{2,}$`
	matched, _ := regexp.MatchString(emailRegex, email)
	if !matched {
		return NewDomainError("formato de email inválido")
	}

	// Validación específica para SENA
	if !strings.HasSuffix(email, "@sena.edu.co") && !strings.HasSuffix(email, "@misena.edu.co") {
		return NewDomainError("el email debe ser del dominio SENA (@sena.edu.co o @misena.edu.co)")
	}

	return nil
}

// validateDocumento valida el número de documento
func validateDocumento(documento string) error {
	documento = strings.TrimSpace(documento)
	if len(documento) < 7 {
		return NewDomainError("el documento debe tener al menos 7 dígitos")
	}
	if len(documento) > 15 {
		return NewDomainError("el documento no puede exceder 15 dígitos")
	}

	// Solo números
	matched, _ := regexp.MatchString(`^[0-9]+$`, documento)
	if !matched {
		return NewDomainError("el documento solo puede contener números")
	}

	return nil
}

// validateRol valida que el rol sea válido
func validateRol(rol UserRole) error {
	switch rol {
	case RoleAprendiz, RoleInstructor, RoleAdmin, RoleCoordinador:
		return nil
	default:
		return NewDomainError("rol inválido: debe ser aprendiz, instructor, admin o coordinador")
	}
}

// ValidateFichaID valida el formato de ID de ficha
func ValidateFichaID(fichaID string) error {
	if len(fichaID) == 0 {
		return NewDomainError("el ID de ficha es obligatorio")
	}

	// Las fichas en SENA tienen formato numérico de 7 dígitos
	matched, _ := regexp.MatchString(`^[0-9]{7}$`, fichaID)
	if !matched {
		return NewDomainError("el ID de ficha debe tener exactamente 7 dígitos numéricos")
	}

	return nil
}

// ValidatePassword valida que la contraseña cumpla las políticas
func ValidatePassword(password string) error {
	if len(password) < 10 {
		return NewDomainError("la contraseña debe tener al menos 10 caracteres")
	}

	if len(password) > 128 {
		return NewDomainError("la contraseña no puede exceder 128 caracteres")
	}

	// Al menos una minúscula
	if matched, _ := regexp.MatchString(`[a-z]`, password); !matched {
		return NewDomainError("la contraseña debe contener al menos una letra minúscula")
	}

	// Al menos una mayúscula
	if matched, _ := regexp.MatchString(`[A-Z]`, password); !matched {
		return NewDomainError("la contraseña debe contener al menos una letra mayúscula")
	}

	// Al menos un número
	if matched, _ := regexp.MatchString(`[0-9]`, password); !matched {
		return NewDomainError("la contraseña debe contener al menos un número")
	}

	// Al menos un carácter especial
	if matched, _ := regexp.MatchString(`[@$!%*?&]`, password); !matched {
		return NewDomainError("la contraseña debe contener al menos un carácter especial (@$!%*?&)")
	}

	return nil
}

// ValidateUserRole valida que el rol sea válido
func ValidateUserRole(rol UserRole) error {
	return validateRol(rol)
}
