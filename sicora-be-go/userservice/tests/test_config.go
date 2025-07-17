package test

import (
	"os"
	"testing"
)

// TestMain se ejecuta antes de todos los tests
func TestMain(m *testing.M) {
	// Setup test environment
	setupTestEnvironment()

	// Run tests
	code := m.Run()

	// Cleanup test environment
	cleanupTestEnvironment()

	// Exit with test result code
	os.Exit(code)
}

// setupTestEnvironment configura las variables de entorno para testing
func setupTestEnvironment() {
	// Set test environment variables
	os.Setenv("GIN_MODE", "test")
	os.Setenv("JWT_SECRET", "test-secret-key-for-testing-only")
	os.Setenv("DB_HOST", "localhost")
	os.Setenv("DB_PORT", "5432")
	os.Setenv("DB_NAME", "sicora_userservice_test")
	os.Setenv("DB_USER", "sicora_user")
	os.Setenv("DB_PASSWORD", "sicora_password")
	os.Setenv("LOG_LEVEL", "error") // Reduce log output during testing
}

// cleanupTestEnvironment limpia el entorno después de los tests
func cleanupTestEnvironment() {
	// Clean up any test data or connections if needed
	// For unit tests with mocks, this might not be necessary
}

// GetTestJWTSecret returns the JWT secret for testing
func GetTestJWTSecret() string {
	return "test-secret-key-for-testing-only"
}

// GetTestDatabaseURL returns the test database URL
func GetTestDatabaseURL() string {
	return "postgres://sicora_user:sicora_password@localhost:5432/sicora_userservice_test?sslmode=disable"
}
