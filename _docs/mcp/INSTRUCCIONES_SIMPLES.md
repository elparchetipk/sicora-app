# 🎯 INSTRUCCIONES SÚPER SIMPLES PARA USAR MCP

## ¿Qué es MCP?

MCP te da un asistente de IA que conoce específicamente tu proyecto SICORA.

## ¿Cómo lo uso?

### 1. Ejecutar un comando (solo una vez)

```bash
cd /home/epti/Documentos/epti-dev/sicora-app/sicora-mcp-server
./scripts/setup-mcp-principiantes.sh
```

### 2. Reiniciar VS Code

- Cerrar VS Code completamente
- Abrir VS Code desde tu proyecto SICORA

### 3. Hacer preguntas en el chat de GitHub Copilot

- Abrir chat de Copilot en VS Code
- Preguntar cosas como:
  - "¿Cuál es el estado del proyecto SICORA?"
  - "Necesito un componente React para mostrar usuarios"
  - "¿Funciona bien la integración frontend-backend?"

## ¿Qué va a pasar?

El asistente va a:

- Conocer tu proyecto SICORA específicamente
- Generar código adaptado a tu stack tecnológico
- Analizar tu proyecto automáticamente
- Darte respuestas súper específicas

## ¿Cómo sé si funciona?

- El servidor se inicia con: "🚀 Servidor MCP SICORA iniciado correctamente"
- El chat de Copilot responde con información específica de SICORA
- Las respuestas mencionan React, Go, PostgreSQL (tus tecnologías)

## ¿Problemas?

```bash
# Verificar estado
pnpm run mcp:status

# Reiniciar servidor
pnpm start
```

## ¡Listo!

Ahora tienes un asistente de IA que conoce tu proyecto SICORA. 🚀
