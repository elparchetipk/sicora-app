package valueobjects

type NotificationType string

const (
	NotificationTypeEvaluationCreated   NotificationType = "evaluation_created"
	NotificationTypeEvaluationUpdated   NotificationType = "evaluation_updated"
	NotificationTypeEvaluationCompleted NotificationType = "evaluation_completed"
	NotificationTypePeriodStarted       NotificationType = "period_started"
	NotificationTypePeriodEnded         NotificationType = "period_ended"
	NotificationTypeReportGenerated     NotificationType = "report_generated"
	NotificationTypeCommentAdded        NotificationType = "comment_added"
)

func (nt NotificationType) IsValid() bool {
	switch nt {
	case NotificationTypeEvaluationCreated, NotificationTypeEvaluationUpdated, NotificationTypeEvaluationCompleted,
		NotificationTypePeriodStarted, NotificationTypePeriodEnded, NotificationTypeReportGenerated,
		NotificationTypeCommentAdded:
		return true
	default:
		return false
	}
}

func (nt NotificationType) String() string {
	return string(nt)
}

func GetAllNotificationTypes() []NotificationType {
	return []NotificationType{
		NotificationTypeEvaluationCreated,
		NotificationTypeEvaluationUpdated,
		NotificationTypeEvaluationCompleted,
		NotificationTypePeriodStarted,
		NotificationTypePeriodEnded,
		NotificationTypeReportGenerated,
		NotificationTypeCommentAdded,
	}
}
