# ✅ CHECKLIST: Cómo usar MCP por primera vez

## 🎯 Objetivo

Configurar y usar MCP (Model Context Protocol) para tener un asistente de IA especializado en tu proyecto SICORA.

---

## 📋 Lista de verificación

### PASO 1: Verificar prerequisitos

- [ ] Node.js >= 18.0.0 instalado
- [ ] pnpm instalado (o se instalará automáticamente)
- [ ] VS Code instalado
- [ ] GitHub Copilot instalado en VS Code
- [ ] Estás en el directorio `sicora-mcp-server/`

### PASO 2: Configurar el servidor MCP

- [ ] Ejecutar configuración automática: `./scripts/setup-mcp-principiantes.sh`
- [ ] O configurar manualmente:
  - [ ] `pnpm install` (instalar dependencias)
  - [ ] `pnpm run build` (compilar)
  - [ ] Verificar que existe `dist/index.js`

### PASO 3: Configurar VS Code

- [ ] Verificar que existe `.vscode/mcp.json` en la raíz del proyecto
- [ ] Cerrar VS Code completamente
- [ ] Reabrir VS Code desde la raíz del proyecto SICORA
- [ ] Verificar que GitHub Copilot está activo

### PASO 4: Iniciar servidor MCP

- [ ] Ejecutar: `pnpm start`
- [ ] Verificar mensaje: "🚀 Servidor MCP SICORA iniciado correctamente"
- [ ] Dejar el servidor ejecutándose

### PASO 5: Hacer primera prueba

- [ ] Abrir chat de GitHub Copilot en VS Code
- [ ] Hacer una pregunta sobre SICORA
- [ ] Observar que el asistente use herramientas MCP automáticamente

---

## 🚀 Configuración rápida (1 comando)

```bash
# Desde el directorio sicora-mcp-server
./scripts/setup-mcp-principiantes.sh
```

Este script hace todo automáticamente y te guía paso a paso.

---

## 🔧 Configuración manual

### 1. Instalar dependencias

```bash
cd sicora-mcp-server
pnpm install
```

### 2. Compilar servidor

```bash
pnpm run build
```

### 3. Verificar configuración VS Code

```bash
# Debe existir este archivo
cat ../.vscode/mcp.json
```

### 4. Iniciar servidor

```bash
pnpm start
```

### 5. Usar en VS Code

- Abrir chat de GitHub Copilot
- Hacer preguntas sobre SICORA

---

## 🎯 Primeras preguntas para probar MCP

### Preguntas básicas

- [ ] "¿Cuál es el estado actual del proyecto SICORA?"
- [ ] "¿Qué tecnologías usa el proyecto SICORA?"
- [ ] "¿Cómo está estructurado el proyecto?"

### Preguntas de análisis

- [ ] "Analiza la salud del proyecto SICORA"
- [ ] "¿Hay problemas de integración entre frontend y backend?"
- [ ] "¿Qué mejoras recomiendas para el proyecto?"

### Preguntas de generación de código

- [ ] "Necesito un componente React para mostrar usuarios"
- [ ] "Crea un handler de Go para autenticación"
- [ ] "Genera un endpoint para gestionar estudiantes"

### Preguntas de integración

- [ ] "¿Funciona correctamente la autenticación entre frontend y backend?"
- [ ] "¿Hay algún problema con las APIs?"
- [ ] "¿Cómo puedo mejorar la comunicación entre servicios?"

---

## 🔍 Señales de que MCP está funcionando

### ✅ Señales positivas

- [ ] El servidor MCP se inicia sin errores
- [ ] VS Code detecta la configuración MCP
- [ ] El chat de Copilot responde con información específica de SICORA
- [ ] Las respuestas incluyen detalles técnicos del proyecto
- [ ] El asistente menciona tecnologías específicas (React, Go, PostgreSQL)

### ❌ Señales de problemas

- [ ] Error al compilar el servidor MCP
- [ ] VS Code no detecta la configuración
- [ ] El chat de Copilot da respuestas genéricas
- [ ] No se mencionan herramientas MCP específicas

---

## 🐛 Solución de problemas

### Problema: "No se inicia el servidor MCP"

```bash
# Verificar errores
pnpm run build
pnpm start
```

### Problema: "VS Code no detecta MCP"

```bash
# Verificar configuración
cat ../.vscode/mcp.json

# Reinstalar dependencias
pnpm install
```

### Problema: "El chat no usa herramientas MCP"

1. Reiniciar VS Code completamente
2. Verificar que GitHub Copilot esté activo
3. Hacer preguntas específicas sobre SICORA

---

## 📚 Recursos adicionales

- [ ] Leer: [GUIA_MCP_PRINCIPIANTES.md](./GUIA_MCP_PRINCIPIANTES.md)
- [ ] Leer: [README-pnpm.md](./README-pnpm.md)
- [ ] Ejecutar: `pnpm run mcp:status` para verificar estado
- [ ] Ejecutar: `./scripts/dev.sh status` para diagnóstico completo

---

## 🎉 ¡Listo!

Una vez que hayas completado todos los pasos, tendrás:

- ✅ Un servidor MCP especializado en SICORA
- ✅ Un asistente de IA que conoce tu proyecto
- ✅ Herramientas automáticas para desarrollo
- ✅ Generación de código específica para SICORA
- ✅ Análisis y documentación automatizada

**¡Ahora puedes desarrollar SICORA con un asistente de IA súper especializado!** 🚀
