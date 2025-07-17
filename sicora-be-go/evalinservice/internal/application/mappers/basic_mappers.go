package mappers

// CommentMapper maneja la conversión entre entidades Comment y DTOs
type CommentMapper struct{}

// NewCommentMapper crea una nueva instancia de CommentMapper
func NewCommentMapper() *CommentMapper {
	return &CommentMapper{}
}

// EvaluationMapper maneja la conversión entre entidades Evaluation y DTOs
type EvaluationMapper struct{}

// NewEvaluationMapper crea una nueva instancia de EvaluationMapper
func NewEvaluationMapper() *EvaluationMapper {
	return &EvaluationMapper{}
}

// ReportMapper maneja la conversión entre entidades Report y DTOs
type ReportMapper struct{}

// NewReportMapper crea una nueva instancia de ReportMapper
func NewReportMapper() *ReportMapper {
	return &ReportMapper{}
}

// ConfigurationMapper maneja la conversión entre entidades Configuration y DTOs
type ConfigurationMapper struct{}

// NewConfigurationMapper crea una nueva instancia de ConfigurationMapper
func NewConfigurationMapper() *ConfigurationMapper {
	return &ConfigurationMapper{}
}

// NotificationMapper maneja la conversión entre entidades Notification y DTOs
type NotificationMapper struct{}

// NewNotificationMapper crea una nueva instancia de NotificationMapper
func NewNotificationMapper() *NotificationMapper {
	return &NotificationMapper{}
}
