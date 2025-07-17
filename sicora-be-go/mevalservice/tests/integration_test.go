package tests

import (
	"bytes"
	"encoding/json"
	"net/http"
	"net/http/httptest"
	"testing"
	"time"

	"github.com/gin-gonic/gin"
	"github.com/google/uuid"
	"github.com/stretchr/testify/assert"
	"github.com/stretchr/testify/require"

	"mevalservice/internal/application/dto"
	"mevalservice/internal/application/usecases"
	"mevalservice/internal/infrastructure/database"
	"mevalservice/internal/infrastructure/repositories"
	"mevalservice/internal/presentation/handlers"
	"mevalservice/internal/presentation/routes"
)

// setupTestServer sets up a test server with in-memory database
func setupTestServer() (*gin.Engine, *database.Database, error) {
	// Setup test database (use in-memory SQLite for testing)
	db, err := database.NewTestDatabase()
	if err != nil {
		return nil, nil, err
	}

	// Run migrations
	if err := db.AutoMigrate(); err != nil {
		return nil, nil, err
	}

	// Initialize repositories
	repos := repositories.NewRepositories(db)

	// Initialize use cases
	committeeUC := usecases.NewCommitteeUseCases(repos.Committee, repos.CommitteeMember)
	studentCaseUC := usecases.NewStudentCaseUseCases(repos.StudentCase, repos.Committee)
	improvementPlanUC := usecases.NewImprovementPlanUseCases(repos.ImprovementPlan, repos.StudentCase)
	sanctionUC := usecases.NewSanctionUseCases(repos.Sanction, repos.StudentCase)
	appealUC := usecases.NewAppealUseCases(repos.Appeal, repos.StudentCase)

	// Initialize handlers
	committeeHandler := handlers.NewCommitteeHandler(committeeUC)
	studentCaseHandler := handlers.NewStudentCaseHandler(studentCaseUC)
	improvementPlanHandler := handlers.NewImprovementPlanHandler(improvementPlanUC)
	sanctionHandler := handlers.NewSanctionHandler(sanctionUC)
	appealHandler := handlers.NewAppealHandler(appealUC)
	healthHandler := handlers.NewHealthHandler()

	// Setup router
	gin.SetMode(gin.TestMode)
	router := gin.New()
	routes.SetupRoutes(router, committeeHandler, studentCaseHandler, improvementPlanHandler, sanctionHandler, appealHandler, healthHandler)

	return router, db, nil
}

func TestHealthEndpoint(t *testing.T) {
	router, db, err := setupTestServer()
	require.NoError(t, err)
	defer db.Close()

	w := httptest.NewRecorder()
	req, _ := http.NewRequest("GET", "/health", nil)
	router.ServeHTTP(w, req)

	assert.Equal(t, http.StatusOK, w.Code)
	
	var response map[string]interface{}
	err = json.Unmarshal(w.Body.Bytes(), &response)
	require.NoError(t, err)
	assert.Equal(t, "healthy", response["status"])
}

func TestCommitteeFlow(t *testing.T) {
	router, db, err := setupTestServer()
	require.NoError(t, err)
	defer db.Close()

	// Test creating a committee
	createReq := dto.CreateCommitteeRequest{
		Name:        "Test Academic Committee",
		Type:        "ACADEMIC",
		SubType:     "MONTHLY",
		Center:      "Centro Biotecnología Industrial",
		StartDate:   time.Now(),
		EndDate:     time.Now().AddDate(0, 1, 0),
		Description: "Test committee for integration testing",
	}

	body, _ := json.Marshal(createReq)
	w := httptest.NewRecorder()
	req, _ := http.NewRequest("POST", "/api/v1/committees", bytes.NewBuffer(body))
	req.Header.Set("Content-Type", "application/json")
	router.ServeHTTP(w, req)

	assert.Equal(t, http.StatusCreated, w.Code)

	var createResponse dto.CommitteeResponse
	err = json.Unmarshal(w.Body.Bytes(), &createResponse)
	require.NoError(t, err)
	assert.Equal(t, createReq.Name, createResponse.Name)
	assert.Equal(t, createReq.Type, createResponse.Type)

	// Test getting the committee by ID
	w = httptest.NewRecorder()
	req, _ = http.NewRequest("GET", "/api/v1/committees/"+createResponse.ID.String(), nil)
	router.ServeHTTP(w, req)

	assert.Equal(t, http.StatusOK, w.Code)

	var getResponse dto.CommitteeResponse
	err = json.Unmarshal(w.Body.Bytes(), &getResponse)
	require.NoError(t, err)
	assert.Equal(t, createResponse.ID, getResponse.ID)
	assert.Equal(t, createResponse.Name, getResponse.Name)
}

func TestStudentCaseFlow(t *testing.T) {
	router, db, err := setupTestServer()
	require.NoError(t, err)
	defer db.Close()

	// First create a committee for the student case
	committee := createTestCommittee(t, router)

	// Test creating a student case
	studentID := uuid.New()
	dueDate := time.Now().AddDate(0, 0, 30)

	createReq := dto.CreateStudentCaseRequest{
		StudentID:   studentID,
		CommitteeID: committee.ID,
		CaseNumber:  "CASE-001-2024",
		Type:        "ACADEMIC",
		Severity:    "MEDIUM",
		Priority:    "NORMAL",
		Title:       "Academic Performance Issue",
		Description: "Student showing declining academic performance",
		Evidence:    "Low grades in last semester",
		ReportedBy:  uuid.New(),
		DueDate:     &dueDate,
	}

	body, _ := json.Marshal(createReq)
	w := httptest.NewRecorder()
	req, _ := http.NewRequest("POST", "/api/v1/student-cases", bytes.NewBuffer(body))
	req.Header.Set("Content-Type", "application/json")
	router.ServeHTTP(w, req)

	assert.Equal(t, http.StatusCreated, w.Code)

	var createResponse dto.StudentCaseResponse
	err = json.Unmarshal(w.Body.Bytes(), &createResponse)
	require.NoError(t, err)
	assert.Equal(t, createReq.CaseNumber, createResponse.CaseNumber)
	assert.Equal(t, createReq.Title, createResponse.Title)

	// Test getting the student case by ID
	w = httptest.NewRecorder()
	req, _ = http.NewRequest("GET", "/api/v1/student-cases/"+createResponse.ID.String(), nil)
	router.ServeHTTP(w, req)

	assert.Equal(t, http.StatusOK, w.Code)
}

func TestImprovementPlanFlow(t *testing.T) {
	router, db, err := setupTestServer()
	require.NoError(t, err)
	defer db.Close()

	// Create prerequisites
	committee := createTestCommittee(t, router)
	studentCase := createTestStudentCase(t, router, committee.ID)

	// Test creating an improvement plan
	startDate := time.Now()
	endDate := time.Now().AddDate(0, 3, 0) // 3 months

	createReq := dto.CreateImprovementPlanRequest{
		StudentCaseID:      studentCase.ID,
		StudentID:          studentCase.StudentID,
		SupervisorID:       uuid.New(),
		PlanNumber:         "PLAN-001-2024",
		Title:              "Academic Recovery Plan",
		Description:        "Comprehensive plan to improve academic performance",
		Objectives:         "Achieve passing grades in all subjects",
		Activities:         "Weekly tutoring sessions, study groups",
		Resources:          "Tutoring materials, study guides",
		Timeline:           "3 months with weekly check-ins",
		EvaluationCriteria: "Monthly progress assessments",
		StartDate:          startDate,
		EndDate:            endDate,
	}

	body, _ := json.Marshal(createReq)
	w := httptest.NewRecorder()
	req, _ := http.NewRequest("POST", "/api/v1/improvement-plans", bytes.NewBuffer(body))
	req.Header.Set("Content-Type", "application/json")
	router.ServeHTTP(w, req)

	assert.Equal(t, http.StatusCreated, w.Code)

	var createResponse dto.ImprovementPlanResponse
	err = json.Unmarshal(w.Body.Bytes(), &createResponse)
	require.NoError(t, err)
	assert.Equal(t, createReq.PlanNumber, createResponse.PlanNumber)
	assert.Equal(t, createReq.Title, createResponse.Title)

	// Test updating progress
	progressReq := map[string]interface{}{
		"progress": 50,
		"notes":    "Student showing good progress in math and science",
	}

	body, _ = json.Marshal(progressReq)
	w = httptest.NewRecorder()
	req, _ = http.NewRequest("PATCH", "/api/v1/improvement-plans/"+createResponse.ID.String()+"/progress", bytes.NewBuffer(body))
	req.Header.Set("Content-Type", "application/json")
	router.ServeHTTP(w, req)

	assert.Equal(t, http.StatusOK, w.Code)
}

func TestSanctionFlow(t *testing.T) {
	router, db, err := setupTestServer()
	require.NoError(t, err)
	defer db.Close()

	// Create prerequisites
	committee := createTestCommittee(t, router)
	studentCase := createTestStudentCase(t, router, committee.ID)

	// Test creating a sanction
	startDate := time.Now()
	endDate := time.Now().AddDate(0, 1, 0) // 1 month

	createReq := dto.CreateSanctionRequest{
		StudentCaseID:   studentCase.ID,
		StudentID:       studentCase.StudentID,
		SanctionNumber:  "SANC-001-2024",
		Type:            "LLAMADO_ATENCION",
		Severity:        "LOW",
		Title:           "First Warning",
		Description:     "Formal warning for tardiness",
		StartDate:       startDate,
		EndDate:         endDate,
		Conditions:      "Must arrive on time for all classes",
		RequiredActions: "Submit attendance report weekly",
		IssuedBy:        uuid.New(),
		ApprovedBy:      uuid.New(),
	}

	body, _ := json.Marshal(createReq)
	w := httptest.NewRecorder()
	req, _ := http.NewRequest("POST", "/api/v1/sanctions", bytes.NewBuffer(body))
	req.Header.Set("Content-Type", "application/json")
	router.ServeHTTP(w, req)

	assert.Equal(t, http.StatusCreated, w.Code)

	var createResponse dto.SanctionResponse
	err = json.Unmarshal(w.Body.Bytes(), &createResponse)
	require.NoError(t, err)
	assert.Equal(t, createReq.SanctionNumber, createResponse.SanctionNumber)
	assert.Equal(t, createReq.Title, createResponse.Title)

	// Test activating sanction
	w = httptest.NewRecorder()
	req, _ = http.NewRequest("PATCH", "/api/v1/sanctions/"+createResponse.ID.String()+"/activate", nil)
	router.ServeHTTP(w, req)

	assert.Equal(t, http.StatusOK, w.Code)
}

func TestAppealFlow(t *testing.T) {
	router, db, err := setupTestServer()
	require.NoError(t, err)
	defer db.Close()

	// Create prerequisites
	committee := createTestCommittee(t, router)
	studentCase := createTestStudentCase(t, router, committee.ID)

	// Test creating an appeal
	createReq := dto.CreateAppealRequest{
		StudentCaseID: studentCase.ID,
		StudentID:     studentCase.StudentID,
		AppealNumber:  "APP-001-2024",
		Type:          "DECISION_APPEAL",
		Reason:        "I believe the decision was unfair and not based on complete evidence",
		Evidence:      "Additional documentation proving attendance",
		RequestedBy:   studentCase.StudentID,
		RequestDate:   time.Now(),
		Priority:      "HIGH",
	}

	body, _ := json.Marshal(createReq)
	w := httptest.NewRecorder()
	req, _ := http.NewRequest("POST", "/api/v1/appeals", bytes.NewBuffer(body))
	req.Header.Set("Content-Type", "application/json")
	router.ServeHTTP(w, req)

	assert.Equal(t, http.StatusCreated, w.Code)

	var createResponse dto.AppealResponse
	err = json.Unmarshal(w.Body.Bytes(), &createResponse)
	require.NoError(t, err)
	assert.Equal(t, createReq.AppealNumber, createResponse.AppealNumber)
	assert.Equal(t, createReq.Reason, createResponse.Reason)

	// Test processing appeal
	processReq := map[string]interface{}{
		"accepted":   true,
		"resolution": "Appeal accepted. Original decision reversed after review of additional evidence.",
	}

	body, _ = json.Marshal(processReq)
	w = httptest.NewRecorder()
	req, _ = http.NewRequest("PATCH", "/api/v1/appeals/"+createResponse.ID.String()+"/process", bytes.NewBuffer(body))
	req.Header.Set("Content-Type", "application/json")
	router.ServeHTTP(w, req)

	assert.Equal(t, http.StatusOK, w.Code)
}

// Helper functions for creating test data
func createTestCommittee(t *testing.T, router *gin.Engine) *dto.CommitteeResponse {
	createReq := dto.CreateCommitteeRequest{
		Name:        "Test Committee",
		Type:        "ACADEMIC",
		SubType:     "MONTHLY",
		Center:      "Test Center",
		StartDate:   time.Now(),
		EndDate:     time.Now().AddDate(0, 1, 0),
		Description: "Test committee",
	}

	body, _ := json.Marshal(createReq)
	w := httptest.NewRecorder()
	req, _ := http.NewRequest("POST", "/api/v1/committees", bytes.NewBuffer(body))
	req.Header.Set("Content-Type", "application/json")
	router.ServeHTTP(w, req)

	var response dto.CommitteeResponse
	json.Unmarshal(w.Body.Bytes(), &response)
	return &response
}

func createTestStudentCase(t *testing.T, router *gin.Engine, committeeID uuid.UUID) *dto.StudentCaseResponse {
	studentID := uuid.New()
	dueDate := time.Now().AddDate(0, 0, 30)

	createReq := dto.CreateStudentCaseRequest{
		StudentID:   studentID,
		CommitteeID: committeeID,
		CaseNumber:  "TEST-CASE-" + uuid.New().String()[:8],
		Type:        "ACADEMIC",
		Severity:    "MEDIUM",
		Priority:    "NORMAL",
		Title:       "Test Case",
		Description: "Test student case",
		Evidence:    "Test evidence",
		ReportedBy:  uuid.New(),
		DueDate:     &dueDate,
	}

	body, _ := json.Marshal(createReq)
	w := httptest.NewRecorder()
	req, _ := http.NewRequest("POST", "/api/v1/student-cases", bytes.NewBuffer(body))
	req.Header.Set("Content-Type", "application/json")
	router.ServeHTTP(w, req)

	var response dto.StudentCaseResponse
	json.Unmarshal(w.Body.Bytes(), &response)
	return &response
}
