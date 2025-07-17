# 📚 Swagger & SonarQube Implementation Guide

## 🎯 Estado Actual - Implementación Iniciada

### **✅ COMPLETADO**

#### **Express UserService:**

- ✅ Swagger/OpenAPI completo configurado
- ✅ Disponible en `/api/docs`
- ✅ Schemas definidos y documentados

#### **Next.js UserService:**

- ✅ Swagger/OpenAPI completo configurado
- ✅ Disponible en `/api/docs`
- ✅ TypeScript completamente integrado

#### **FastAPI:**

- ✅ Swagger built-in funcional
- ✅ Documentación automática en `/docs`

### **🚧 EN PROGRESO**

#### **Go UserService:**

- ✅ Dependencias agregadas a `go.mod`
- ✅ Imports configurados en `main.go`
- ✅ Endpoints Swagger configurados en `/docs` y `/swagger`
- ✅ Anotaciones Swagger agregadas a handlers
- ❌ **PENDIENTE**: Ejecutar comandos para completar

## 🔧 Comandos Requeridos para Completar

### **1. Go UserService - Finalizar Swagger**

```bash
# Navegar al directorio Go
cd 02-go/userservice

# Descargar dependencias
go mod tidy

# Instalar herramienta swag (si no está instalada)
go install github.com/swaggo/swag/cmd/swag@latest

# Generar documentación Swagger
swag init

# Ejecutar el servidor
go run main.go
```

**Verificación:**

- Swagger UI: `http://localhost:8002/docs/index.html`
- OpenAPI JSON: `http://localhost:8002/swagger/doc.json`

### **2. Java Spring Boot - Implementar Swagger**

```bash
cd 05-springboot-java/userservice
```

**Agregar a `pom.xml`:**

```xml
<dependency>
    <groupId>org.springdoc</groupId>
    <artifactId>springdoc-openapi-starter-webmvc-ui</artifactId>
    <version>2.3.0</version>
</dependency>
```

**Comandos:**

```bash
# Compilar con nueva dependencia
mvn clean compile

# Ejecutar aplicación
mvn spring-boot:run
```

**Verificación:**

- Swagger UI: `http://localhost:8005/swagger-ui.html`
- OpenAPI JSON: `http://localhost:8005/v3/api-docs`

### **3. Kotlin Spring Boot - Implementar Swagger**

```bash
cd 06-springboot-kotlin/userservice
```

**Agregar a `build.gradle.kts`:**

```kotlin
implementation("org.springdoc:springdoc-openapi-starter-webmvc-ui:2.3.0")
```

**Comandos:**

```bash
# Compilar con nueva dependencia
./gradlew build

# Ejecutar aplicación
./gradlew bootRun
```

**Verificación:**

- Swagger UI: `http://localhost:8006/swagger-ui.html`
- OpenAPI JSON: `http://localhost:8006/v3/api-docs`

## 📊 SonarQube Configuration

### **Configuración Central Actualizada**

**Archivo:** `sonar-project.properties` (raíz del proyecto)

```properties
# Multistack SonarQube Configuration
sonar.projectKey=sicora-app-multistack
sonar.projectName=SICORA-APP Backend Multistack
sonar.organization=sicora
sonar.projectVersion=1.0.0

# Modules
sonar.modules=fastapi,express,nextjs,go,java,kotlin

# FastAPI
fastapi.sonar.projectName=FastAPI Services
fastapi.sonar.sources=01-fastapi
fastapi.sonar.language=py
fastapi.sonar.exclusions=**/venv/**,**/__pycache__/**,**/migrations/**

# Express
express.sonar.projectName=Express UserService
express.sonar.sources=03-express/userservice/src
express.sonar.language=js
express.sonar.exclusions=**/node_modules/**,**/coverage/**

# Next.js
nextjs.sonar.projectName=Next.js UserService
nextjs.sonar.sources=04-nextjs/userservice/src,04-nextjs/userservice/pages/api
nextjs.sonar.language=ts
nextjs.sonar.exclusions=**/node_modules/**,**/.next/**

# Go
go.sonar.projectName=Go UserService
go.sonar.sources=02-go/userservice
go.sonar.language=go
go.sonar.exclusions=**/vendor/**,**/docs/**

# Java
java.sonar.projectName=Java Spring Boot UserService
java.sonar.sources=05-springboot-java/userservice/src/main/java
java.sonar.language=java
java.sonar.exclusions=**/target/**

# Kotlin
kotlin.sonar.projectName=Kotlin Spring Boot UserService
kotlin.sonar.sources=06-springboot-kotlin/userservice/src/main/kotlin
kotlin.sonar.language=kotlin
kotlin.sonar.exclusions=**/build/**
```

### **Comandos SonarQube por Stack**

#### **Express.js:**

```bash
cd 03-express/userservice

# Instalar sonar-scanner
npm install -g sonarqube-scanner

# Ejecutar análisis
sonar-scanner
```

#### **Next.js:**

```bash
cd 04-nextjs/userservice

# Ejecutar análisis TypeScript
sonar-scanner -Dsonar.typescript.lcov.reportPaths=coverage/lcov.info
```

#### **Go:**

```bash
cd 02-go/userservice

# Ejecutar tests con coverage
go test -coverprofile=coverage.out ./...

# Análisis SonarQube
sonar-scanner -Dsonar.go.coverage.reportPaths=coverage.out
```

#### **Java:**

```bash
cd 05-springboot-java/userservice

# Ejecutar tests con JaCoCo
mvn clean test jacoco:report

# Análisis SonarQube
mvn sonar:sonar
```

#### **Kotlin:**

```bash
cd 06-springboot-kotlin/userservice

# Ejecutar tests con JaCoCo
./gradlew test jacocoTestReport

# Análisis SonarQube
./gradlew sonarqube
```

## 🎓 Resultados Esperados

### **Swagger/OpenAPI URLs:**

- **FastAPI**: `http://localhost:8001/docs`
- **Go**: `http://localhost:8002/docs/index.html`
- **Express**: `http://localhost:8003/api/docs`
- **Next.js**: `http://localhost:8004/api/docs`
- **Java**: `http://localhost:8005/swagger-ui.html`
- **Kotlin**: `http://localhost:8006/swagger-ui.html`

### **Funcionalidades Disponibles:**

1. **Documentación interactiva** - Try it out functionality
2. **Schemas validados** - Request/Response models
3. **Autenticación integrada** - Bearer token support
4. **Ejemplos automáticos** - Sample requests
5. **Exportación OpenAPI** - JSON/YAML specs

### **SonarQube Benefits:**

1. **Code quality metrics** unificadas
2. **Security vulnerabilities** detection
3. **Code smells** identification
4. **Technical debt** quantification
5. **Coverage reports** consolidados

## 📋 Checklist de Verificación

### **Swagger Implementation:**

- [ ] Go: Documentación generada con `swag init`
- [ ] Java: SpringDoc dependency agregada
- [ ] Kotlin: SpringDoc configurado con Gradle
- [ ] All Stacks: Swagger UI accesible
- [ ] All Stacks: OpenAPI JSON disponible

### **SonarQube Setup:**

- [ ] Central config actualizada
- [ ] Individual scanners configurados
- [ ] Coverage reports generados
- [ ] Quality gates definidos
- [ ] CI/CD integration preparada

### **Documentation Quality:**

- [ ] API endpoints documentados
- [ ] Request/Response schemas definidos
- [ ] Authentication methods descritos
- [ ] Error responses especificados
- [ ] Examples provided for complex operations

Esta implementación establecerá un **estándar profesional** de documentación y calidad de código en todo el proyecto multistack.
