package valueobjects

type ReportStatus string

const (
	ReportStatusPending    ReportStatus = "pending"
	ReportStatusGenerating ReportStatus = "generating"
	ReportStatusCompleted  ReportStatus = "completed"
	ReportStatusFailed     ReportStatus = "failed"
)

func (rs ReportStatus) IsValid() bool {
	switch rs {
	case ReportStatusPending, ReportStatusGenerating, ReportStatusCompleted, ReportStatusFailed:
		return true
	default:
		return false
	}
}

func (rs ReportStatus) String() string {
	return string(rs)
}

func GetAllReportStatuses() []ReportStatus {
	return []ReportStatus{
		ReportStatusPending,
		ReportStatusGenerating,
		ReportStatusCompleted,
		ReportStatusFailed,
	}
}
