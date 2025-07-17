package entities

import "fmt"

// ValidationError representa un error de validación de entidad
type ValidationError struct {
	Field   string `json:"field"`
	Message string `json:"message"`
}

func (e *ValidationError) Error() string {
	return fmt.Sprintf("validation error on field '%s': %s", e.Field, e.Message)
}

// BusinessRuleError representa un error de regla de negocio
type BusinessRuleError struct {
	Rule    string `json:"rule"`
	Message string `json:"message"`
}

func (e *BusinessRuleError) Error() string {
	return fmt.Sprintf("business rule violation '%s': %s", e.Rule, e.Message)
}

// NotFoundError representa un error cuando una entidad no es encontrada
type NotFoundError struct {
	Entity string `json:"entity"`
	ID     string `json:"id"`
}

func (e *NotFoundError) Error() string {
	return fmt.Sprintf("%s with id '%s' not found", e.Entity, e.ID)
}

// ConflictError representa un error de conflicto (duplicados, etc.)
type ConflictError struct {
	Resource string `json:"resource"`
	Message  string `json:"message"`
}

func (e *ConflictError) Error() string {
	return fmt.Sprintf("conflict on resource '%s': %s", e.Resource, e.Message)
}

// Constructor functions for easier error creation

// NewValidationError creates a new validation error
func NewValidationError(field string, err error) *ValidationError {
	message := "validation failed"
	if err != nil {
		message = err.Error()
	}
	return &ValidationError{
		Field:   field,
		Message: message,
	}
}

// NewBusinessRuleError creates a new business rule error
func NewBusinessRuleError(message string) *BusinessRuleError {
	return &BusinessRuleError{
		Rule:    "business_rule",
		Message: message,
	}
}

// NewNotFoundError creates a new not found error
func NewNotFoundError(entity, id string) *NotFoundError {
	return &NotFoundError{
		Entity: entity,
		ID:     id,
	}
}

// NewConflictError creates a new conflict error
func NewConflictError(resource, message string) *ConflictError {
	return &ConflictError{
		Resource: resource,
		Message:  message,
	}
}
