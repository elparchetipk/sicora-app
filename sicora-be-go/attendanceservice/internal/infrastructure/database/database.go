package database

import (
	"fmt"

	"attendanceservice/internal/infrastructure/database/models"

	"gorm.io/driver/postgres"
	"gorm.io/gorm"
	"gorm.io/gorm/logger"
)

// Config estructura de configuración de la base de datos
type Config struct {
	Host     string
	Port     string
	User     string
	Password string
	DBName   string
	Schema   string
	SSLMode  string
}

// Database wrapper para GORM
type Database struct {
	*gorm.DB
}

// NewDatabase crea una nueva conexión a la base de datos
func NewDatabase(config Config) (*Database, error) {
	dsn := fmt.Sprintf(
		"host=%s port=%s user=%s password=%s dbname=%s search_path=%s sslmode=%s",
		config.Host,
		config.Port,
		config.User,
		config.Password,
		config.DBName,
		config.Schema,
		config.SSLMode,
	)

	db, err := gorm.Open(postgres.Open(dsn), &gorm.Config{
		Logger: logger.Default.LogMode(logger.Info),
	})
	if err != nil {
		return nil, fmt.Errorf("failed to connect to database: %w", err)
	}

	// Configurar el pool de conexiones
	sqlDB, err := db.DB()
	if err != nil {
		return nil, fmt.Errorf("failed to get database instance: %w", err)
	}

	sqlDB.SetMaxIdleConns(10)
	sqlDB.SetMaxOpenConns(100)

	return &Database{db}, nil
}

// AutoMigrate ejecuta las migraciones automáticas
func (db *Database) AutoMigrate() error {
	return db.DB.AutoMigrate(
		&models.AttendanceRecord{},
		&models.AttendanceQRCode{},
		&models.Justification{},
		&models.AttendanceAlert{},
	)
}

// CreateSchema crea el schema si no existe
func (db *Database) CreateSchema(schemaName string) error {
	return db.DB.Exec(fmt.Sprintf("CREATE SCHEMA IF NOT EXISTS %s", schemaName)).Error
}

// Close cierra la conexión a la base de datos
func (db *Database) Close() error {
	sqlDB, err := db.DB.DB()
	if err != nil {
		return err
	}
	return sqlDB.Close()
}
