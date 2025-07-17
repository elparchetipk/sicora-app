# Software Factory Service

A microservice for managing the Academic Software Factory (FSA) at SENA CGMLTI, built with Go and following Clean Architecture principles.

## Overview

The Software Factory Service is part of the SICORA multistack ecosystem and provides comprehensive management for:

- **Projects**: Academic software projects with learning objectives and technical requirements
- **Teams**: Development teams with role-based assignments and rotation schedules
- **Sprints**: Agile sprint management with academic evaluation integration
- **User Stories**: Academic and functional user stories with evaluation criteria
- **Evaluations**: Multi-dimensional evaluation system for technical and academic progress
- **Technologies**: Technology stack management and recommendations

## Features

- ✅ **Project Management**: Create and manage academic software projects
- ✅ **Team Organization**: Form teams with specialized roles and capacity management
- ✅ **Sprint Planning**: Agile sprint management with academic integration
- ✅ **Story Tracking**: User story management with academic objectives
- ✅ **Evaluation System**: Comprehensive evaluation framework
- ✅ **Technology Recommendations**: Smart technology stack suggestions
- ✅ **REST API**: Complete RESTful API with OpenAPI documentation
- ✅ **Clean Architecture**: Maintainable and testable codebase
- ✅ **PostgreSQL Integration**: Robust data persistence with GORM

## Architecture

This service follows Clean Architecture principles with the following layers:

```
├── cmd/server/                 # Application entry point
├── internal/
│   ├── domain/                # Business logic and entities
│   │   ├── entities/          # Domain entities
│   │   └── repositories/      # Repository interfaces
│   ├── application/           # Application layer
│   │   ├── dtos/             # Data transfer objects
│   │   └── usecases/         # Business use cases
│   └── infrastructure/       # External integrations
│       ├── config/           # Configuration management
│       ├── database/         # Database setup and migrations
│       └── http/             # HTTP handlers and routes
├── docs/                     # API documentation (Swagger)
├── tests/                    # Test files
├── Makefile                  # Build and development tasks
└── README.md                 # This file
```

## Requirements

- Go 1.23 or higher
- PostgreSQL 12 or higher
- Docker (optional)

## Quick Start

### 1. Clone and Setup

```bash
# Clone the repository (if not already done)
git clone <repository-url>
cd sicora-be-go/softwarefactoryservice

# Install dependencies
make deps
```

### 2. Configure Environment

Create a `.env` file or set environment variables:

```env
# Database Configuration
DB_HOST=localhost
DB_PORT=5432
DB_USER=postgres
DB_PASSWORD=your_password
DB_NAME=sicora_softwarefactory
DB_SSL_MODE=disable

# Server Configuration
SERVER_HOST=0.0.0.0
SERVER_PORT=8080

# Security
JWT_SECRET=your-secret-key

# Environment
ENVIRONMENT=development
```

### 3. Database Setup

```bash
# Make sure PostgreSQL is running
# Create the database
createdb sicora_softwarefactory

# Run migrations
make db-migrate
```

### 4. Run the Service

```bash
# Development mode (with auto-reload)
make dev

# Or build and run
make run

# Or use Docker
make docker-build
make docker-run
```

The service will be available at `http://localhost:8080`

## API Documentation

The service provides a complete REST API with OpenAPI/Swagger documentation.

### Generate Documentation

```bash
make swagger
```

### Access Documentation

Once the service is running, access the API documentation at:

- Swagger UI: `http://localhost:8080/docs/index.html`
- OpenAPI Spec: `http://localhost:8080/docs/swagger.json`

### Main Endpoints

| Endpoint                        | Method | Description        |
| ------------------------------- | ------ | ------------------ |
| `/api/v1/projects`              | GET    | List projects      |
| `/api/v1/projects`              | POST   | Create project     |
| `/api/v1/projects/{id}`         | GET    | Get project        |
| `/api/v1/projects/{id}`         | PUT    | Update project     |
| `/api/v1/projects/{id}`         | DELETE | Delete project     |
| `/api/v1/projects/{id}/stats`   | GET    | Project statistics |
| `/api/v1/teams`                 | GET    | List teams         |
| `/api/v1/teams`                 | POST   | Create team        |
| `/api/v1/teams/{id}/members`    | POST   | Add team member    |
| `/api/v1/sprints`               | GET    | List sprints       |
| `/api/v1/sprints`               | POST   | Create sprint      |
| `/api/v1/sprints/{id}/start`    | POST   | Start sprint       |
| `/api/v1/sprints/{id}/complete` | POST   | Complete sprint    |

## Development

### Available Make Commands

```bash
make help          # Show all available commands
make build         # Build the binary
make test          # Run tests
make test-coverage # Run tests with coverage
make fmt           # Format code
make lint          # Lint code
make clean         # Clean build artifacts
```

### Project Structure

The project follows Go standard layout and Clean Architecture:

- **Domain Layer**: Contains business entities and repository interfaces
- **Application Layer**: Contains use cases and DTOs
- **Infrastructure Layer**: Contains external integrations (database, HTTP)

### Testing

```bash
# Run all tests
make test

# Run tests with coverage
make test-coverage

# Run specific package tests
go test ./internal/domain/entities/...
```

### Code Quality

The project uses standard Go tools for code quality:

```bash
# Format code
make fmt

# Lint code (requires golangci-lint)
make lint
```

## Integration with SICORA

This service integrates with the SICORA ecosystem:

- **UserService**: User authentication and management
- **ScheduleService**: Academic schedule integration
- **NotificationService**: Event notifications
- **API Gateway**: Centralized API management

## Database Schema

The service uses PostgreSQL with the following main entities:

- `factory_projects`: Software projects
- `factory_teams`: Development teams
- `factory_team_members`: Team membership
- `factory_sprints`: Sprint management
- `factory_user_stories`: User stories
- `factory_evaluations`: Evaluation records
- `factory_technologies`: Technology catalog

## Configuration

The service can be configured through environment variables:

| Variable      | Description            | Default                |
| ------------- | ---------------------- | ---------------------- |
| `DB_HOST`     | Database host          | localhost              |
| `DB_PORT`     | Database port          | 5432                   |
| `DB_USER`     | Database user          | postgres               |
| `DB_PASSWORD` | Database password      | (required)             |
| `DB_NAME`     | Database name          | sicora_softwarefactory |
| `SERVER_PORT` | HTTP server port       | 8080                   |
| `JWT_SECRET`  | JWT signing key        | (required)             |
| `ENVIRONMENT` | Environment (dev/prod) | development            |

## Contributing

1. Follow Go coding standards
2. Write tests for new features
3. Update documentation
4. Follow Clean Architecture principles
5. Use conventional commit messages

## License

This project is part of the SENA CGMLTI academic ecosystem.

## Support

For questions or issues:

- Check the API documentation
- Review the test files for usage examples
- Contact the development team

---

**Software Factory Service** - Empowering Academic Software Development at SENA CGMLTI
