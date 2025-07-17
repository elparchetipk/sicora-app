package middleware

import (
	"net/http"
	"reflect"
	"strings"

	"github.com/gin-gonic/gin"
	"github.com/go-playground/validator/v10"
)

// ValidationMiddleware maneja la validación de datos de entrada
type ValidationMiddleware struct {
	validator *validator.Validate
}

// ValidationError representa un error de validación estructurado
type ValidationError struct {
	Field   string `json:"field"`
	Tag     string `json:"tag"`
	Value   string `json:"value"`
	Message string `json:"message"`
}

// ValidationResponse representa la respuesta de errores de validación
type ValidationResponse struct {
	Error   string            `json:"error"`
	Message string            `json:"message"`
	Errors  []ValidationError `json:"validation_errors"`
}

// NewValidationMiddleware crea un nuevo middleware de validación
func NewValidationMiddleware() *ValidationMiddleware {
	v := validator.New()

	// Registrar validaciones personalizadas
	v.RegisterValidation("uuid", validateUUID)
	v.RegisterValidation("role", validateRole)
	v.RegisterValidation("status", validateStatus)

	// Usar nombres de campo JSON en lugar de nombres de struct
	v.RegisterTagNameFunc(func(fld reflect.StructField) string {
		name := strings.SplitN(fld.Tag.Get("json"), ",", 2)[0]
		if name == "-" {
			return ""
		}
		return name
	})

	return &ValidationMiddleware{
		validator: v,
	}
}

// ValidateJSON middleware que valida el JSON de entrada
func (m *ValidationMiddleware) ValidateJSON(model interface{}) gin.HandlerFunc {
	return func(c *gin.Context) {
		// Crear una nueva instancia del modelo
		modelType := reflect.TypeOf(model)
		if modelType.Kind() == reflect.Ptr {
			modelType = modelType.Elem()
		}

		newModel := reflect.New(modelType).Interface()

		// Bind del JSON
		if err := c.ShouldBindJSON(newModel); err != nil {
			c.JSON(http.StatusBadRequest, gin.H{
				"error":   "Invalid JSON format",
				"message": err.Error(),
			})
			c.Abort()
			return
		}

		// Validar el modelo
		if err := m.validator.Struct(newModel); err != nil {
			validationErrors := m.formatValidationErrors(err)
			c.JSON(http.StatusBadRequest, ValidationResponse{
				Error:   "Validation failed",
				Message: "The request data is invalid",
				Errors:  validationErrors,
			})
			c.Abort()
			return
		}

		// Agregar el modelo validado al contexto
		c.Set("validated_data", newModel)
		c.Next()
	}
}

// ValidateQuery middleware que valida los parámetros de query
func (m *ValidationMiddleware) ValidateQuery(model interface{}) gin.HandlerFunc {
	return func(c *gin.Context) {
		// Crear una nueva instancia del modelo
		modelType := reflect.TypeOf(model)
		if modelType.Kind() == reflect.Ptr {
			modelType = modelType.Elem()
		}

		newModel := reflect.New(modelType).Interface()

		// Bind de los query parameters
		if err := c.ShouldBindQuery(newModel); err != nil {
			c.JSON(http.StatusBadRequest, gin.H{
				"error":   "Invalid query parameters",
				"message": err.Error(),
			})
			c.Abort()
			return
		}

		// Validar el modelo
		if err := m.validator.Struct(newModel); err != nil {
			validationErrors := m.formatValidationErrors(err)
			c.JSON(http.StatusBadRequest, ValidationResponse{
				Error:   "Validation failed",
				Message: "The query parameters are invalid",
				Errors:  validationErrors,
			})
			c.Abort()
			return
		}

		// Agregar el modelo validado al contexto
		c.Set("validated_query", newModel)
		c.Next()
	}
}

// formatValidationErrors formatea los errores de validación para respuesta JSON
func (m *ValidationMiddleware) formatValidationErrors(err error) []ValidationError {
	var validationErrors []ValidationError

	if validationErrs, ok := err.(validator.ValidationErrors); ok {
		for _, validationErr := range validationErrs {
			validationErrors = append(validationErrors, ValidationError{
				Field:   validationErr.Field(),
				Tag:     validationErr.Tag(),
				Value:   validationErr.Param(),
				Message: m.getErrorMessage(validationErr),
			})
		}
	}

	return validationErrors
}

// getErrorMessage genera mensajes de error amigables para el usuario
func (m *ValidationMiddleware) getErrorMessage(err validator.FieldError) string {
	switch err.Tag() {
	case "required":
		return "This field is required"
	case "email":
		return "Must be a valid email address"
	case "min":
		return "Must be at least " + err.Param() + " characters long"
	case "max":
		return "Must be at most " + err.Param() + " characters long"
	case "uuid":
		return "Must be a valid UUID"
	case "role":
		return "Must be a valid role (admin, instructor, student)"
	case "status":
		return "Must be a valid status"
	case "gte":
		return "Must be greater than or equal to " + err.Param()
	case "lte":
		return "Must be less than or equal to " + err.Param()
	case "oneof":
		return "Must be one of: " + err.Param()
	default:
		return "Invalid value"
	}
}

// Validaciones personalizadas

// validateUUID valida que el campo sea un UUID válido
func validateUUID(fl validator.FieldLevel) bool {
	value := fl.Field().String()
	if value == "" {
		return true // Permitir valores vacíos, usar 'required' para campos obligatorios
	}

	// Validar formato UUID básico
	return len(value) == 36 && strings.Count(value, "-") == 4
}

// validateRole valida que el rol sea válido
func validateRole(fl validator.FieldLevel) bool {
	role := fl.Field().String()
	validRoles := []string{"admin", "instructor", "student"}

	for _, validRole := range validRoles {
		if role == validRole {
			return true
		}
	}

	return false
}

// validateStatus valida que el estado sea válido
func validateStatus(fl validator.FieldLevel) bool {
	status := fl.Field().String()
	validStatuses := []string{"ACTIVE", "INACTIVE", "PENDING", "COMPLETED", "CANCELLED"}

	for _, validStatus := range validStatuses {
		if status == validStatus {
			return true
		}
	}

	return false
}

// GetValidatedData obtiene los datos validados del contexto
func GetValidatedData(c *gin.Context) (interface{}, bool) {
	data, exists := c.Get("validated_data")
	return data, exists
}

// GetValidatedQuery obtiene los parámetros de query validados del contexto
func GetValidatedQuery(c *gin.Context) (interface{}, bool) {
	query, exists := c.Get("validated_query")
	return query, exists
}
