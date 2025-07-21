# Tests de Integración - Backend Python SICORA

## 📋 Estructura de Tests

```
tests/
├── conftest.py                 # Configuración global de tests
├── integration/               # Tests de integración
│   ├── __init__.py
│   ├── test_apigateway_integration.py
│   ├── test_notification_integration.py
│   ├── test_userservice_integration.py
│   └── test_cross_service_integration.py
├── unit/                      # Tests unitarios
│   ├── __init__.py
│   ├── apigateway/
│   ├── notification/
│   └── userservice/
└── fixtures/                  # Datos de prueba
    ├── __init__.py
    ├── database_fixtures.py
    └── api_fixtures.py
```

## 🎯 Cobertura de Tests

### Tests de Integración

- [x] Conectividad de base de datos
- [x] Endpoints de health y métricas
- [ ] Flujos completos de API
- [ ] Integración entre servicios
- [ ] Tests de performance básicos

### Tests Unitarios

- [ ] Modelos de dominio
- [ ] Servicios de aplicación
- [ ] Repositorios
- [ ] Controllers/Routers

## 🚀 Comandos de Ejecución

```bash
# Ejecutar todos los tests
pytest

# Solo tests de integración
pytest -m integration

# Solo tests unitarios
pytest -m unit

# Tests con cobertura
pytest --cov=. --cov-report=html

# Tests específicos
pytest tests/integration/test_apigateway_integration.py
```

## 📊 Métricas Objetivo

- **Cobertura**: > 80%
- **Tests de integración**: > 90% de endpoints
- **Tests unitarios**: > 85% de funciones críticas
- **Performance**: < 200ms promedio por endpoint
