# 🤖 Guía para usar MCP (Model Context Protocol) - Principiantes

## 🎯 ¿Qué es MCP?

MCP (Model Context Protocol) es un protocolo que permite a los asistentes de IA acceder a herramientas y recursos específicos de tu proyecto. Es como darle "superpoderes" al asistente para que entienda mejor tu código y pueda ayudarte de manera más específica.

## 🚀 Cómo empezar a usar MCP

### Paso 1: Verificar que el servidor MCP está funcionando

```bash
# Desde el directorio sicora-mcp-server
cd /home/epti/Documentos/epti-dev/sicora-app/sicora-mcp-server
pnpm run mcp:status
```

**Deberías ver**:

```
[INFO] ✅ Compilado: dist/index.js existe
[INFO] ✅ Dependencias: node_modules existe
[WARN] ⚠️  Servidor: No está ejecutándose
```

### Paso 2: Iniciar el servidor MCP

```bash
# Iniciar el servidor MCP
pnpm start
```

**Deberías ver**:

```
🚀 Servidor MCP SICORA iniciado correctamente
```

### Paso 3: Configurar VS Code para usar MCP

El archivo `.vscode/mcp.json` ya está configurado. Ahora necesitas:

1. **Reiniciar VS Code** completamente
2. **Verificar que VS Code detecte el servidor MCP**

## 🛠️ Herramientas MCP disponibles para SICORA

Una vez que MCP esté funcionando, tendrás acceso a estas herramientas:

### 1. **sicora-analyze** - Análisis del proyecto

```
Analiza la estructura completa del proyecto SICORA
- Estructura de archivos
- Dependencias
- Estado de salud del proyecto
- Recomendaciones de mejora
```

### 2. **sicora-generate** - Generación de código

```
Genera código específico para SICORA:
- Componentes React
- Handlers de Go
- Endpoints de API
- Modelos de base de datos
```

### 3. **sicora-integrate** - Integración frontend-backend

```
Verifica y mejora la integración entre:
- Frontend React
- Backend Go
- Base de datos
- APIs
```

### 4. **sicora-test** - Gestión de pruebas

```
Ejecuta y gestiona pruebas:
- Pruebas unitarias
- Pruebas de integración
- Pruebas end-to-end
```

### 5. **sicora-document** - Documentación

```
Actualiza documentación automáticamente:
- README
- Comentarios de código
- Guías de desarrollo
```

## 📝 Cómo usar las herramientas MCP

### Opción 1: Comando de Chat (Recomendado)

En VS Code, abre el chat de GitHub Copilot y usa comandos como:

```
@sicora-analyze analiza el proyecto completo
@sicora-generate crea un componente React para login
@sicora-integrate verifica la conexión frontend-backend
@sicora-test ejecuta pruebas unitarias
@sicora-document actualiza el README
```

### Opción 2: Paleta de comandos

1. Presiona `Ctrl+Shift+P` (o `Cmd+Shift+P` en Mac)
2. Busca "MCP"
3. Selecciona las herramientas disponibles

### Opción 3: Automático

El asistente usará las herramientas MCP automáticamente cuando:

- Hagas preguntas sobre el proyecto SICORA
- Pidas generar código específico
- Necesites análisis del proyecto

## 🔍 Ejemplos prácticos

### Ejemplo 1: Analizar el proyecto

**Tú preguntas**: "¿Cuál es el estado actual del proyecto SICORA?"
**El asistente**: Usará `sicora-analyze` automáticamente y te dará un reporte completo.

### Ejemplo 2: Generar código

**Tú preguntas**: "Necesito un componente React para mostrar usuarios"
**El asistente**: Usará `sicora-generate` y creará un componente específico para SICORA.

### Ejemplo 3: Verificar integración

**Tú preguntas**: "¿Funciona bien la conexión entre frontend y backend?"
**El asistente**: Usará `sicora-integrate` y te dará un reporte de estado.

## 🚨 Solución de problemas

### Problema: "No puedo ver las herramientas MCP"

**Solución**:

1. Verifica que el servidor esté ejecutándose:

   ```bash
   pnpm run mcp:status
   ```

2. Reinicia VS Code completamente

3. Verifica la configuración:
   ```bash
   cat .vscode/mcp.json
   ```

### Problema: "El servidor MCP no inicia"

**Solución**:

1. Recompila el proyecto:

   ```bash
   pnpm run build
   ```

2. Verifica dependencias:

   ```bash
   pnpm install
   ```

3. Revisa logs:
   ```bash
   pnpm start
   ```

### Problema: "VS Code no detecta MCP"

**Solución**:

1. Asegúrate de tener la extensión GitHub Copilot
2. Verifica que el archivo `.vscode/mcp.json` existe
3. Reinicia VS Code

## 🎯 Mejores prácticas

### 1. Mantén el servidor MCP ejecutándose

```bash
# Usar en modo desarrollo
pnpm run dev
```

### 2. Usa preguntas específicas

❌ **Mal**: "Ayúdame con el código"
✅ **Bien**: "Necesito un componente React para el login de SICORA"

### 3. Aprovecha el contexto

El servidor MCP conoce:

- Estructura del proyecto
- Tecnologías usadas (React, Go, PostgreSQL)
- Patrones de código de SICORA
- Mejores prácticas del proyecto

### 4. Combina herramientas

```
1. @sicora-analyze (para entender el estado)
2. @sicora-generate (para crear código)
3. @sicora-test (para probar)
4. @sicora-document (para documentar)
```

## 🎉 ¡Empieza a usar MCP ahora!

1. **Inicia el servidor**:

   ```bash
   cd sicora-mcp-server
   pnpm start
   ```

2. **Reinicia VS Code**

3. **Haz tu primera pregunta**:
   "¿Puedes analizar el estado actual del proyecto SICORA?"

4. **Observa cómo el asistente usa las herramientas MCP automáticamente**

---

**¡Listo!** Ya puedes usar MCP para tener un asistente de IA súper especializado en tu proyecto SICORA. 🚀
