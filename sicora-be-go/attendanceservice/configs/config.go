package configs

import (
	"fmt"
	"log"
	"os"
	"strconv"

	"github.com/joho/godotenv"
)

// Config estructura de configuración del servicio
type Config struct {
	Server   ServerConfig   `json:"server"`
	Database DatabaseConfig `json:"database"`
	JWT      JWTConfig      `json:"jwt"`
	CORS     CORSConfig     `json:"cors"`
}

// ServerConfig configuración del servidor
type ServerConfig struct {
	Host string `json:"host"`
	Port string `json:"port"`
	Env  string `json:"env"`
}

// DatabaseConfig configuración de la base de datos
type DatabaseConfig struct {
	Host     string `json:"host"`
	Port     string `json:"port"`
	User     string `json:"user"`
	Password string `json:"password"`
	DBName   string `json:"db_name"`
	Schema   string `json:"schema"`
	SSLMode  string `json:"ssl_mode"`
}

// JWTConfig configuración de JWT
type JWTConfig struct {
	Secret     string `json:"secret"`
	ExpiryHour int    `json:"expiry_hour"`
}

// CORSConfig configuración de CORS
type CORSConfig struct {
	AllowedOrigins []string `json:"allowed_origins"`
	AllowedMethods []string `json:"allowed_methods"`
	AllowedHeaders []string `json:"allowed_headers"`
}

// LoadConfig carga la configuración desde variables de entorno
func LoadConfig() (*Config, error) {
	// Intentar cargar archivo .env si existe
	if err := godotenv.Load(); err != nil {
		log.Println("No .env file found, using environment variables")
	}

	config := &Config{
		Server: ServerConfig{
			Host: getEnv("SERVER_HOST", "0.0.0.0"),
			Port: getEnv("SERVER_PORT", "8003"),
			Env:  getEnv("SERVER_ENV", "development"),
		},
		Database: DatabaseConfig{
			Host:     getEnv("DB_HOST", "localhost"),
			Port:     getEnv("DB_PORT", "5432"),
			User:     getEnv("DB_USER", "attendanceservice_user"),
			Password: getEnv("DB_PASSWORD", ""),
			DBName:   getEnv("DB_NAME", "sicora_multistack"),
			Schema:   getEnv("DB_SCHEMA", "attendanceservice"),
			SSLMode:  getEnv("DB_SSL_MODE", "disable"),
		},
		JWT: JWTConfig{
			Secret:     getEnv("JWT_SECRET", "your-secret-key"),
			ExpiryHour: getEnvAsInt("JWT_EXPIRY_HOUR", 24),
		},
		CORS: CORSConfig{
			AllowedOrigins: []string{
				getEnv("CORS_ALLOWED_ORIGINS", "*"),
			},
			AllowedMethods: []string{"GET", "POST", "PUT", "DELETE", "OPTIONS"},
			AllowedHeaders: []string{"Origin", "Content-Type", "Accept", "Authorization"},
		},
	}

	if err := validateConfig(config); err != nil {
		return nil, fmt.Errorf("invalid configuration: %w", err)
	}

	return config, nil
}

// getEnv obtiene una variable de entorno con valor por defecto
func getEnv(key, defaultValue string) string {
	if value := os.Getenv(key); value != "" {
		return value
	}
	return defaultValue
}

// getEnvAsInt obtiene una variable de entorno como entero con valor por defecto
func getEnvAsInt(key string, defaultValue int) int {
	if value := os.Getenv(key); value != "" {
		if intValue, err := strconv.Atoi(value); err == nil {
			return intValue
		}
	}
	return defaultValue
}

// validateConfig valida la configuración
func validateConfig(config *Config) error {
	if config.Database.Password == "" {
		return fmt.Errorf("database password is required")
	}
	if config.JWT.Secret == "your-secret-key" {
		return fmt.Errorf("JWT secret must be set")
	}
	return nil
}

// GetServerAddress retorna la dirección completa del servidor
func (c *Config) GetServerAddress() string {
	return fmt.Sprintf("%s:%s", c.Server.Host, c.Server.Port)
}

// IsDevelopment verifica si está en modo desarrollo
func (c *Config) IsDevelopment() bool {
	return c.Server.Env == "development"
}

// IsProduction verifica si está en modo producción
func (c *Config) IsProduction() bool {
	return c.Server.Env == "production"
}
