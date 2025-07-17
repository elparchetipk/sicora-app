# INSTRUCCIONES PARA COMPLETAR E2E TESTING - EVALPROY

## 🎯 OBJETIVO

Ejecutar y validar el sistema de pruebas E2E (end-to-end) implementado para el módulo EvalProy.

## ✅ PREREQUISITOS COMPLETADOS

- ✅ Cypress instalado y configurado
- ✅ Archivos de pruebas E2E creados
- ✅ Comandos custom implementados
- ✅ Fixtures de datos preparadas
- ✅ Scripts de package.json configurados

## 🚀 PASOS PARA EJECUCIÓN

### Paso 1: Iniciar el Servidor de Desarrollo

```bash
# En terminal 1 (mantener abierto):
cd /home/epti/Documentos/epti-dev/asiste-app/sicora-app-fe
pnpm dev
```

**Verificación**:

- El servidor debe mostrar algo como: `Local: http://localhost:5173/`
- Abrir http://localhost:5173 en navegador para confirmar que la app carga

### Paso 2: Ejecutar Pruebas E2E (Opción Interactiva)

```bash
# En terminal 2:
cd /home/epti/Documentos/epti-dev/asiste-app/sicora-app-fe
pnpm cypress:open
```

**En la interfaz de Cypress**:

1. Seleccionar "E2E Testing"
2. Elegir navegador (Chrome recomendado)
3. Ejecutar pruebas en este orden:
   - `connectivity-test.cy.ts` (verificación básica)
   - `student-workflow.cy.ts` (flujo estudiante)
   - `instructor-workflow.cy.ts` (flujo instructor)
   - `admin-workflow.cy.ts` (flujo administrador)
   - `stakeholder-workflow.cy.ts` (flujo stakeholder)
   - `guards-and-errors.cy.ts` (casos edge)

### Paso 3: Ejecutar Pruebas E2E (Modo Headless)

```bash
# Alternativa para ejecución automática:
pnpm cypress:run

# O ejecutar prueba específica:
npx cypress run --spec "cypress/e2e/evalproy/student-workflow.cy.ts"
```

### Paso 4: Revisar Resultados

- **Screenshots**: `cypress/screenshots/` (en caso de fallos)
- **Videos**: `cypress/videos/` (si está habilitado)
- **Terminal**: Revisar logs y errores

## 🔧 TROUBLESHOOTING

### Problema: Servidor no inicia

```bash
# Verificar dependencias:
pnpm install

# Limpiar caché y reinstalar:
rm -rf node_modules pnpm-lock.yaml
pnpm install

# Verificar puerto ocupado:
lsof -i :5173
```

### Problema: Cypress no encuentra elementos

1. Verificar que la app esté cargada completamente
2. Revisar que los `data-testid` existen en componentes
3. Ajustar selectores en archivos `.cy.ts`

### Problema: API Interceptors fallan

- Los interceptors están configurados, no necesitan backend real
- Verificar que las rutas coincidan con las reales de la app

## 📊 COBERTURA ESPERADA

### Por Rol:

- **Estudiante**: Navegación, gestión de ideas, sesiones, avances
- **Instructor**: Proyectos asignados, evaluaciones, reportes
- **Administrador**: Dashboard, gestión de usuarios y proyectos
- **Stakeholder**: Evaluación de proyectos, historial

### Por Funcionalidad:

- **Navegación**: Rutas, menús, breadcrumbs
- **Guards**: Autenticación y autorización
- **Formularios**: Validaciones, envío, errores
- **Responsive**: Mobile-first, diferentes viewports
- **Accesibilidad**: Navegación por teclado, ARIA

## 📈 MÉTRICAS DE ÉXITO

### ✅ Criterios de Aceptación:

- [ ] Todas las pruebas pasan sin fallos críticos
- [ ] Navegación funciona en todos los roles
- [ ] Guards protegen rutas correctamente
- [ ] Formularios validan datos apropiadamente
- [ ] Responsive funciona en móvil y desktop
- [ ] Accesibilidad básica implementada

### 📊 Resultados Esperados:

- **Tests Passed**: 80%+ (permitir algunos fallos menores)
- **Coverage**: Flujos principales cubiertos
- **Performance**: Pruebas ejecutan en <5 minutos

## 🎉 AL COMPLETAR

### Documentar Resultados:

1. Capturas de pantalla de resultados exitosos
2. Log de errores encontrados (si hay)
3. Ajustes realizados a las pruebas
4. Tiempo total de ejecución

### Siguiente Fase:

- Integración en pipeline CI/CD
- Pruebas de regresión automáticas
- Expansión de cobertura según necesidades

## 📞 SOPORTE

Si hay problemas técnicos:

1. Revisar `cypress/screenshots/` para capturas de fallos
2. Verificar logs del servidor en terminal 1
3. Consultar documentación oficial de Cypress
4. Revisar configuración en `cypress.config.ts`

---

**NOTA**: Este sistema E2E está diseñado para ser robusto y funcionar con datos mock, por lo que no requiere un backend completamente funcional para la mayoría de las pruebas.
