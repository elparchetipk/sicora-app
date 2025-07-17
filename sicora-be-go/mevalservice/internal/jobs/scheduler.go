package jobs

import (
	"context"
	"fmt"
	"log"
	"time"

	"github.com/robfig/cron/v3"

	"mevalservice/internal/application/usecases"
	"mevalservice/internal/domain/entities"
	"mevalservice/internal/domain/repositories"
)

// JobScheduler handles automatic jobs for MEvalService
type JobScheduler struct {
	cron                   *cron.Cron
	committeeUC            usecases.CommitteeUseCases
	studentCaseUC          usecases.StudentCaseUseCases
	improvementPlanUC      usecases.ImprovementPlanUseCases
	sanctionUC             usecases.SanctionUseCases
	appealUC               usecases.AppealUseCases
	committeeRepo          repositories.CommitteeRepository
	studentCaseRepo        repositories.StudentCaseRepository
	improvementPlanRepo    repositories.ImprovementPlanRepository
	sanctionRepo           repositories.SanctionRepository
	appealRepo             repositories.AppealRepository
	notificationService    NotificationService
}

// NotificationService interface for sending notifications
type NotificationService interface {
	SendEmail(to []string, subject, body string) error
	SendAlert(message string, priority string) error
}

// NewJobScheduler creates a new job scheduler
func NewJobScheduler(
	committeeUC usecases.CommitteeUseCases,
	studentCaseUC usecases.StudentCaseUseCases,
	improvementPlanUC usecases.ImprovementPlanUseCases,
	sanctionUC usecases.SanctionUseCases,
	appealUC usecases.AppealUseCases,
	committeeRepo repositories.CommitteeRepository,
	studentCaseRepo repositories.StudentCaseRepository,
	improvementPlanRepo repositories.ImprovementPlanRepository,
	sanctionRepo repositories.SanctionRepository,
	appealRepo repositories.AppealRepository,
	notificationService NotificationService,
) *JobScheduler {
	return &JobScheduler{
		cron:                   cron.New(cron.WithLocation(time.UTC)),
		committeeUC:            committeeUC,
		studentCaseUC:          studentCaseUC,
		improvementPlanUC:      improvementPlanUC,
		sanctionUC:             sanctionUC,
		appealUC:               appealUC,
		committeeRepo:          committeeRepo,
		studentCaseRepo:        studentCaseRepo,
		improvementPlanRepo:    improvementPlanRepo,
		sanctionRepo:           sanctionRepo,
		appealRepo:             appealRepo,
		notificationService:    notificationService,
	}
}

// Start begins the job scheduler
func (js *JobScheduler) Start() error {
	// Monthly committee creation - First Monday of each month at 09:00
	_, err := js.cron.AddFunc("0 9 1-7 * 1", js.createMonthlyCommittees)
	if err != nil {
		return fmt.Errorf("failed to schedule monthly committee creation: %w", err)
	}

	// Daily overdue case alerts - Every day at 08:00
	_, err = js.cron.AddFunc("0 8 * * *", js.checkOverdueCases)
	if err != nil {
		return fmt.Errorf("failed to schedule overdue case alerts: %w", err)
	}

	// Weekly improvement plan progress check - Every Monday at 10:00
	_, err = js.cron.AddFunc("0 10 * * 1", js.checkImprovementPlanProgress)
	if err != nil {
		return fmt.Errorf("failed to schedule improvement plan progress check: %w", err)
	}

	// Daily sanction expiration check - Every day at 07:00
	_, err = js.cron.AddFunc("0 7 * * *", js.checkSanctionExpirations)
	if err != nil {
		return fmt.Errorf("failed to schedule sanction expiration check: %w", err)
	}

	// Daily appeal deadline alerts - Every day at 09:00
	_, err = js.cron.AddFunc("0 9 * * *", js.checkAppealDeadlines)
	if err != nil {
		return fmt.Errorf("failed to schedule appeal deadline check: %w", err)
	}

	// Monthly committee performance report - Last day of month at 17:00
	_, err = js.cron.AddFunc("0 17 28-31 * *", js.generateMonthlyReports)
	if err != nil {
		return fmt.Errorf("failed to schedule monthly reports: %w", err)
	}

	js.cron.Start()
	log.Println("Job scheduler started successfully")
	return nil
}

// Stop stops the job scheduler
func (js *JobScheduler) Stop() {
	js.cron.Stop()
	log.Println("Job scheduler stopped")
}

// createMonthlyCommittees creates monthly committees for each center
func (js *JobScheduler) createMonthlyCommittees() {
	ctx := context.Background()
	currentDate := time.Now()
	
	log.Printf("Creating monthly committees for %s %d", currentDate.Month(), currentDate.Year())

	// Get all existing committees to identify centers
	committees, err := js.committeeRepo.GetAll(ctx)
	if err != nil {
		log.Printf("Error getting committees for monthly creation: %v", err)
		return
	}

	centers := make(map[string]bool)
	for _, committee := range committees {
		centers[committee.Center] = true
	}

	// Create monthly committees for each center
	for center := range centers {
		// Create Academic Committee
		js.createCommitteeForCenter(ctx, center, "ACADEMIC", "MONTHLY")
		
		// Create Disciplinary Committee
		js.createCommitteeForCenter(ctx, center, "DISCIPLINARY", "MONTHLY")
	}
}

// createCommitteeForCenter creates a committee for a specific center
func (js *JobScheduler) createCommitteeForCenter(ctx context.Context, center, committeeType, subType string) {
	currentDate := time.Now()
	
	committee := &entities.Committee{
		Name:        fmt.Sprintf("%s Committee %s - %s %d", committeeType, center, currentDate.Month(), currentDate.Year()),
		Type:        entities.CommitteeType(committeeType),
		SubType:     entities.CommitteeSubType(subType),
		Center:      center,
		Status:      entities.CommitteeStatusActive,
		StartDate:   currentDate,
		EndDate:     currentDate.AddDate(0, 1, 0), // One month duration
		Description: fmt.Sprintf("Monthly %s committee for %s center", committeeType, center),
		CreatedAt:   currentDate,
		UpdatedAt:   currentDate,
	}

	if err := js.committeeRepo.Create(ctx, committee); err != nil {
		log.Printf("Error creating %s committee for center %s: %v", committeeType, center, err)
		return
	}

	log.Printf("Created %s committee for center %s", committeeType, center)
}

// checkOverdueCases checks for overdue student cases and sends alerts
func (js *JobScheduler) checkOverdueCases() {
	ctx := context.Background()
	
	log.Println("Checking for overdue student cases")

	overdueCases, err := js.studentCaseRepo.GetOverdueCases(ctx)
	if err != nil {
		log.Printf("Error getting overdue cases: %v", err)
		return
	}

	if len(overdueCases) == 0 {
		log.Println("No overdue cases found")
		return
	}

	// Group cases by committee for better notification management
	casesByCommittee := make(map[string][]*entities.StudentCase)
	for _, studentCase := range overdueCases {
		committeeID := studentCase.CommitteeID.String()
		casesByCommittee[committeeID] = append(casesByCommittee[committeeID], studentCase)
	}

	// Send notifications for each committee
	for committeeID, cases := range casesByCommittee {
		js.sendOverdueCaseAlert(ctx, committeeID, cases)
	}

	log.Printf("Processed %d overdue cases", len(overdueCases))
}

// sendOverdueCaseAlert sends alert for overdue cases
func (js *JobScheduler) sendOverdueCaseAlert(ctx context.Context, committeeID string, cases []*entities.StudentCase) {
	subject := fmt.Sprintf("ALERT: %d Overdue Student Cases", len(cases))
	
	body := "The following student cases are overdue and require immediate attention:\n\n"
	for _, studentCase := range cases {
		daysOverdue := int(time.Since(*studentCase.DueDate).Hours() / 24)
		body += fmt.Sprintf("- Case #%s: %s (Overdue by %d days)\n", 
			studentCase.CaseNumber, studentCase.Title, daysOverdue)
	}
	
	body += "\nPlease review and take appropriate action immediately."

	if err := js.notificationService.SendAlert(body, "HIGH"); err != nil {
		log.Printf("Error sending overdue case alert: %v", err)
	}
}

// checkImprovementPlanProgress checks improvement plan progress and sends reminders
func (js *JobScheduler) checkImprovementPlanProgress() {
	ctx := context.Background()
	
	log.Println("Checking improvement plan progress")

	// Get all active improvement plans
	plans, err := js.improvementPlanRepo.GetByStatus(ctx, string(entities.PlanStatusActive))
	if err != nil {
		log.Printf("Error getting active improvement plans: %v", err)
		return
	}

	stagnantPlans := []*entities.ImprovementPlan{}
	nearDeadlinePlans := []*entities.ImprovementPlan{}

	for _, plan := range plans {
		// Check for stagnant plans (no progress update in 7 days)
		if time.Since(plan.UpdatedAt).Hours() > 168 { // 7 days
			stagnantPlans = append(stagnantPlans, plan)
		}

		// Check for plans nearing deadline (within 7 days)
		if plan.EndDate.Sub(time.Now()).Hours() < 168 && plan.EndDate.Sub(time.Now()).Hours() > 0 {
			nearDeadlinePlans = append(nearDeadlinePlans, plan)
		}
	}

	if len(stagnantPlans) > 0 {
		js.sendStagnantPlanAlert(stagnantPlans)
	}

	if len(nearDeadlinePlans) > 0 {
		js.sendNearDeadlinePlanAlert(nearDeadlinePlans)
	}

	log.Printf("Checked %d improvement plans: %d stagnant, %d near deadline", 
		len(plans), len(stagnantPlans), len(nearDeadlinePlans))
}

// sendStagnantPlanAlert sends alert for stagnant improvement plans
func (js *JobScheduler) sendStagnantPlanAlert(plans []*entities.ImprovementPlan) {
	subject := fmt.Sprintf("ALERT: %d Stagnant Improvement Plans", len(plans))
	
	body := "The following improvement plans have not been updated in over 7 days:\n\n"
	for _, plan := range plans {
		daysStagnant := int(time.Since(plan.UpdatedAt).Hours() / 24)
		body += fmt.Sprintf("- Plan #%s: %s (Last updated %d days ago)\n", 
			plan.PlanNumber, plan.Title, daysStagnant)
	}
	
	body += "\nPlease review and update progress immediately."

	if err := js.notificationService.SendAlert(body, "MEDIUM"); err != nil {
		log.Printf("Error sending stagnant plan alert: %v", err)
	}
}

// sendNearDeadlinePlanAlert sends alert for plans nearing deadline
func (js *JobScheduler) sendNearDeadlinePlanAlert(plans []*entities.ImprovementPlan) {
	subject := fmt.Sprintf("REMINDER: %d Improvement Plans Nearing Deadline", len(plans))
	
	body := "The following improvement plans are nearing their deadline:\n\n"
	for _, plan := range plans {
		daysRemaining := int(plan.EndDate.Sub(time.Now()).Hours() / 24)
		body += fmt.Sprintf("- Plan #%s: %s (%d days remaining)\n", 
			plan.PlanNumber, plan.Title, daysRemaining)
	}
	
	body += "\nPlease ensure completion before the deadline."

	if err := js.notificationService.SendAlert(body, "MEDIUM"); err != nil {
		log.Printf("Error sending near deadline plan alert: %v", err)
	}
}

// checkSanctionExpirations checks for sanctions that are expiring or have expired
func (js *JobScheduler) checkSanctionExpirations() {
	ctx := context.Background()
	
	log.Println("Checking sanction expirations")

	// Get all active sanctions
	sanctions, err := js.sanctionRepo.GetByStatus(ctx, string(entities.SanctionStatusActive))
	if err != nil {
		log.Printf("Error getting active sanctions: %v", err)
		return
	}

	expiredSanctions := []*entities.Sanction{}
	expiringSanctions := []*entities.Sanction{}

	for _, sanction := range sanctions {
		now := time.Now()
		
		// Check for expired sanctions
		if sanction.EndDate.Before(now) {
			expiredSanctions = append(expiredSanctions, sanction)
			
			// Auto-complete expired sanctions
			sanction.Status = entities.SanctionStatusCompleted
			sanction.UpdatedAt = now
			if err := js.sanctionRepo.Update(ctx, sanction); err != nil {
				log.Printf("Error auto-completing expired sanction %s: %v", sanction.SanctionNumber, err)
			}
		} else if sanction.EndDate.Sub(now).Hours() < 72 { // Within 3 days
			expiringSanctions = append(expiringSanctions, sanction)
		}
	}

	if len(expiredSanctions) > 0 {
		js.sendExpiredSanctionAlert(expiredSanctions)
	}

	if len(expiringSanctions) > 0 {
		js.sendExpiringSanctionAlert(expiringSanctions)
	}

	log.Printf("Processed sanctions: %d expired (auto-completed), %d expiring soon", 
		len(expiredSanctions), len(expiringSanctions))
}

// sendExpiredSanctionAlert sends alert for expired sanctions
func (js *JobScheduler) sendExpiredSanctionAlert(sanctions []*entities.Sanction) {
	subject := fmt.Sprintf("INFO: %d Sanctions Auto-Completed", len(sanctions))
	
	body := "The following sanctions have expired and were automatically completed:\n\n"
	for _, sanction := range sanctions {
		body += fmt.Sprintf("- Sanction #%s: %s (Expired on %s)\n", 
			sanction.SanctionNumber, sanction.Title, sanction.EndDate.Format("2006-01-02"))
	}

	if err := js.notificationService.SendAlert(body, "LOW"); err != nil {
		log.Printf("Error sending expired sanction alert: %v", err)
	}
}

// sendExpiringSanctionAlert sends alert for sanctions expiring soon
func (js *JobScheduler) sendExpiringSanctionAlert(sanctions []*entities.Sanction) {
	subject := fmt.Sprintf("REMINDER: %d Sanctions Expiring Soon", len(sanctions))
	
	body := "The following sanctions will expire within 3 days:\n\n"
	for _, sanction := range sanctions {
		daysRemaining := int(sanction.EndDate.Sub(time.Now()).Hours() / 24)
		body += fmt.Sprintf("- Sanction #%s: %s (%d days remaining)\n", 
			sanction.SanctionNumber, sanction.Title, daysRemaining)
	}
	
	body += "\nPlease review completion status."

	if err := js.notificationService.SendAlert(body, "LOW"); err != nil {
		log.Printf("Error sending expiring sanction alert: %v", err)
	}
}

// checkAppealDeadlines checks for appeals approaching deadline
func (js *JobScheduler) checkAppealDeadlines() {
	ctx := context.Background()
	
	log.Println("Checking appeal deadlines")

	// Get all submitted appeals
	appeals, err := js.appealRepo.GetByStatus(ctx, string(entities.AppealStatusSubmitted))
	if err != nil {
		log.Printf("Error getting submitted appeals: %v", err)
		return
	}

	urgentAppeals := []*entities.Appeal{}

	for _, appeal := range appeals {
		// Appeals should be reviewed within 15 days of submission
		daysSinceSubmission := int(time.Since(appeal.RequestDate).Hours() / 24)
		
		if daysSinceSubmission >= 12 { // 3 days before deadline
			urgentAppeals = append(urgentAppeals, appeal)
		}
	}

	if len(urgentAppeals) > 0 {
		js.sendUrgentAppealAlert(urgentAppeals)
	}

	log.Printf("Checked %d appeals: %d urgent", len(appeals), len(urgentAppeals))
}

// sendUrgentAppealAlert sends alert for urgent appeals
func (js *JobScheduler) sendUrgentAppealAlert(appeals []*entities.Appeal) {
	subject := fmt.Sprintf("URGENT: %d Appeals Require Immediate Review", len(appeals))
	
	body := "The following appeals are approaching the review deadline (15 days):\n\n"
	for _, appeal := range appeals {
		daysSinceSubmission := int(time.Since(appeal.RequestDate).Hours() / 24)
		daysRemaining := 15 - daysSinceSubmission
		body += fmt.Sprintf("- Appeal #%s: %s (%d days remaining)\n", 
			appeal.AppealNumber, appeal.Reason[:50]+"...", daysRemaining)
	}
	
	body += "\nPlease review and process these appeals immediately to comply with regulations."

	if err := js.notificationService.SendAlert(body, "HIGH"); err != nil {
		log.Printf("Error sending urgent appeal alert: %v", err)
	}
}

// generateMonthlyReports generates performance reports for committees
func (js *JobScheduler) generateMonthlyReports() {
	ctx := context.Background()
	
	log.Println("Generating monthly performance reports")

	// Check if it's actually the last day of the month
	now := time.Now()
	tomorrow := now.AddDate(0, 0, 1)
	if now.Month() == tomorrow.Month() {
		// Not the last day of month
		return
	}

	// Get all committees for this month
	startOfMonth := time.Date(now.Year(), now.Month(), 1, 0, 0, 0, 0, now.Location())
	endOfMonth := startOfMonth.AddDate(0, 1, -1)

	committees, err := js.committeeRepo.GetByDateRange(ctx, startOfMonth, endOfMonth)
	if err != nil {
		log.Printf("Error getting committees for monthly report: %v", err)
		return
	}

	for _, committee := range committees {
		js.generateCommitteeReport(ctx, committee, startOfMonth, endOfMonth)
	}

	log.Printf("Generated monthly reports for %d committees", len(committees))
}

// generateCommitteeReport generates a performance report for a specific committee
func (js *JobScheduler) generateCommitteeReport(ctx context.Context, committee *entities.Committee, startDate, endDate time.Time) {
	// Get cases handled by this committee
	cases, err := js.studentCaseRepo.GetByCommitteeAndDateRange(ctx, committee.ID, startDate, endDate)
	if err != nil {
		log.Printf("Error getting cases for committee %s report: %v", committee.ID, err)
		return
	}

	// Calculate metrics
	totalCases := len(cases)
	resolvedCases := 0
	overdueCases := 0
	
	for _, studentCase := range cases {
		if studentCase.Status == entities.CaseStatusResolved || studentCase.Status == entities.CaseStatusClosed {
			resolvedCases++
		}
		if studentCase.DueDate != nil && studentCase.DueDate.Before(time.Now()) && 
		   studentCase.Status != entities.CaseStatusResolved && studentCase.Status != entities.CaseStatusClosed {
			overdueCases++
		}
	}

	resolutionRate := float64(0)
	if totalCases > 0 {
		resolutionRate = float64(resolvedCases) / float64(totalCases) * 100
	}

	// Generate report
	subject := fmt.Sprintf("Monthly Report - %s Committee (%s %d)", 
		committee.Name, endDate.Month(), endDate.Year())
	
	body := fmt.Sprintf(`Monthly Performance Report

Committee: %s
Period: %s to %s

METRICS:
- Total Cases Handled: %d
- Cases Resolved: %d
- Cases Overdue: %d
- Resolution Rate: %.1f%%

STATUS SUMMARY:
`, committee.Name, startDate.Format("2006-01-02"), endDate.Format("2006-01-02"), 
		totalCases, resolvedCases, overdueCases, resolutionRate)

	// Add case status breakdown
	statusCount := make(map[entities.CaseStatus]int)
	for _, studentCase := range cases {
		statusCount[studentCase.Status]++
	}

	for status, count := range statusCount {
		body += fmt.Sprintf("- %s: %d\n", status, count)
	}

	body += "\nThis is an automated monthly report from MEvalService."

	if err := js.notificationService.SendEmail([]string{"admin@sicora.edu"}, subject, body); err != nil {
		log.Printf("Error sending monthly report for committee %s: %v", committee.ID, err)
	}
}
