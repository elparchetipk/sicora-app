# Política de Seguridad

## Versiones Soportadas

Actualmente soportamos las siguientes versiones de SICORA con actualizaciones de seguridad:

| Versión | Soportada |
| ------- | --------- |
| 1.0.x   | ✅ Sí     |
| < 1.0   | ❌ No     |

## Reportar una Vulnerabilidad

La seguridad es muy importante para nosotros. Si descubres una vulnerabilidad de seguridad en SICORA, por favor repórtala de manera responsable.

### 🔒 Proceso de Reporte Confidencial

**NO** crear un issue público para vulnerabilidades de seguridad. En su lugar:

1. **Email**: Envía un email a **security@onevision.education** con:

   - Descripción detallada de la vulnerabilidad
   - Pasos para reproducir el problema
   - Impacto potencial
   - Versión afectada
   - Tu información de contacto

2. **Respuesta**: Recibirás una confirmación dentro de **48 horas**

3. **Investigación**: Investigaremos el reporte dentro de **5 días hábiles**

4. **Resolución**: Si es confirmada, trabajaremos en un fix prioritario

5. **Divulgación**: Coordinaremos la divulgación pública responsable

### 🏆 Reconocimiento

Los reportes de seguridad válidos serán reconocidos en:

- Hall of Fame de seguridad en la documentación
- Agradecimientos en las notas de release
- Reconocimiento público (si el reportero lo desea)

## 🛡️ Medidas de Seguridad Implementadas

### Autenticación y Autorización

- **JWT Tokens**: Autenticación basada en tokens seguros
- **Refresh Tokens**: Rotación automática de tokens
- **Roles y Permisos**: Sistema granular de autorización
- **Middleware de Seguridad**: Verificación en cada request
- **Sesiones Seguras**: Gestión segura de sesiones de usuario

### Comunicación

- **HTTPS**: Todas las comunicaciones en producción usan HTTPS
- **CORS**: Configuración estricta de Cross-Origin Resource Sharing
- **Headers de Seguridad**: CSP, HSTS, X-Frame-Options implementados
- **Rate Limiting**: Protección contra ataques de fuerza bruta

### Base de Datos

- **SQL Injection**: Protección mediante ORM (GORM, SQLAlchemy)
- **Prepared Statements**: Todas las consultas utilizan statements preparados
- **Validación de Entrada**: Validación estricta en todas las capas
- **Escapado de Datos**: Todos los datos son escapados apropiadamente

### Infraestructura

- **Docker Security**: Contenedores con usuarios no-root
- **Network Isolation**: Segmentación de red entre servicios
- **Secrets Management**: Variables de entorno seguras
- **Container Scanning**: Escaneo regular de vulnerabilidades

### Código

- **Dependency Scanning**: Escaneo automático de dependencias
- **Static Analysis**: Análisis estático de código
- **Code Review**: Revisión obligatoria de código
- **Automated Testing**: Tests de seguridad automatizados

## 🚨 Tipos de Vulnerabilidades

### Críticas (Resolución: 24-48 horas)

- Ejecución remota de código
- Escalación de privilegios
- Bypass de autenticación
- Exposición de datos sensibles

### Altas (Resolución: 3-7 días)

- SQL Injection
- Cross-Site Scripting (XSS)
- Cross-Site Request Forgery (CSRF)
- Insecure Direct Object References

### Medias (Resolución: 2-4 semanas)

- Information Disclosure
- Weak Cryptography
- Session Management Issues
- Insufficient Logging

### Bajas (Resolución: 1-3 meses)

- Problemas de configuración
- Issues menores de información
- Problemas de usabilidad relacionados con seguridad

## 🔍 Scope de Seguridad

### En Scope

- **Frontend React** (sicora-app-fe)
- **Backend Go** (sicora-be-go)
- **Backend Python** (sicora-be-python)
- **API Gateway**
- **Base de datos PostgreSQL/MongoDB**
- **Infraestructura Docker**
- **MCP Server**

### Fuera de Scope

- Ataques de ingeniería social
- Vulnerabilidades en dependencias de terceros (reportar directamente a los mantenedores)
- Ataques de denegación de servicio (DoS)
- Problemas de configuración del entorno local de desarrollo

## 📋 Checklist de Seguridad para Desarrolladores

### Antes de Hacer Commit

- [ ] ¿He revisado el código por posibles vulnerabilidades?
- [ ] ¿Estoy validando todas las entradas de usuario?
- [ ] ¿He escapado todos los datos de salida?
- [ ] ¿Estoy usando consultas preparadas?
- [ ] ¿He implementado autorización apropiada?
- [ ] ¿He evitado hardcodear secrets?

### En Pull Requests

- [ ] ¿El código ha sido revisado por al menos un desarrollador senior?
- [ ] ¿Pasan todos los tests de seguridad automatizados?
- [ ] ¿He actualizado la documentación de seguridad si es necesario?
- [ ] ¿He considerado el impacto en la superficie de ataque?

## 🛠️ Herramientas de Seguridad

### Análisis Estático

- **ESLint**: Para frontend JavaScript/TypeScript
- **Gosec**: Para código Go
- **Bandit**: Para código Python
- **SonarQube**: Análisis integral de calidad y seguridad

### Análisis de Dependencias

- **npm audit**: Para dependencias de Node.js
- **go mod tidy**: Para módulos Go
- **pip-audit**: Para paquetes Python
- **Snyk**: Escaneo continuo de vulnerabilidades

### Testing de Seguridad

- **OWASP ZAP**: Tests de penetración automatizados
- **Unit Tests**: Tests específicos de seguridad
- **Integration Tests**: Tests de seguridad de extremo a extremo

## 📚 Recursos de Seguridad

### Guías de Desarrollo Seguro

- [OWASP Top 10](https://owasp.org/www-project-top-ten/)
- [OWASP API Security Top 10](https://owasp.org/www-project-api-security/)
- [Go Security Checklist](https://github.com/securecodewarrior/go-security-checklist)
- [React Security Best Practices](https://snyk.io/blog/10-react-security-best-practices/)

### Capacitación

- Sesiones de seguridad para desarrolladores
- Code review enfocado en seguridad
- Actualizaciones regulares sobre nuevas amenazas
- Workshops de desarrollo seguro

## 🔄 Proceso de Actualización de Seguridad

1. **Detección**: Monitoring continuo de vulnerabilidades
2. **Evaluación**: Análisis de impacto y riesgo
3. **Desarrollo**: Creación de fix prioritario
4. **Testing**: Pruebas exhaustivas del fix
5. **Deployment**: Despliegue coordinado
6. **Comunicación**: Notificación a usuarios y stakeholders

## 📞 Contacto de Seguridad

- **Email Principal**: security@onevision.education
- **Email Alternativo**: dev@onevision.education
- **Tiempo de Respuesta**: Máximo 48 horas
- **Horario**: 24/7 para vulnerabilidades críticas

---

**Nota**: Este documento es revisado y actualizado regularmente. La última actualización fue el 3 de agosto de 2025.

**SICORA Security Team** - Comprometidos con la seguridad y privacidad de nuestros usuarios.
