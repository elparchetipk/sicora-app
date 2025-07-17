# 🚀 GUÍA DE CONFIGURACIÓN - INTEGRACIÓN FRONTEND-BACKEND GO

**Fecha**: 2 de julio de 2025  
**Proyecto**: SICORA - Sistema de Control de Asistencia  
**Objetivo**: Configurar la primera integración entre React Frontend y Go Backend

---

## 📋 **RESUMEN EJECUTIVO**

Esta guía te permitirá configurar manualmente toda la integración entre el frontend de React y el backend de Go, evitando problemas con la terminal interactiva.

**Servicios involucrados:**

- ✅ **PostgreSQL 15** (Base de datos compartida)
- ✅ **Go UserService** (Backend de autenticación y usuarios)
- ✅ **React Frontend** (Interfaz de usuario)

---

## 🎯 **PASO 1: VERIFICAR Y CONFIGURAR BACKEND GO**

### **1.1. Verificar PostgreSQL**

```bash
# UBICACIÓN: Cualquier directorio
pwd  # Para ver dónde estás
docker ps | grep postgres
```

### **1.2. Iniciar PostgreSQL (si no está corriendo)**

```bash
# UBICACIÓN: /home/epti/Documentos/epti-dev/sicora-app/sicora-be-go
cd /home/epti/Documentos/epti-dev/sicora-app/sicora-be-go
docker-compose -f docker-compose.infra.yml up -d
```

### **1.3. Verificar conexión a la base de datos**

```bash
# UBICACIÓN: Cualquier directorio
psql -h localhost -p 5432 -U sicora_user -d sicora_dev -c "\dt"
```

**Resultado esperado**: Lista de tablas o mensaje indicando que no hay tablas aún.

### **1.4. Navegar al UserService**

```bash
# UBICACIÓN: /home/epti/Documentos/epti-dev/sicora-app/sicora-be-go/userservice
cd /home/epti/Documentos/epti-dev/sicora-app/sicora-be-go/userservice
pwd  # Verificar ubicación
```

### **1.5. Ejecutar el UserService**

```bash
# UBICACIÓN: /home/epti/Documentos/epti-dev/sicora-app/sicora-be-go/userservice
./userservice
```

**Resultado esperado**:

```
[USERSERVICE-GO] 2025/07/02 XX:XX:XX Starting SICORA UserService Go...
Successfully connected to PostgreSQL 15 database: sicora_dev
Database migrations completed successfully
🚀 Server starting on port 8080
📊 Health check: http://localhost:8080/health
```

### **1.6. Verificar que el backend funcione (NUEVA TERMINAL)**

```bash
# UBICACIÓN: Cualquier directorio
curl http://localhost:8080/health
```

**Resultado esperado**:

```json
{ "status": "ok", "timestamp": "2025-07-02T..." }
```

---

## 🎯 **PASO 2: CONFIGURAR FRONTEND**

### **2.1. Navegar al Frontend**

```bash
# UBICACIÓN: /home/epti/Documentos/epti-dev/sicora-app/sicora-app-fe
cd /home/epti/Documentos/epti-dev/sicora-app/sicora-app-fe
pwd  # Verificar ubicación
```

### **2.2. Instalar Dependencias HTTP**

```bash
# UBICACIÓN: /home/epti/Documentos/epti-dev/sicora-app/sicora-app-fe
pnpm install axios zustand @tanstack/react-query
```

### **2.3. Instalar Tipos de Desarrollo**

```bash
# UBICACIÓN: /home/epti/Documentos/epti-dev/sicora-app/sicora-app-fe
pnpm install -D @types/node
```

### **2.4. Verificar Instalación**

```bash
# UBICACIÓN: /home/epti/Documentos/epti-dev/sicora-app/sicora-app-fe
cat package.json | grep -A 10 '"dependencies"'
```

---

## 🎯 **PASO 3: VERIFICAR ARCHIVOS CREADOS**

### **3.1. Verificar Archivos de Integración**

```bash
# UBICACIÓN: /home/epti/Documentos/epti-dev/sicora-app/sicora-app-fe
cd /home/epti/Documentos/epti-dev/sicora-app/sicora-app-fe

# Verificar que estos archivos existen:
ls -la .env.local
ls -la src/types/auth.types.ts
ls -la src/lib/api-client.ts
ls -la src/lib/auth-api.ts
ls -la src/stores/auth-store.ts
ls -la src/components/BackendTestComponent.tsx
```

**Resultado esperado**: Todos los archivos deben existir y tener contenido.

### **3.2. Ver Estructura de Archivos**

```bash
# UBICACIÓN: /home/epti/Documentos/epti-dev/sicora-app/sicora-app-fe
find src/ -name "*.ts" -o -name "*.tsx" | grep -E "(auth|api|store)" | sort
```

---

## 🎯 **PASO 4: CREAR ARCHIVOS FALTANTES**

### **4.1. Crear Hook de Autenticación**

```bash
# UBICACIÓN: /home/epti/Documentos/epti-dev/sicora-app/sicora-app-fe
cd /home/epti/Documentos/epti-dev/sicora-app/sicora-app-fe

# Crear directorio hooks si no existe
mkdir -p src/hooks

# Crear el archivo useAuth.ts
nano src/hooks/useAuth.ts
# O usa tu editor preferido: code src/hooks/useAuth.ts
```

**Contenido del archivo `src/hooks/useAuth.ts`**:

```typescript
import { useAuthStore } from '@/stores/auth-store';

export const useAuth = () => {
  const store = useAuthStore();

  return {
    user: store.user,
    isAuthenticated: store.isAuthenticated,
    isLoading: store.isLoading,
    error: store.error,
    login: store.login,
    logout: store.logout,
    clearError: store.clearError,
  };
};

export default useAuth;
```

### **4.2. Configurar main.tsx (React Query)**

```bash
# UBICACIÓN: /home/epti/Documentos/epti-dev/sicora-app/sicora-app-fe
nano src/main.tsx
# Añadir QueryClient provider (ver contenido abajo)
```

**Modificaciones en `src/main.tsx`**:

```typescript
// Añadir estos imports al inicio
import { QueryClient, QueryClientProvider } from '@tanstack/react-query'

// Crear QueryClient
const queryClient = new QueryClient({
  defaultOptions: {
    queries: {
      retry: 1,
      refetchOnWindowFocus: false,
    },
  },
})

// Envolver App con QueryClientProvider
<QueryClientProvider client={queryClient}>
  <App />
</QueryClientProvider>
```

---

## 🎯 **PASO 5: PROBAR BACKEND CON cURL**

### **5.1. Health Check**

```bash
# UBICACIÓN: Cualquier directorio
curl http://localhost:8080/health
```

### **5.2. Crear Usuario de Prueba**

```bash
# UBICACIÓN: Cualquier directorio
curl -X POST http://localhost:8080/api/v1/users \
  -H "Content-Type: application/json" \
  -d '{
    "nombre": "Usuario",
    "apellido": "Prueba",
    "email": "test@cgmlti.com",
    "documento": "12345678",
    "rol": "instructor",
    "password": "Test123!",
    "ficha_id": "TEST001",
    "programa_formacion": "Desarrollo de Software"
  }'
```

**Resultado esperado**: Usuario creado exitosamente o mensaje indicando que ya existe.

### **5.3. Probar Login**

```bash
# UBICACIÓN: Cualquier directorio
curl -X POST http://localhost:8080/api/v1/auth/login \
  -H "Content-Type: application/json" \
  -d '{
    "email": "test@cgmlti.com",
    "password": "Test123!"
  }'
```

**Resultado esperado**: JSON con `access_token`, `refresh_token` y datos del usuario.

### **5.4. Probar Obtener Perfil**

```bash
# UBICACIÓN: Cualquier directorio
# REEMPLAZA "TOKEN_AQUI" con el access_token del paso anterior
curl -X GET http://localhost:8080/api/v1/users/profile \
  -H "Authorization: Bearer TOKEN_AQUI"
```

---

## 🎯 **PASO 6: INICIAR FRONTEND**

### **6.1. Iniciar Servidor de Desarrollo**

```bash
# UBICACIÓN: /home/epti/Documentos/epti-dev/sicora-app/sicora-app-fe
cd /home/epti/Documentos/epti-dev/sicora-app/sicora-app-fe
pnpm dev
```

**Resultado esperado**:

```
VITE v5.x.x ready in XXXms

➜  Local:   http://localhost:5173/
➜  Network: use --host to expose
```

### **6.2. Verificar Frontend (NUEVA TERMINAL)**

```bash
# UBICACIÓN: Cualquier directorio
curl http://localhost:5173
```

### **6.3. Crear Ruta de Prueba**

Editar `src/App.tsx` para añadir:

```typescript
import BackendTestComponent from '@/components/BackendTestComponent'

// En tu router, añadir:
{
  path: '/test-backend',
  element: <BackendTestComponent />
}
```

---

## 🎯 **PASO 7: VERIFICACIÓN FINAL**

### **7.1. Verificar Servicios Corriendo**

```bash
# UBICACIÓN: Cualquier directorio

# PostgreSQL
docker ps | grep postgres

# Backend Go
curl -s http://localhost:8080/health | jq . || curl -s http://localhost:8080/health

# Frontend React
curl -s http://localhost:5173 | head -10

# Ver puertos ocupados
netstat -tlnp | grep -E ':(5173|8080|5432)'
```

### **7.2. Acceder a la Página de Prueba**

1. Abrir navegador
2. Ir a: `http://localhost:5173/test-backend`
3. Usar el componente de prueba para verificar integración

---

## 📊 **LOGS Y DEBUGGING**

### **Ver Logs del UserService**

```bash
# UBICACIÓN: /home/epti/Documentos/epti-dev/sicora-app/sicora-be-go/userservice
cd /home/epti/Documentos/epti-dev/sicora-app/sicora-be-go/userservice
tail -f userservice.log
```

### **Ver Logs de PostgreSQL**

```bash
# UBICACIÓN: /home/epti/Documentos/epti-dev/sicora-app/sicora-be-go
cd /home/epti/Documentos/epti-dev/sicora-app/sicora-be-go
docker logs sicora-postgres
```

### **Ver Procesos Corriendo**

```bash
# UBICACIÓN: Cualquier directorio
ps aux | grep userservice
ps aux | grep node
```

---

## 🗂️ **RESUMEN DE UBICACIONES**

| Servicio           | Directorio de Trabajo                                                |
| ------------------ | -------------------------------------------------------------------- |
| **Backend Go**     | `/home/epti/Documentos/epti-dev/sicora-app/sicora-be-go`             |
| **UserService**    | `/home/epti/Documentos/epti-dev/sicora-app/sicora-be-go/userservice` |
| **Frontend**       | `/home/epti/Documentos/epti-dev/sicora-app/sicora-app-fe`            |
| **Docker Compose** | `/home/epti/Documentos/epti-dev/sicora-app/sicora-be-go`             |

---

## ✅ **CHECKLIST DE VERIFICACIÓN**

Marca cuando tengas cada elemento funcionando:

- [ ] ✅ PostgreSQL corriendo (puerto 5432)
- [ ] ✅ Backend Go userservice corriendo (puerto 8080)
- [ ] ✅ Frontend corriendo (puerto 5173)
- [ ] ✅ Dependencias instaladas (axios, zustand, react-query)
- [ ] ✅ Variables de entorno configuradas (`.env.local`)
- [ ] ✅ Health check responde: `curl http://localhost:8080/health`
- [ ] ✅ Creación de usuario funciona (cURL)
- [ ] ✅ Login funciona (cURL)
- [ ] ✅ Obtener perfil funciona (cURL)
- [ ] ✅ Ruta `/test-backend` accesible
- [ ] ✅ Componente de prueba funciona

---

## 🚀 **CUANDO TENGAS TODO LISTO**

**Escríbeme**: _"Backend y frontend listos, todo funciona"_

Y entonces continuaremos con:

1. **Crear el LoginPage real**
2. **Implementar Route Guards**
3. **Integrar con el sistema de navegación existente**
4. **Preparar para el despliegue en Hostinger**

---

## 🆘 **SOLUCIÓN DE PROBLEMAS COMUNES**

### **PostgreSQL no inicia**

```bash
cd /home/epti/Documentos/epti-dev/sicora-app/sicora-be-go
docker-compose -f docker-compose.infra.yml down
docker-compose -f docker-compose.infra.yml up -d
```

### **UserService no conecta a la base**

Verificar archivo `.env` en `/userservice/`:

```bash
cd /home/epti/Documentos/epti-dev/sicora-app/sicora-be-go/userservice
cat .env
```

### **Frontend no encuentra módulos**

```bash
cd /home/epti/Documentos/epti-dev/sicora-app/sicora-app-fe
rm -rf node_modules
pnpm install
```

### **Puertos ocupados**

```bash
# Ver qué está usando el puerto
lsof -i :8080
lsof -i :5173
lsof -i :5432

# Matar proceso si es necesario
kill -9 PID_AQUI
```

---

**¡Éxito en la configuración!** 🎉
