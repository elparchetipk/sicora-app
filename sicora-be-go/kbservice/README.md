# SICORA KbService - Knowledge Base Service

## Overview

The **KbService** (Knowledge Base Service) is a microservice component of the SICORA application ecosystem, designed to manage documentation, FAQs, semantic search, and knowledge analytics. Built following Clean Architecture principles, it provides a robust and scalable solution for knowledge management.

## 🚀 Current Implementation Status

### ✅ Completed Features

- **Clean Architecture structure** implemented
- **Database entities** for Documents, FAQs, and Analytics
- **GORM repository layer** with PostgreSQL support
- **pgvector integration** for semantic search capabilities
- **Basic CRUD operations** for Documents and FAQs
- **Analytics tracking** infrastructure
- **Docker containerization** ready
- **Health check endpoints**
- **Middleware support** (CORS, logging, recovery)

### 🔄 In Progress

- Full semantic search implementation
- AI service integration
- Complete analytics dashboard
- Authentication and authorization
- Comprehensive testing suite

### 📋 Planned Features

- Swagger/OpenAPI documentation
- Advanced workflow management
- Real-time notifications
- Performance monitoring
- Automated content suggestions

## Features

### 📚 Document Management

- **Full CRUD operations** for documents
- **Versioning system** with rollback capabilities
- **Hierarchical document structure** (parent-child relationships)
- **Rich metadata support** (tags, keywords, categories, audiences)
- **Multiple document types** (tutorials, API docs, troubleshooting guides, etc.)
- **Approval workflow** (draft → review → approved → published)
- **SEO optimization** with meta titles and descriptions

### ❓ FAQ Management

- **Dynamic FAQ system** with scoring algorithms
- **AI-powered suggestions** from user interactions
- **Rating and feedback system** (helpful/unhelpful)
- **Popularity and relevance scoring**
- **Priority-based organization**
- **Related content recommendations**

### 🔍 Advanced Search

- **Full-text search** using PostgreSQL's built-in capabilities
- **Semantic search** powered by vector embeddings (pgvector)
- **Multi-category filtering**
- **Audience-specific content**
- **Tag-based organization**
- **Relevance ranking**

### 📊 Analytics & Intelligence

- **Content performance metrics**
- **User engagement tracking**
- **Search pattern analysis**
- **Knowledge gap identification**
- **Real-time analytics dashboard**
- **Automated reporting**

### 🎯 Smart Features

- **AI-enhanced content generation**
- **Automatic tagging and categorization**
- **Reading time estimation**
- **Content summarization**
- **Related content suggestions**
- **Unanswered question detection**

## Architecture

### Clean Architecture Layers

```
cmd/
├── server/                 # Application entry point
internal/
├── domain/                # Business logic (entities, interfaces)
│   ├── entities/          # Core business entities
│   └── repositories/      # Repository interfaces
├── application/           # Application services
│   ├── dto/              # Data Transfer Objects
│   └── usecases/         # Business use cases
├── infrastructure/       # External concerns
│   ├── database/         # Database configuration
│   └── repositories/     # Repository implementations
└── presentation/         # Interface layer
    ├── handlers/         # HTTP handlers
    ├── routes/          # Route definitions
    └── middleware/      # HTTP middleware
```

### Technology Stack

- **Language**: Go 1.23
- **Framework**: Gin (HTTP router)
- **Database**: PostgreSQL 16 with pgvector extension
- **ORM**: GORM
- **Search**: PostgreSQL full-text + Vector similarity
- **Caching**: Redis (optional)
- **Monitoring**: Prometheus + Grafana
- **Documentation**: Swagger/OpenAPI
- **Containerization**: Docker + Docker Compose

## Getting Started

### Prerequisites

- Go 1.23 or higher
- Docker and Docker Compose
- PostgreSQL 16 with pgvector extension
- Make (for running Makefile commands)

### Quick Start

1. **Clone the repository**

   ```bash
   git clone <repository-url>
   cd kbservice
   ```

2. **Start development environment**

   ```bash
   make dev
   ```

3. **The service will be available at:**
   - API: http://localhost:8080
   - Health check: http://localhost:8080/health
   - Database: localhost:5432
   - Grafana: http://localhost:3000 (admin/admin)

### Manual Setup

1. **Install dependencies**

   ```bash
   make deps
   ```

2. **Start supporting services**

   ```bash
   make docker-up
   ```

3. **Run the application**
   ```bash
   make run
   ```

## Configuration

### Environment Variables

Copy `.env.example` to `.env` and configure:

```env
# Database
DB_HOST=localhost
DB_PORT=5432
DB_USER=postgres
DB_PASSWORD=postgres
DB_NAME=sicora_kb

# Server
PORT=8080
GIN_MODE=debug

# Optional AI Service
AI_SERVICE_URL=http://localhost:8081
AI_SERVICE_API_KEY=your-api-key
```

### Database Setup

The service automatically:

- Creates required tables
- Sets up pgvector extension
- Creates optimized indexes
- Sets up full-text search triggers

## API Documentation

### Core Endpoints

#### Documents

- `POST /api/v1/documents` - Create document
- `GET /api/v1/documents/:id` - Get document
- `PUT /api/v1/documents/:id` - Update document
- `DELETE /api/v1/documents/:id` - Delete document
- `GET /api/v1/documents` - Search documents
- `POST /api/v1/documents/search/semantic` - Semantic search

#### FAQs

- `POST /api/v1/faqs` - Create FAQ
- `GET /api/v1/faqs/:id` - Get FAQ
- `GET /api/v1/faqs` - Search FAQs
- `POST /api/v1/faqs/:id/rate` - Rate FAQ
- `GET /api/v1/faqs/popular` - Get popular FAQs

#### Analytics

- `GET /api/v1/analytics/content` - Content statistics
- `GET /api/v1/analytics/engagement` - User engagement
- `GET /api/v1/analytics/realtime` - Real-time metrics

### Authentication

The service expects user information in headers:

- `X-User-ID`: User UUID
- `X-User-Role`: User role (ADMIN, INSTRUCTOR, STUDENT, etc.)

## Development

### Common Commands

```bash
# Development
make dev          # Start full development environment
make run          # Run application only
make test         # Run tests
make test-cover   # Run tests with coverage

# Code Quality
make lint         # Run linter
make format       # Format code
make check        # Run all checks

# Database
make migrate      # Run migrations
make db-reset     # Reset database
make seed         # Load sample data

# Docker
make docker-up    # Start services
make docker-down  # Stop services
make docker-logs  # View logs
```

### Testing

```bash
# Unit tests
go test ./...

# Integration tests
go test -tags=integration ./...

# Benchmarks
go test -bench=. ./...

# Coverage
make test-cover
```

### Code Style

- Follow Go best practices
- Use gofmt for formatting
- Run golangci-lint before commits
- Write comprehensive tests
- Document public APIs

## Deployment

### Docker Production

```bash
# Build production image
make docker-prod

# Run with docker-compose
docker-compose -f docker-compose.prod.yml up -d
```

### Environment-specific Configurations

- **Development**: Full logging, debug mode
- **Staging**: Reduced logging, performance monitoring
- **Production**: Minimal logging, security hardening

## Monitoring and Observability

### Metrics (Prometheus)

- Request duration and count
- Database query performance
- Cache hit/miss rates
- Error rates and types
- Business metrics (content views, searches)

### Logging

- Structured JSON logging
- Request tracing
- Error tracking
- Performance metrics

### Health Checks

- `/health` - Basic health status
- `/ready` - Readiness for traffic
- Database connectivity
- External service availability

## Performance Considerations

### Database Optimization

- **Indexes**: Optimized for common query patterns
- **Vector Search**: HNSW indexes for semantic search
- **Full-text Search**: PostgreSQL built-in capabilities
- **Connection Pooling**: Configured for optimal performance

### Caching Strategy

- **Application-level**: Frequent queries cached
- **Database-level**: Query result caching
- **CDN**: Static content caching

### Search Performance

- **Hybrid Search**: Combines full-text and semantic search
- **Index Management**: Automatic index optimization
- **Query Optimization**: Efficient query patterns

## Security

### Data Protection

- Input validation and sanitization
- SQL injection prevention (GORM ORM)
- XSS protection
- Rate limiting

### Access Control

- Role-based access control (RBAC)
- Multi-tenant support
- Audit logging
- Secure headers

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests
5. Run quality checks: `make check`
6. Submit a pull request

### Development Guidelines

- Follow Clean Architecture principles
- Write tests for new features
- Update documentation
- Follow Git commit conventions
- Ensure backward compatibility

## Troubleshooting

### Common Issues

1. **Database Connection Issues**

   ```bash
   make docker-up  # Ensure PostgreSQL is running
   make db-reset   # Reset database if corrupted
   ```

2. **Vector Extension Not Available**

   ```bash
   # Use pgvector/pgvector Docker image
   docker-compose up postgres
   ```

3. **Performance Issues**

   ```bash
   # Check database indexes
   make db-analyze

   # Monitor metrics
   # Visit http://localhost:3000 (Grafana)
   ```

### Debugging

```bash
# Enable debug logging
export GIN_MODE=debug

# View detailed logs
make logs

# Database queries
export DB_LOG_LEVEL=info
```

## Roadmap

### Phase 1 (Current)

- ✅ Core document and FAQ management
- ✅ Basic search functionality
- ✅ Analytics foundation
- ✅ Clean architecture implementation

### Phase 2 (Next)

- 🔄 AI service integration
- 🔄 Advanced search features
- 🔄 Real-time collaboration
- 🔄 Enhanced analytics

### Phase 3 (Future)

- 📋 Machine learning recommendations
- 📋 Multi-language support
- 📋 Advanced workflow automation
- 📋 Integration with external systems

## License

This project is part of the SICORA application ecosystem. See the main repository for license information.

## Support

For support and questions:

- Create an issue in the repository
- Check the documentation
- Review the troubleshooting guide

---

**SICORA KbService** - Empowering knowledge management with AI-driven insights and semantic search capabilities.
