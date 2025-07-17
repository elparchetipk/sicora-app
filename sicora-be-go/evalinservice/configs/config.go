package configs

import (
	"os"
	"strconv"
)

// Config contiene toda la configuración de la aplicación
type Config struct {
	// Servidor
	ServerPort  string
	Environment string

	// Base de datos
	DatabaseURL      string
	DatabaseHost     string
	DatabasePort     string
	DatabaseUser     string
	DatabasePassword string
	DatabaseName     string
	DatabaseSSLMode  string

	// JWT
	JWTSecret     string
	JWTExpiration int

	// Servicios externos
	UserServiceURL         string
	ScheduleServiceURL     string
	NotificationServiceURL string

	// Rate limiting
	RateLimitEnabled bool
	RateLimitRPS     int

	// CORS
	CORSAllowedOrigins []string
	CORSAllowedMethods []string
	CORSAllowedHeaders []string
}

// LoadConfig carga la configuración desde variables de entorno
func LoadConfig() *Config {
	return &Config{
		// Servidor
		ServerPort:  getEnv("PORT", "8004"),
		Environment: getEnv("ENVIRONMENT", "development"),

		// Base de datos
		DatabaseURL:      getEnv("DATABASE_URL", ""),
		DatabaseHost:     getEnv("DB_HOST", "localhost"),
		DatabasePort:     getEnv("DB_PORT", "5432"),
		DatabaseUser:     getEnv("DB_USER", "sicora_user"),
		DatabasePassword: getEnv("DB_PASSWORD", "sicora_password"),
		DatabaseName:     getEnv("DB_NAME", "sicora_evalin_db"),
		DatabaseSSLMode:  getEnv("DB_SSL_MODE", "disable"),

		// JWT
		JWTSecret:     getEnv("JWT_SECRET", "your-super-secret-jwt-key-change-in-production"),
		JWTExpiration: getEnvAsInt("JWT_EXPIRATION", 24), // horas

		// Servicios externos
		UserServiceURL:         getEnv("USER_SERVICE_URL", "http://localhost:8001"),
		ScheduleServiceURL:     getEnv("SCHEDULE_SERVICE_URL", "http://localhost:8002"),
		NotificationServiceURL: getEnv("NOTIFICATION_SERVICE_URL", "http://localhost:8007"),

		// Rate limiting
		RateLimitEnabled: getEnvAsBool("RATE_LIMIT_ENABLED", true),
		RateLimitRPS:     getEnvAsInt("RATE_LIMIT_RPS", 100),

		// CORS
		CORSAllowedOrigins: getEnvAsStringSlice("CORS_ALLOWED_ORIGINS", []string{"http://localhost:3000", "http://localhost:3001"}),
		CORSAllowedMethods: getEnvAsStringSlice("CORS_ALLOWED_METHODS", []string{"GET", "POST", "PUT", "DELETE", "OPTIONS"}),
		CORSAllowedHeaders: getEnvAsStringSlice("CORS_ALLOWED_HEADERS", []string{"Origin", "Content-Type", "Accept", "Authorization", "X-Requested-With"}),
	}
}

// GetDatabaseDSN retorna el DSN para la conexión a PostgreSQL
func (c *Config) GetDatabaseDSN() string {
	if c.DatabaseURL != "" {
		return c.DatabaseURL
	}

	return "host=" + c.DatabaseHost +
		" port=" + c.DatabasePort +
		" user=" + c.DatabaseUser +
		" password=" + c.DatabasePassword +
		" dbname=" + c.DatabaseName +
		" sslmode=" + c.DatabaseSSLMode
}

// Helper functions
func getEnv(key, defaultValue string) string {
	if value := os.Getenv(key); value != "" {
		return value
	}
	return defaultValue
}

func getEnvAsInt(key string, defaultValue int) int {
	if value := os.Getenv(key); value != "" {
		if intValue, err := strconv.Atoi(value); err == nil {
			return intValue
		}
	}
	return defaultValue
}

func getEnvAsBool(key string, defaultValue bool) bool {
	if value := os.Getenv(key); value != "" {
		if boolValue, err := strconv.ParseBool(value); err == nil {
			return boolValue
		}
	}
	return defaultValue
}

func getEnvAsStringSlice(key string, defaultValue []string) []string {
	if value := os.Getenv(key); value != "" {
		// Implementación básica - en producción podríamos usar una librería para parsing más sofisticado
		return []string{value}
	}
	return defaultValue
}
