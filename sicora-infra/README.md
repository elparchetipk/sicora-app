# SICORA Infrastructure

## Descripción
Repositorio de infraestructura y DevOps para el ecosistema SICORA. Contiene configuraciones de Docker, Kubernetes, CI/CD, monitoreo y seguridad compartidas entre todos los stacks del proyecto.

## Estructura del Proyecto

```
sicora-infra/
├── docker/                 # Configuraciones Docker
│   ├── base/               # Imágenes base reutilizables
│   ├── services/           # Configuraciones específicas por servicio
│   ├── development/        # Configuración para desarrollo
│   └── production/         # Configuración para producción
├── k8s/                    # Manifiestos Kubernetes
│   ├── base/               # Configuraciones base
│   ├── development/        # Ambiente de desarrollo
│   ├── production/         # Ambiente de producción
│   └── monitoring/         # Configuraciones de monitoreo
├── nginx/                  # Configuraciones Nginx
│   ├── configs/            # Archivos de configuración
│   ├── ssl/                # Certificados SSL
│   └── templates/          # Plantillas de configuración
├── ci-cd/                  # Pipelines CI/CD
│   ├── github-actions/     # GitHub Actions workflows
│   ├── jenkins/            # Jenkins pipelines
│   └── gitlab-ci/          # GitLab CI configurations
├── monitoring/             # Stack de monitoreo
│   ├── prometheus/         # Configuración Prometheus
│   ├── grafana/            # Dashboards Grafana
│   └── alertmanager/       # Configuración AlertManager
├── security/               # Políticas y configuraciones de seguridad
│   ├── policies/           # Políticas de seguridad
│   └── configs/            # Configuraciones de seguridad
├── scripts/                # Scripts de automatización
│   ├── deployment/         # Scripts de despliegue
│   ├── maintenance/        # Scripts de mantenimiento
│   └── backup/             # Scripts de respaldo
├── docs/                   # Documentación
│   ├── setup/              # Guías de instalación
│   ├── deployment/         # Guías de despliegue
│   └── troubleshooting/    # Resolución de problemas
└── environments/           # Configuraciones por ambiente
    ├── dev/                # Desarrollo
    ├── staging/            # Staging
    └── prod/               # Producción
```

## Tecnologías Utilizadas

- **Docker & Docker Compose**: Containerización
- **Kubernetes**: Orquestación de contenedores
- **Nginx**: Reverse proxy y load balancer
- **PostgreSQL 15**: Base de datos principal
- **Prometheus + Grafana**: Monitoreo y métricas
- **GitHub Actions**: CI/CD
- **SonarQube**: Análisis de código

## Requisitos

- Docker 24+
- Docker Compose v2+
- Kubernetes 1.28+
- Nginx 1.25+
- PostgreSQL 15

## Configuración Rápida

1. **Clonar el repositorio**:
   ```bash
   git clone <sicora-infra-repo>
   cd sicora-infra
   ```

2. **Configurar variables de entorno**:
   ```bash
   cp environments/dev/.env.example environments/dev/.env
   # Editar variables según el ambiente
   ```

3. **Iniciar servicios de desarrollo**:
   ```bash
   docker compose -f docker/development/docker-compose.yml up -d
   ```

## Uso en Otros Repositorios

### Como Submódulo Git

```bash
# Agregar sicora-infra como submódulo
git submodule add <sicora-infra-repo> infra

# Inicializar submódulos
git submodule update --init --recursive
```

### Referencia Directa

```bash
# Clonar sicora-infra en paralelo
git clone <sicora-infra-repo> ../sicora-infra

# Usar configuraciones desde otros proyectos
docker compose -f ../sicora-infra/docker/development/docker-compose.yml up -d
```

## Ambientes

### Desarrollo (dev)
- Servicios locales con Docker Compose
- Base de datos PostgreSQL 15 local
- Hot reload habilitado
- Logs detallados

### Staging (staging)
- Réplica del ambiente de producción
- Tests de integración automatizados
- Datos de prueba

### Producción (prod)
- Kubernetes cluster
- Alta disponibilidad
- Monitoreo completo
- Backups automatizados

## Monitoreo

- **Prometheus**: Recolección de métricas
- **Grafana**: Visualización de dashboards
- **AlertManager**: Notificaciones y alertas
- **Logs centralizados**: ELK Stack (opcional)

## Seguridad

- Políticas de seguridad definidas
- Análisis de vulnerabilidades con SonarQube
- Certificados SSL/TLS automatizados
- Secrets management con Kubernetes secrets

## Contribución

1. Fork del repositorio
2. Crear rama feature: `git checkout -b feature/nueva-funcionalidad`
3. Commit cambios: `git commit -am 'feat: agregar nueva funcionalidad'`
4. Push a la rama: `git push origin feature/nueva-funcionalidad`
5. Crear Pull Request

## Licencia

[Especificar licencia del proyecto]

## Soporte

Para problemas o preguntas, crear un issue en el repositorio o contactar al equipo de DevOps.
