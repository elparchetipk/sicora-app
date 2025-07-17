# Instalación de Dependencias de Testing

Para ejecutar la suite de tests, necesitas instalar las dependencias de testing.

## Instalar testify para mocks y assertions

```bash
go get -u github.com/stretchr/testify/assert
go get -u github.com/stretchr/testify/mock
go get -u github.com/stretchr/testify/suite
```

## Ejecutar el comando para actualizar go.mod

```bash
cd 02-go/userservice
go mod tidy
```

## Verificar instalación ejecutando tests

```bash
# Ejecutar todos los tests
go test ./...

# Ejecutar tests con verbose output
go test -v ./...

# Ejecutar tests con cobertura
go test -v -cover ./...
```

## Comandos de desarrollo

```bash
# Limpiar caché de tests
go clean -testcache

# Ejecutar tests en modo watch (requiere entr o similar)
find . -name "*.go" | entr -r go test ./...

# Ejecutar tests específicos
go test -v -run TestBulk ./tests/usecases/
```

Nota: Los tests utilizan mocks, por lo que no requieren una base de datos real para ejecutarse.
