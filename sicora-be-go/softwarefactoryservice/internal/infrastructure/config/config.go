package config

import (
	"fmt"
	"os"
	"strconv"
)

// DatabaseConfig holds database configuration
type DatabaseConfig struct {
	Host     string
	Port     int
	User     string
	Password string
	DBName   string
	Schema   string
	SSLMode  string
}

// ServerConfig holds server configuration
type ServerConfig struct {
	Host string
	Port int
}

// PaginationConfig holds pagination configuration
type PaginationConfig struct {
	DefaultPageSize int
	MaxPageSize     int
	DefaultPage     int
}

// Config holds all configuration
type Config struct {
	Database   DatabaseConfig
	Server     ServerConfig
	Pagination PaginationConfig
	JWTSecret  string
	Environment string
}

// LoadConfig loads configuration from environment variables
func LoadConfig() (*Config, error) {
	config := &Config{
		Database: DatabaseConfig{
			Host:     getEnvOrDefault("DB_HOST", "localhost"),
			Port:     getIntEnvOrDefault("DB_PORT", 5432),
			User:     getEnvOrDefault("DB_USER", "softwarefactoryservice_user"),
			Password: getEnvOrDefault("DB_PASSWORD", "softwarefactoryservice_password_placeholder"),
			DBName:   getEnvOrDefault("DB_NAME", "sicora_db"),
			Schema:   getEnvOrDefault("DB_SCHEMA", "softwarefactoryservice_schema"),
			SSLMode:  getEnvOrDefault("DB_SSL_MODE", "disable"),
		},
		Server: ServerConfig{
			Host: getEnvOrDefault("SERVER_HOST", "0.0.0.0"),
			Port: getIntEnvOrDefault("SERVER_PORT", 8080),
		},
		Pagination: PaginationConfig{
			DefaultPageSize: getIntEnvOrDefault("PAGINATION_DEFAULT_SIZE", 20),
			MaxPageSize:     getIntEnvOrDefault("PAGINATION_MAX_SIZE", 100),
			DefaultPage:     getIntEnvOrDefault("PAGINATION_DEFAULT_PAGE", 1),
		},
		JWTSecret:   getEnvOrDefault("JWT_SECRET", "your-secret-key"),
		Environment: getEnvOrDefault("ENVIRONMENT", "development"),
	}

	// Validate required configuration
	if config.Database.Password == "" && config.Environment == "production" {
		return nil, fmt.Errorf("database password is required in production")
	}

	return config, nil
}

// GetDSN returns the database connection string with schema configuration
func (c *DatabaseConfig) GetDSN() string {
	dsn := fmt.Sprintf("host=%s port=%d user=%s password=%s dbname=%s sslmode=%s",
		c.Host, c.Port, c.User, c.Password, c.DBName, c.SSLMode)
	
	// Add search_path parameter to use the specific schema
	if c.Schema != "" {
		dsn += fmt.Sprintf(" search_path=%s", c.Schema)
	}
	
	return dsn
}

// GetServerAddress returns the server address
func (c *ServerConfig) GetServerAddress() string {
	return fmt.Sprintf("%s:%d", c.Host, c.Port)
}

// Helper functions
func getEnvOrDefault(key, defaultValue string) string {
	if value := os.Getenv(key); value != "" {
		return value
	}
	return defaultValue
}

func getIntEnvOrDefault(key string, defaultValue int) int {
	if value := os.Getenv(key); value != "" {
		if intValue, err := strconv.Atoi(value); err == nil {
			return intValue
		}
	}
	return defaultValue
}
