package valueobjects

// QuestionType representa los tipos de preguntas disponibles
type QuestionType string

const (
	QuestionTypeLikert         QuestionType = "LIKERT"          // Escala 1-5
	QuestionTypeText           QuestionType = "TEXT"            // Respuesta libre
	QuestionTypeMultipleChoice QuestionType = "MULTIPLE_CHOICE" // Selección múltiple
	QuestionTypeSingleChoice   QuestionType = "SINGLE_CHOICE"   // Selección única
	QuestionTypeBoolean        QuestionType = "BOOLEAN"         // Sí/No
)

// IsValid verifica si el tipo de pregunta es válido
func (qt QuestionType) IsValid() bool {
	switch qt {
	case QuestionTypeLikert, QuestionTypeText, QuestionTypeMultipleChoice, QuestionTypeSingleChoice, QuestionTypeBoolean:
		return true
	default:
		return false
	}
}

// String retorna la representación en string del tipo de pregunta
func (qt QuestionType) String() string {
	return string(qt)
}

// GetValidOptions retorna las opciones válidas para el tipo de pregunta
func (qt QuestionType) GetValidOptions() []string {
	switch qt {
	case QuestionTypeLikert:
		return []string{"1", "2", "3", "4", "5"}
	case QuestionTypeBoolean:
		return []string{"true", "false"}
	case QuestionTypeMultipleChoice, QuestionTypeSingleChoice:
		// Se definen en la pregunta específica
		return nil
	case QuestionTypeText:
		// Respuesta libre
		return nil
	default:
		return nil
	}
}

// RequiresOptions indica si el tipo de pregunta requiere opciones predefinidas
func (qt QuestionType) RequiresOptions() bool {
	return qt == QuestionTypeMultipleChoice || qt == QuestionTypeSingleChoice
}

// AllowsMultipleAnswers indica si el tipo permite múltiples respuestas
func (qt QuestionType) AllowsMultipleAnswers() bool {
	return qt == QuestionTypeMultipleChoice
}
