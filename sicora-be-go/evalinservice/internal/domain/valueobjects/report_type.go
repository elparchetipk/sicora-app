package valueobjects

type ReportType string

const (
	ReportTypeInstructorPerformance ReportType = "instructor_performance"
	ReportTypePeriodSummary         ReportType = "period_summary"
	ReportTypeComparative           ReportType = "comparative"
	ReportTypeDetailed              ReportType = "detailed"
	ReportTypeExecutive             ReportType = "executive"
)

func (rt ReportType) IsValid() bool {
	switch rt {
	case ReportTypeInstructorPerformance, ReportTypePeriodSummary, ReportTypeComparative, ReportTypeDetailed, ReportTypeExecutive:
		return true
	default:
		return false
	}
}

func (rt ReportType) String() string {
	return string(rt)
}

func GetAllReportTypes() []ReportType {
	return []ReportType{
		ReportTypeInstructorPerformance,
		ReportTypePeriodSummary,
		ReportTypeComparative,
		ReportTypeDetailed,
		ReportTypeExecutive,
	}
}
