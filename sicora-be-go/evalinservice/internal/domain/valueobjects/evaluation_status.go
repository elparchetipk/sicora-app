package valueobjects

// EvaluationStatus representa el estado de una evaluación
type EvaluationStatus string

const (
	EvaluationStatusDraft     EvaluationStatus = "DRAFT"     // Borrador, en progreso
	EvaluationStatusSubmitted EvaluationStatus = "SUBMITTED" // Enviada, completa
	EvaluationStatusValidated EvaluationStatus = "VALIDATED" // Validada por administrador
	EvaluationStatusCompleted EvaluationStatus = "COMPLETED" // Completada (alias para submitted)
	EvaluationStatusPending   EvaluationStatus = "PENDING"   // Pendiente
)

// IsValid verifica si el estado de la evaluación es válido
func (es EvaluationStatus) IsValid() bool {
	switch es {
	case EvaluationStatusDraft, EvaluationStatusSubmitted, EvaluationStatusValidated, EvaluationStatusCompleted, EvaluationStatusPending:
		return true
	default:
		return false
	}
}

// String retorna la representación en string del estado
func (es EvaluationStatus) String() string {
	return string(es)
}

// CanBeModified indica si la evaluación puede ser modificada
func (es EvaluationStatus) CanBeModified() bool {
	return es == EvaluationStatusDraft
}

// CanBeSubmitted indica si la evaluación puede ser enviada
func (es EvaluationStatus) CanBeSubmitted() bool {
	return es == EvaluationStatusDraft
}

// CanBeValidated indica si la evaluación puede ser validada
func (es EvaluationStatus) CanBeValidated() bool {
	return es == EvaluationStatusSubmitted
}

// IsComplete indica si la evaluación está completa
func (es EvaluationStatus) IsComplete() bool {
	return es == EvaluationStatusSubmitted || es == EvaluationStatusValidated
}
