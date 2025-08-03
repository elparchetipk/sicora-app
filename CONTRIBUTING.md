# Contributing to SICORA

<div align="center">

![SICORA Logo](./assets/logo-sicora-small.svg)

</div>

¡Gracias por tu interés en contribuir a SICORA! Este documento proporciona pautas para contribuir al proyecto.

## 📋 Tabla de Contenidos

- [Código de Conducta](#código-de-conducta)
- [Cómo Contribuir](#cómo-contribuir)
- [Configuración del Entorno](#configuración-del-entorno)
- [Proceso de Desarrollo](#proceso-de-desarrollo)
- [Estándares de Código](#estándares-de-código)
- [Reportar Bugs](#reportar-bugs)
- [Solicitar Características](#solicitar-características)
- [Pull Requests](#pull-requests)
- [Documentación](#documentación)

## 🤝 Código de Conducta

Este proyecto sigue el [Contributor Covenant Code of Conduct](CODE_OF_CONDUCT.md). Al participar, se espera que mantengas este código.

## 🚀 Cómo Contribuir

### Tipos de Contribuciones Bienvenidas

- 🐛 **Reportes de bugs** - Ayúdanos a encontrar y corregir problemas
- ✨ **Nuevas características** - Propone mejoras al sistema
- 📚 **Documentación** - Mejora la documentación existente
- 🧪 **Pruebas** - Agrega o mejora tests
- 🔧 **Herramientas** - Scripts y utilidades de desarrollo
- 🌍 **Traducciones** - Internacionalización del sistema

### Primeros Pasos

1. **Fork el repositorio** en GitHub
2. **Clona tu fork** localmente
3. **Configura el entorno** siguiendo las instrucciones
4. **Crea una rama** para tu contribución
5. **Hace tus cambios** siguiendo los estándares
6. **Haz push** y crea un Pull Request

## ⚙️ Configuración del Entorno

### Prerrequisitos

- **Node.js** 18+ y **pnpm**
- **Python** 3.9+ y **pip**
- **Go** 1.21+
- **Docker** y **Docker Compose**
- **Git** configurado

### Configuración Inicial

```bash
# Clonar el repositorio
git clone https://github.com/onevision/sicora-app.git
cd sicora-app

# Configuración Git inicial (configuración mínima para desarrollo)
./scripts/init-git-sicora.sh

# Instalar dependencias del frontend
cd sicora-app-fe
pnpm install

# Configurar infraestructura Docker
cd ../sicora-infra/docker
docker compose up -d

# Verificar servicios
cd ../..
./scripts/health-check-services.sh status
```

### Verificación del Entorno

```bash
# Verificar que todo funciona
./scripts/diagnose-docker-network.sh

# Ejecutar tests básicos
cd sicora-app-fe && pnpm test
cd ../sicora-be-go && make test
cd ../sicora-be-python && make test
```

## 🔄 Proceso de Desarrollo

### Flujo de Trabajo

1. **Crea una issue** antes de hacer cambios grandes
2. **Asígnate la issue** o comenta que trabajarás en ella
3. **Crea una rama** desde `main` con nombre descriptivo
4. **Desarrolla con commits pequeños** y descriptivos
5. **Mantén la rama actualizada** con `main`
6. **Ejecuta tests** antes de hacer push
7. **Crea Pull Request** con descripción detallada

### Nomenclatura de Ramas

```bash
# Nuevas características
feature/nombre-caracteristica

# Corrección de bugs
fix/descripcion-bug

# Documentación
docs/que-documentas

# Refactoring
refactor/area-refactorizada

# Ejemplos
feature/user-authentication
fix/docker-network-errors
docs/contributing-guide
refactor/frontend-components
```

### Commits

Usamos [Conventional Commits](https://www.conventionalcommits.org/):

```bash
# Formato
<type>[optional scope]: <description>

# Tipos válidos
feat:     Nueva característica
fix:      Corrección de bug
docs:     Documentación
style:    Formato (sin cambios de código)
refactor: Refactoring
test:     Agregar/modificar tests
chore:    Tareas de mantenimiento
perf:     Mejoras de rendimiento
ci:       Integración continua
build:    Sistema de build

# Ejemplos
feat(auth): add JWT token refresh mechanism
fix(docker): resolve network connectivity issues
docs: update contributing guidelines
test(frontend): add user component tests
```

## 📝 Estándares de Código

### Frontend (React + TypeScript)

```bash
# Linting y formato
pnpm lint
pnpm format

# Tests
pnpm test
pnpm test:coverage
```

**Estándares**:

- ESLint + Prettier configurados
- TypeScript estricto
- Tests con Vitest
- Componentes funcionales con hooks
- Styled components o Tailwind CSS

### Backend Go

```bash
# Formato y linting
gofmt -w .
golint ./...
go vet ./...

# Tests
make test
make test-coverage
```

**Estándares**:

- Go modules para dependencias
- Clean Architecture
- Tests unitarios obligatorios
- Documentación en código (godoc)
- Error handling explícito

### Backend Python

```bash
# Formato y linting
black .
flake8 .
mypy .

# Tests
pytest
pytest --cov
```

**Estándares**:

- Black para formato
- Type hints obligatorios
- Docstrings en funciones públicas
- Tests con pytest
- Virtual environments

### Docker

```bash
# Verificar configuración
./scripts/diagnose-docker-network.sh

# Tests de integración
./scripts/health-check-services.sh
```

**Estándares**:

- Dockerfiles optimizados (multi-stage)
- docker-compose para desarrollo
- Variables de entorno documentadas
- Health checks en servicios

## 🐛 Reportar Bugs

### Antes de Reportar

1. **Busca issues existentes** para evitar duplicados
2. **Reproduce el bug** de manera consistente
3. **Verifica con la última versión** del código

### Template de Bug Report

```markdown
**Descripción del Bug**
Descripción clara y concisa del problema.

**Para Reproducir**
Pasos para reproducir el comportamiento:

1. Ir a '...'
2. Hacer click en '....'
3. Scrollear hasta '....'
4. Ver error

**Comportamiento Esperado**
Descripción clara de lo que esperabas que pasara.

**Screenshots**
Si aplica, agregar screenshots para explicar el problema.

**Entorno (completa la siguiente información):**

- OS: [ej. Ubuntu 22.04]
- Browser [ej. chrome, safari]
- Versión [ej. 22]
- Node.js version: [ej. 18.16.0]
- Docker version: [ej. 24.0.2]

**Contexto Adicional**
Cualquier otro contexto sobre el problema.

**Logs**
```

Pegar logs relevantes aquí

```

```

## ✨ Solicitar Características

### Template de Feature Request

```markdown
**¿Tu feature request está relacionada a un problema? Describe.**
Descripción clara del problema. Ej. Estoy siempre frustrado cuando [...]

**Describe la solución que te gustaría**
Descripción clara y concisa de lo que quieres que pase.

**Describe alternativas que hayas considerado**
Descripción clara de soluciones o características alternativas.

**Contexto adicional**
Cualquier otro contexto o screenshots sobre el feature request.

**Impacto esperado**

- [ ] Mejora la experiencia de usuario
- [ ] Mejora el rendimiento
- [ ] Facilita el desarrollo
- [ ] Mejora la seguridad
- [ ] Otro: ****\_\_\_****
```

## 🔀 Pull Requests

### Antes de Crear un PR

1. **Asegúrate de que la rama esté actualizada** con `main`
2. **Ejecuta todos los tests** y que pasen
3. **Verifica el linting** y formato de código
4. **Actualiza documentación** si es necesario
5. **Agrega tests** para nueva funcionalidad

### Template de Pull Request

```markdown
## Descripción

Breve descripción de los cambios realizados.

## Tipo de cambio

- [ ] Bug fix (non-breaking change que corrige un issue)
- [ ] Nueva característica (non-breaking change que agrega funcionalidad)
- [ ] Breaking change (fix o feature que causaría que funcionalidad existente no funcione como se espera)
- [ ] Actualización de documentación

## ¿Cómo ha sido probado?

Describe las pruebas que realizaste para verificar tus cambios.

## Checklist:

- [ ] Mi código sigue el estilo de código de este proyecto
- [ ] He realizado una auto-revisión de mi código
- [ ] He comentado mi código, particularmente en áreas difíciles de entender
- [ ] He realizado los cambios correspondientes a la documentación
- [ ] Mis cambios no generan nuevas advertencias
- [ ] He agregado pruebas que demuestran que mi corrección es efectiva o que mi característica funciona
- [ ] Las pruebas unitarias nuevas y existentes pasan localmente con mis cambios

## Screenshots (si aplica):

Agregar screenshots para mostrar los cambios visuales.

## Issues relacionadas

Fixes #(issue number)
```

### Proceso de Revisión

1. **Automated checks** deben pasar (CI/CD)
2. **Code review** por al menos 1 maintainer
3. **Testing** en entorno de desarrollo
4. **Merge** después de aprobación

## 📚 Documentación

### Tipos de Documentación

- **README.md** - Documentación principal
- **\_docs/** - Documentación técnica organizada
- **Código** - Comentarios inline y docstrings
- **API** - Documentación Swagger/OpenAPI
- **Scripts** - Documentación de herramientas

### Estándares de Documentación

- **Markdown** para toda la documentación
- **Inglés** para código, **Español** para documentación de usuario
- **Screenshots** cuando sea apropiado
- **Ejemplos de código** funcionales
- **Enlaces** actualizados y verificados

### Estructura de Documentación

```
_docs/
├── integracion/     # Integración frontend-backend
├── mcp/            # Model Context Protocol
├── configuracion/   # Configuración de servicios
├── desarrollo/      # Guías de desarrollo
├── reportes/       # Reportes y métricas
└── guias/          # Tutorials y guías de usuario
```

## 🏷️ Versioning

Este proyecto usa [Semantic Versioning](https://semver.org/):

- **MAJOR** version cuando haces cambios incompatibles de API
- **MINOR** version cuando agregas funcionalidad de manera backwards-compatible
- **PATCH** version cuando haces correcciones backwards-compatible

## 🙋‍♀️ ¿Necesitas Ayuda?

- **GitHub Issues** - Para preguntas técnicas
- **GitHub Discussions** - Para discusiones generales
- **Email** - desarrollo@onevision.com para contacto directo

## 🎉 Reconocimientos

Los contribuidores serán reconocidos en:

- **README.md** - Lista de contribuidores
- **CHANGELOG.md** - Créditos en releases
- **GitHub** - Automatic contributor recognition

---

¡Gracias por contribuir a SICORA! Juntos hacemos el mejor sistema académico open source. 🚀
