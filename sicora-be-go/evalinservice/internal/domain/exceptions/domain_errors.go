package exceptions

import "fmt"

// DomainError representa un error del dominio
type DomainError struct {
	Message string
	Code    string
}

func (e *DomainError) Error() string {
	return e.Message
}

// NewDomainError crea un nuevo error de dominio
func NewDomainError(code, message string) *DomainError {
	return &DomainError{
		Code:    code,
		Message: message,
	}
}

// Question-related errors
func NewQuestionNotFoundError(id string) *DomainError {
	return NewDomainError("QUESTION_NOT_FOUND", fmt.Sprintf("Pregunta con ID %s no encontrada", id))
}

func NewInvalidQuestionTypeError(questionType string) *DomainError {
	return NewDomainError("INVALID_QUESTION_TYPE", fmt.Sprintf("Tipo de pregunta inválido: %s", questionType))
}

func NewQuestionInUseError(id string) *DomainError {
	return NewDomainError("QUESTION_IN_USE", fmt.Sprintf("Pregunta con ID %s está siendo utilizada y no puede ser eliminada", id))
}

// Questionnaire-related errors
func NewQuestionnaireNotFoundError(id string) *DomainError {
	return NewDomainError("QUESTIONNAIRE_NOT_FOUND", fmt.Sprintf("Cuestionario con ID %s no encontrado", id))
}

func NewQuestionnaireInUseError(id string) *DomainError {
	return NewDomainError("QUESTIONNAIRE_IN_USE", fmt.Sprintf("Cuestionario con ID %s está siendo utilizado y no puede ser eliminado", id))
}

func NewQuestionAlreadyInQuestionnaireError(questionID, questionnaireID string) *DomainError {
	return NewDomainError("QUESTION_ALREADY_IN_QUESTIONNAIRE",
		fmt.Sprintf("Pregunta %s ya está en el cuestionario %s", questionID, questionnaireID))
}

func NewQuestionNotInQuestionnaireError(questionID, questionnaireID string) *DomainError {
	return NewDomainError("QUESTION_NOT_IN_QUESTIONNAIRE",
		fmt.Sprintf("Pregunta %s no está en el cuestionario %s", questionID, questionnaireID))
}

// Period-related errors
func NewEvaluationPeriodNotFoundError(id string) *DomainError {
	return NewDomainError("EVALUATION_PERIOD_NOT_FOUND", fmt.Sprintf("Período de evaluación con ID %s no encontrado", id))
}

func NewInvalidPeriodDatesError() *DomainError {
	return NewDomainError("INVALID_PERIOD_DATES", "La fecha de inicio debe ser anterior a la fecha de fin")
}

func NewPeriodNotActiveError(id string) *DomainError {
	return NewDomainError("PERIOD_NOT_ACTIVE", fmt.Sprintf("Período de evaluación %s no está activo", id))
}

func NewPeriodCannotBeModifiedError(id string, status string) *DomainError {
	return NewDomainError("PERIOD_CANNOT_BE_MODIFIED",
		fmt.Sprintf("Período %s con estado %s no puede ser modificado", id, status))
}

func NewOverlappingPeriodsError() *DomainError {
	return NewDomainError("OVERLAPPING_PERIODS", "Ya existe un período activo que se superpone con las fechas especificadas")
}

// Evaluation-related errors
func NewEvaluationNotFoundError(id string) *DomainError {
	return NewDomainError("EVALUATION_NOT_FOUND", fmt.Sprintf("Evaluación con ID %s no encontrada", id))
}

func NewEvaluationAlreadyExistsError(studentID, instructorID, periodID string) *DomainError {
	return NewDomainError("EVALUATION_ALREADY_EXISTS",
		fmt.Sprintf("Ya existe una evaluación del estudiante %s al instructor %s en el período %s",
			studentID, instructorID, periodID))
}

func NewInvalidEvaluationResponseError(questionID, response string) *DomainError {
	return NewDomainError("INVALID_EVALUATION_RESPONSE",
		fmt.Sprintf("Respuesta inválida '%s' para la pregunta %s", response, questionID))
}

func NewIncompleteEvaluationError() *DomainError {
	return NewDomainError("INCOMPLETE_EVALUATION", "La evaluación no está completa. Faltan respuestas obligatorias")
}

func NewEvaluationCannotBeModifiedError(id string, status string) *DomainError {
	return NewDomainError("EVALUATION_CANNOT_BE_MODIFIED",
		fmt.Sprintf("Evaluación %s con estado %s no puede ser modificada", id, status))
}

func NewEvaluationAlreadySubmittedError(id string) *DomainError {
	return NewDomainError("EVALUATION_ALREADY_SUBMITTED",
		fmt.Sprintf("Evaluación %s ya ha sido enviada", id))
}

// Authorization errors
func NewUnauthorizedAccessError(action string) *DomainError {
	return NewDomainError("UNAUTHORIZED_ACCESS", fmt.Sprintf("No tiene permisos para %s", action))
}

func NewInvalidUserRoleError(requiredRole, currentRole string) *DomainError {
	return NewDomainError("INVALID_USER_ROLE",
		fmt.Sprintf("Se requiere rol %s, pero el usuario tiene rol %s", requiredRole, currentRole))
}

// External service errors
func NewExternalServiceError(service, operation string, err error) *DomainError {
	return NewDomainError("EXTERNAL_SERVICE_ERROR",
		fmt.Sprintf("Error en servicio externo %s durante %s: %v", service, operation, err))
}

func NewUserNotFoundError(userID string) *DomainError {
	return NewDomainError("USER_NOT_FOUND", fmt.Sprintf("Usuario con ID %s no encontrado", userID))
}

func NewInstructorNotEvaluableError(instructorID, studentID string) *DomainError {
	return NewDomainError("INSTRUCTOR_NOT_EVALUABLE",
		fmt.Sprintf("El instructor %s no puede ser evaluado por el estudiante %s en este período",
			instructorID, studentID))
}

// Validation errors
func NewValidationError(field, message string) *DomainError {
	return NewDomainError("VALIDATION_ERROR", fmt.Sprintf("Error de validación en %s: %s", field, message))
}

func NewRequiredFieldError(field string) *DomainError {
	return NewDomainError("REQUIRED_FIELD", fmt.Sprintf("El campo %s es obligatorio", field))
}

func NewInvalidFormatError(field, format string) *DomainError {
	return NewDomainError("INVALID_FORMAT", fmt.Sprintf("El campo %s debe tener formato %s", field, format))
}
