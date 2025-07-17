# Testing Suite - UserService Go

## Descripción

Suite completa de tests unitarios para el UserService implementado en Go. Los tests siguen las mejores prácticas de testing en Go utilizando testify para mocks y assertions.

## Estructura de Tests

```
tests/
├── entities/          # Tests de entidades de dominio
│   └── user_test.go
├── fixtures/          # Datos de prueba reutilizables
│   └── user_fixtures.go
├── handlers/          # Tests de handlers HTTP
│   └── user_handler_test.go
├── mocks/            # Mocks de interfaces
│   └── user_repository_mock.go
├── usecases/         # Tests de casos de uso
│   └── bulk_usecases_test.go
└── test_config.go    # Configuración global de tests
```

## Tipos de Tests Implementados

### 1. Tests de Entidades (Domain Tests)
**Archivo**: `tests/entities/user_test.go`

Prueban la lógica de negocio de las entidades:
- `TestUser_NewUser` - Creación de usuarios con validaciones
- `TestUser_GetFullName` - Obtención de nombre completo
- `TestUser_Activate/Deactivate` - Cambios de estado
- `TestUser_SetPassword` - Manejo de contraseñas
- `TestUser_CheckPassword` - Verificación de contraseñas
- `TestUser_IsAprendiz/IsInstructor/IsAdmin` - Verificación de roles
- `TestUser_CanManageUsers` - Permisos de gestión
- `TestUserRole_IsValid` - Validación de roles

### 2. Tests de Use Cases (Application Tests)
**Archivos**: 
- `internal/application/usecases/user_usecases_test.go`
- `tests/usecases/bulk_usecases_test.go`

Prueban la lógica de aplicación:
- `TestCreateUserUseCase_Execute` - Creación de usuarios
- `TestGetUserUseCase_Execute` - Obtención de usuarios
- `TestBulkUserUseCases_BulkCreateUsers` - Creación masiva
- `TestBulkUserUseCases_BulkUpdateUsers` - Actualización masiva
- `TestBulkUserUseCases_BulkDeleteUsers` - Eliminación masiva
- `TestBulkUserUseCases_BulkChangeStatus` - Cambio de estado masivo

### 3. Tests de Handlers (Presentation Tests)
**Archivo**: `tests/handlers/user_handler_test.go`

Prueban los endpoints HTTP:
- `TestUserHandler_CreateUser` - Endpoint de creación
- `TestUserHandler_BulkCreateUsers` - Endpoint de creación masiva
- Tests de validación de JSON
- Tests de respuestas HTTP

### 4. Mocks
**Archivo**: `tests/mocks/user_repository_mock.go`

Mock completo del UserRepository con todos los métodos:
- Métodos CRUD básicos
- Métodos de bulk operations
- Métodos de consulta especializados

### 5. Fixtures (Datos de Prueba)
**Archivo**: `tests/fixtures/user_fixtures.go`

Datos de prueba reutilizables:
- `NewValidUser()` - Usuario aprendiz válido
- `NewValidInstructor()` - Instructor válido
- `NewValidAdmin()` - Administrador válido
- `NewCreateUserRequest()` - Request de creación
- `NewBulkCreateUserRequest()` - Request de creación masiva
- `NewBulkUpdateUserRequest()` - Request de actualización masiva
- Funciones helper para punteros

## Comandos de Ejecución

### Ejecutar Todos los Tests
```bash
# Desde la raíz del proyecto
cd 02-go/userservice
go test ./...

# Con verbose output
go test -v ./...

# Con coverage
go test -v -cover ./...

# Coverage detallado
go test -v -coverprofile=coverage.out ./...
go tool cover -html=coverage.out
```

### Ejecutar Tests Específicos
```bash
# Solo tests de entidades
go test -v ./tests/entities/

# Solo tests de use cases
go test -v ./internal/application/usecases/
go test -v ./tests/usecases/

# Solo tests de handlers
go test -v ./tests/handlers/

# Test específico por función
go test -v -run TestUser_NewUser ./tests/entities/

# Tests de bulk operations
go test -v -run TestBulk ./tests/usecases/
```

### Ejecutar Tests con Benchmarks
```bash
# Tests con benchmarks
go test -v -bench=. ./...

# Solo benchmarks
go test -bench=. -run=^$ ./...
```

## Configuración de Testing

### Variables de Entorno
Los tests utilizan las siguientes variables de entorno configuradas automáticamente:
```bash
GIN_MODE=test
JWT_SECRET=test-secret-key-for-testing-only
DB_HOST=localhost
DB_PORT=5432
DB_NAME=sicora_userservice_test
DB_USER=sicora_user
DB_PASSWORD=sicora_password
LOG_LEVEL=error
```

### Base de Datos de Test
Para tests de integración (cuando se implementen):
```bash
# Crear base de datos de test
createdb sicora_userservice_test

# Ejecutar migraciones de test
migrate -path ./migrations -database "postgres://sicora_user:sicora_password@localhost:5432/sicora_userservice_test?sslmode=disable" up
```

## Cobertura de Código

### Objetivos de Cobertura
- **Entidades**: 95%+ (lógica de dominio crítica)
- **Use Cases**: 90%+ (lógica de aplicación)
- **Handlers**: 85%+ (capa de presentación)
- **Repositories**: 80%+ (con tests de integración)

### Verificar Cobertura
```bash
# Generar reporte de cobertura
go test -coverprofile=coverage.out ./...
go tool cover -func=coverage.out

# Reporte HTML
go tool cover -html=coverage.out -o coverage.html
```

## Mejores Prácticas Implementadas

### 1. Principios AAA (Arrange, Act, Assert)
Todos los tests siguen la estructura:
```go
t.Run("test description", func(t *testing.T) {
    // Arrange - Setup test data and mocks
    
    // Act - Execute the function under test
    
    // Assert - Verify results
})
```

### 2. Mocks con Testify
```go
// Setup mock
mockRepo := new(mocks.MockUserRepository)
mockRepo.On("GetByEmail", ctx, email).Return(user, nil)

// Verify mock calls
mockRepo.AssertExpectations(t)
```

### 3. Fixtures para Datos de Prueba
```go
// Reutilizable y mantenible
user := fixtures.NewValidUser()
request := fixtures.NewCreateUserRequest()
```

### 4. Tests de Casos Edge
- Valores nulos/vacíos
- Errores de validación
- Errores de base de datos
- Casos límite

### 5. Nomenclatura Descriptiva
```go
func TestUser_SetPassword_EmptyPasswordFails(t *testing.T)
func TestBulkCreateUsers_SuccessfulCreation(t *testing.T)
```

## Tests de Performance

### Benchmarks
Para casos críticos como bulk operations:
```go
func BenchmarkBulkCreateUsers(b *testing.B) {
    // Setup
    for i := 0; i < b.N; i++ {
        // Test bulk creation performance
    }
}
```

### Load Testing
Para endpoints críticos:
```bash
# Con herramientas externas como vegeta
echo "POST http://localhost:8001/api/v1/users/bulk" | vegeta attack -duration=30s -rate=10 | vegeta report
```

## Integración Continua

### GitHub Actions (ejemplo)
```yaml
- name: Run Tests
  run: |
    cd 02-go/userservice
    go test -v -race -coverprofile=coverage.out ./...
    go tool cover -func=coverage.out
```

### Pre-commit Hooks
```bash
# Ejecutar tests antes de cada commit
#!/bin/sh
cd 02-go/userservice
go test ./...
```

## Depuración de Tests

### Tests Fallidos
```bash
# Ejecutar con información detallada
go test -v -failfast ./...

# Debug específico
go test -v -run TestSpecificFunction ./package/
```

### Tests Lentos
```bash
# Identificar tests lentos
go test -v -timeout 30s ./...
```

## Mantenimiento

### Actualizar Mocks
Cuando se modifique la interfaz del repositorio:
1. Actualizar `tests/mocks/user_repository_mock.go`
2. Ejecutar tests para verificar compatibilidad
3. Actualizar fixtures si es necesario

### Agregar Nuevos Tests
1. Seguir la estructura de carpetas existente
2. Usar fixtures existentes cuando sea posible
3. Mantener cobertura de código alta
4. Documentar tests complejos

## Herramientas Recomendadas

### IDEs
- **VS Code**: Con extensión Go
- **GoLand**: IDE especializado para Go

### Extensiones Útiles
- Go Test Explorer (VS Code)
- Coverage Gutters (VS Code)
- Test output colorization

### Línea de Comandos
```bash
# Alias útiles
alias gotest="go test -v ./..."
alias gocover="go test -v -cover ./..."
alias gocoverhtml="go test -coverprofile=coverage.out ./... && go tool cover -html=coverage.out"
```
