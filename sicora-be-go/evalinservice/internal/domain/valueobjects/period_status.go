package valueobjects

// PeriodStatus representa el estado de un período de evaluación
type PeriodStatus string

const (
	PeriodStatusDraft  PeriodStatus = "DRAFT"  // Borrador, en preparación
	PeriodStatusActive PeriodStatus = "ACTIVE" // Activo, acepta evaluaciones
	PeriodStatusClosed PeriodStatus = "CLOSED" // Cerrado, no acepta más evaluaciones
)

// IsValid verifica si el estado del período es válido
func (ps PeriodStatus) IsValid() bool {
	switch ps {
	case PeriodStatusDraft, PeriodStatusActive, PeriodStatusClosed:
		return true
	default:
		return false
	}
}

// String retorna la representación en string del estado
func (ps PeriodStatus) String() string {
	return string(ps)
}

// CanAcceptEvaluations indica si el período puede aceptar evaluaciones
func (ps PeriodStatus) CanAcceptEvaluations() bool {
	return ps == PeriodStatusActive
}

// CanBeModified indica si el período puede ser modificado
func (ps PeriodStatus) CanBeModified() bool {
	return ps == PeriodStatusDraft
}

// CanBeActivated indica si el período puede ser activado
func (ps PeriodStatus) CanBeActivated() bool {
	return ps == PeriodStatusDraft
}

// CanBeClosed indica si el período puede ser cerrado
func (ps PeriodStatus) CanBeClosed() bool {
	return ps == PeriodStatusActive
}
