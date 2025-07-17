package main

import (
	"database/sql"
	"fmt"
	"log"
	"os"

	"github.com/joho/godotenv"
	_ "github.com/lib/pq"
)

func main() {
	// Cargar variables de entorno
	if err := godotenv.Load(); err != nil {
		log.Println("No se encontró archivo .env, usando variables del sistema")
	}

	// Configuración de base de datos
	dbHost := getEnv("DATABASE_HOST", "localhost")
	dbPort := getEnv("DATABASE_PORT", "5432")
	dbName := getEnv("DATABASE_NAME", "sicora_dev")
	dbUser := getEnv("DATABASE_USER", "sicora_user")
	dbPassword := getEnv("DATABASE_PASSWORD", "sicora_password")

	// Construir string de conexión
	dbURL := fmt.Sprintf("postgres://%s:%s@%s:%s/%s?sslmode=disable",
		dbUser, dbPassword, dbHost, dbPort, dbName)

	fmt.Printf("Intentando conectar a: %s:%s/%s\n", dbHost, dbPort, dbName)

	// Intentar conexión
	db, err := sql.Open("postgres", dbURL)
	if err != nil {
		log.Fatalf("Error al abrir conexión: %v", err)
	}
	defer db.Close()

	// Probar conexión
	if err := db.Ping(); err != nil {
		log.Fatalf("Error al hacer ping a la base de datos: %v", err)
	}

	fmt.Println("✅ Conexión a PostgreSQL exitosa!")

	// Verificar versión de PostgreSQL
	var version string
	err = db.QueryRow("SELECT version()").Scan(&version)
	if err != nil {
		log.Fatalf("Error al obtener versión: %v", err)
	}

	fmt.Printf("📊 Versión de PostgreSQL: %s\n", version)

	// Verificar que sea PostgreSQL 15
	if contains(version, "PostgreSQL 15") {
		fmt.Println("✅ PostgreSQL 15 confirmado!")
	} else {
		fmt.Println("⚠️  Advertencia: No se detectó PostgreSQL 15")
	}

	// Listar bases de datos disponibles
	fmt.Println("\n📋 Bases de datos disponibles:")
	rows, err := db.Query("SELECT datname FROM pg_database WHERE datistemplate = false")
	if err != nil {
		log.Printf("Error al listar bases de datos: %v", err)
		return
	}
	defer rows.Close()

	for rows.Next() {
		var dbName string
		if err := rows.Scan(&dbName); err != nil {
			log.Printf("Error al leer nombre de base de datos: %v", err)
			continue
		}
		fmt.Printf("  - %s\n", dbName)
	}
}

func getEnv(key, defaultValue string) string {
	if value := os.Getenv(key); value != "" {
		return value
	}
	return defaultValue
}

func contains(s, substr string) bool {
	return len(s) >= len(substr) && s[:len(substr)] == substr ||
		len(s) > len(substr) &&
			(s[len(s)-len(substr):] == substr ||
				indexOf(s, substr) != -1)
}

func indexOf(s, substr string) int {
	for i := 0; i <= len(s)-len(substr); i++ {
		if s[i:i+len(substr)] == substr {
			return i
		}
	}
	return -1
}
