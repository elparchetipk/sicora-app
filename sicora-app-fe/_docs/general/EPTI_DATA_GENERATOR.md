# 🎲 GENERADOR DE DATOS SINTÉTICOS - EPTI ONEVISION

## 🎯 OBJETIVO

Generar datos completamente sintéticos que reflejen la estructura real del SENA pero con información falsa para proteger la privacidad y seguridad de los datos institucionales.

---

## 📊 CONFIGURACIÓN DE GENERACIÓN

### **1. USUARIOS SINTÉTICOS**

```javascript
// Generador de usuarios para EPTI ONEVISION
const NOMBRES_FICTICIOS = [
  'Carlos',
  'María',
  'José',
  'Ana',
  'Luis',
  'Carmen',
  'David',
  'Laura',
  'Miguel',
  'Patricia',
  'Rafael',
  'Sandra',
  'Andrés',
  'Diana',
  'Felipe',
  'Mónica',
  'Gabriel',
  'Natalia',
  'Sebastián',
  'Valeria',
  'Nicolás',
  'Paola',
];

const APELLIDOS_FICTICIOS = [
  'García',
  'Rodríguez',
  'López',
  'Martínez',
  'González',
  'Pérez',
  'Sánchez',
  'Ramírez',
  'Cruz',
  'Flores',
  'Rivera',
  'Gómez',
  'Díaz',
  'Reyes',
  'Morales',
  'Jiménez',
  'Herrera',
  'Medina',
  'Castro',
  'Ortiz',
  'Rubio',
  'Marín',
];

const generarUsuario = () => ({
  documento: generarDocumento(),
  tipo_documento: elegirAleatorio(['CC', 'CE', 'TI']),
  nombres: `${elegirAleatorio(NOMBRES_FICTICIOS)} ${elegirAleatorio(NOMBRES_FICTICIOS)}`,
  apellidos: `${elegirAleatorio(APELLIDOS_FICTICIOS)} ${elegirAleatorio(APELLIDOS_FICTICIOS)}`,
  email: generarEmailEPTI(),
  telefono: generarTelefono(),
  fecha_nacimiento: generarFechaNacimiento(),
  genero: elegirAleatorio(['M', 'F']),
  ciudad: elegirAleatorio(CIUDADES_COLOMBIA),
  departamento: elegirAleatorio(DEPARTAMENTOS_COLOMBIA),
});
```

### **2. PROGRAMAS DE FORMACIÓN SINTÉTICOS**

```javascript
const PROGRAMAS_EPTI = [
  {
    codigo: 'EPTI001',
    nombre: 'Desarrollo de Software Empresarial',
    nivel: 'tecnologo',
    duracion_horas: 2640,
    duracion_meses: 24,
    area_conocimiento: 'Tecnologías de la Información',
    sector_economico: 'Software y TI',
  },
  {
    codigo: 'EPTI002',
    nombre: 'Gestión de Redes y Telecomunicaciones',
    nivel: 'tecnico',
    duracion_horas: 1760,
    duracion_meses: 18,
    area_conocimiento: 'Telecomunicaciones',
    sector_economico: 'Telecomunicaciones',
  },
  {
    codigo: 'EPTI003',
    nombre: 'Análisis de Datos y Business Intelligence',
    nivel: 'tecnologo',
    duracion_horas: 2640,
    duracion_meses: 24,
    area_conocimiento: 'Ciencias de Datos',
    sector_economico: 'Análisis de Datos',
  },
  {
    codigo: 'EPTI004',
    nombre: 'Ciberseguridad y Ethical Hacking',
    nivel: 'especializacion',
    duracion_horas: 880,
    duracion_meses: 12,
    area_conocimiento: 'Seguridad Informática',
    sector_economico: 'Ciberseguridad',
  },
  {
    codigo: 'EPTI005',
    nombre: 'Gestión de Proyectos Tecnológicos',
    nivel: 'tecnologo',
    duracion_horas: 2200,
    duracion_meses: 20,
    area_conocimiento: 'Gestión de Proyectos',
    sector_economico: 'Consultoría TI',
  },
  {
    codigo: 'EPTI006',
    nombre: 'Marketing Digital y E-commerce',
    nivel: 'tecnico',
    duracion_horas: 1540,
    duracion_meses: 16,
    area_conocimiento: 'Marketing Digital',
    sector_economico: 'Comercio Electrónico',
  },
  {
    codigo: 'EPTI007',
    nombre: 'Automatización Industrial 4.0',
    nivel: 'tecnologo',
    duracion_horas: 2640,
    duracion_meses: 24,
    area_conocimiento: 'Automatización',
    sector_economico: 'Industria 4.0',
  },
  {
    codigo: 'EPTI008',
    nombre: 'Desarrollo de Aplicaciones Móviles',
    nivel: 'tecnico',
    duracion_horas: 1760,
    duracion_meses: 18,
    area_conocimiento: 'Desarrollo Móvil',
    sector_economico: 'Aplicaciones Móviles',
  },
];
```

### **3. CENTROS DE FORMACIÓN EPTI**

```javascript
const CENTROS_EPTI = [
  {
    codigo: 'EPTI-NO',
    nombre: 'Centro Tecnológico EPTI Norte',
    direccion: 'Avenida Digital 123, Zona Norte',
    ciudad: 'Bogotá',
    departamento: 'Cundinamarca',
    telefono: '(601) 555-0101',
    email: 'norte@epti.edu.co',
  },
  {
    codigo: 'EPTI-SU',
    nombre: 'Centro de Innovación EPTI Sur',
    direccion: 'Carrera Innovación 456, Zona Sur',
    ciudad: 'Medellín',
    departamento: 'Antioquia',
    telefono: '(604) 555-0102',
    email: 'sur@epti.edu.co',
  },
  {
    codigo: 'EPTI-VR',
    nombre: 'Campus Virtual EPTI Digital',
    direccion: 'Plataforma Virtual - Sede Principal',
    ciudad: 'Cali',
    departamento: 'Valle del Cauca',
    telefono: '(602) 555-0103',
    email: 'virtual@epti.edu.co',
  },
  {
    codigo: 'EPTI-EM',
    nombre: 'Centro EPTI Empresarial',
    direccion: 'Zona Empresarial Tech Park 789',
    ciudad: 'Barranquilla',
    departamento: 'Atlántico',
    telefono: '(605) 555-0104',
    email: 'empresarial@epti.edu.co',
  },
];
```

---

## 🎲 FUNCIONES DE GENERACIÓN

### **Documentos Sintéticos**

```javascript
const generarDocumento = () => {
  // Generar números de documento válidos pero ficticios
  const prefijos = ['10', '11', '12', '20', '30', '40', '50', '60', '70', '80'];
  const prefijo = elegirAleatorio(prefijos);
  const numero = Math.floor(Math.random() * 999999)
    .toString()
    .padStart(6, '0');
  const digito = Math.floor(Math.random() * 10);
  return `${prefijo}${numero}${digito}`;
};
```

### **Emails Corporativos EPTI**

```javascript
const generarEmailEPTI = (nombres, apellidos) => {
  const nombre = nombres.split(' ')[0].toLowerCase();
  const apellido = apellidos.split(' ')[0].toLowerCase();
  const dominios = [
    '@epti.edu.co',
    '@estudiantes.epti.edu.co',
    '@instructores.epti.edu.co',
  ];
  const dominio = elegirAleatorio(dominios);
  return `${nombre}.${apellido}${Math.floor(Math.random() * 99)}${dominio}`;
};
```

### **Fichas de Formación**

```javascript
const generarFicha = () => {
  const año = new Date().getFullYear();
  const trimestre = Math.floor(Math.random() * 4) + 1;
  const numero = Math.floor(Math.random() * 999)
    .toString()
    .padStart(3, '0');
  return `${año}${trimestre}${numero}`;
};
```

### **Horarios Realistas**

```javascript
const generarHorarios = () => {
  const jornadas = {
    mañana: { inicio: '06:00', fin: '12:00' },
    tarde: { inicio: '12:00', fin: '18:00' },
    noche: { inicio: '18:00', fin: '22:00' },
  };

  const competencias = [
    'Desarrollar software según requerimientos',
    'Implementar bases de datos relacionales',
    'Aplicar metodologías ágiles de desarrollo',
    'Configurar redes de telecomunicaciones',
    'Analizar datos empresariales',
    'Implementar sistemas de seguridad informática',
    'Gestionar proyectos tecnológicos',
    'Desarrollar estrategias de marketing digital',
  ];

  return {
    jornada: elegirAleatorio(Object.keys(jornadas)),
    competencia: elegirAleatorio(competencias),
    resultado_aprendizaje: generarResultadoAprendizaje(),
  };
};
```

---

## 📈 VOLÚMENES DE DATOS SUGERIDOS

### **Para Demostración Completa:**

- **👥 Usuarios**: 5,000 registros
  - 4,000 Aprendices
  - 800 Instructores
  - 150 Coordinadores
  - 50 Administrativos

- **🏫 Centros**: 4 centros
- **📚 Programas**: 8 programas
- **📋 Fichas**: 200 fichas activas
- **📅 Horarios**: 2,000 bloques horarios
- **📊 Asistencias**: 50,000 registros (últimos 6 meses)

### **Distribución por Roles:**

```javascript
const DISTRIBUCION_ROLES = {
  'aprendiz': 80%,           // 4,000 usuarios
  'instructor': 16%,         // 800 usuarios
  'coordinador': 3%,         // 150 usuarios
  'administrativo': 1%       // 50 usuarios
};
```

---

## 🚀 SCRIPT DE GENERACIÓN AUTOMÁTICA

### **Comando de Ejecución:**

```bash
# Instalar dependencias
npm install faker-js casual moment

# Ejecutar generador
node scripts/generate-epti-data.js --records=5000 --environment=demo

# Exportar a SQL
node scripts/export-to-sql.js --output=epti_demo_data.sql

# Importar a base de datos
mysql -u usuario -p epti_onevision_demo < epti_demo_data.sql
```

### **Configuración de Generación:**

```javascript
const CONFIG_GENERACION = {
  entorno: 'demo',
  prefijo_email: 'demo.',
  sufijo_documentos: '000',
  año_base: 2024,
  seed_aleatoriedad: 12345, // Para resultados reproducibles
  validaciones: {
    email_unicos: true,
    documentos_unicos: true,
    fichas_coherentes: true,
    horarios_sin_conflicto: true,
  },
};
```

---

## 🔍 VALIDACIONES DE DATOS

### **Integridad Referencial:**

- ✅ Todos los aprendices tienen ficha válida
- ✅ Todas las fichas tienen programa válido
- ✅ Todos los horarios tienen instructor y ambiente válidos
- ✅ Todas las asistencias tienen aprendiz y horario válidos

### **Consistencia Temporal:**

- ✅ Fechas de fichas coherentes
- ✅ Horarios dentro de rango de fichas
- ✅ Asistencias en días laborales
- ✅ Usuarios con edad apropiada para el rol

### **Realismo de Datos:**

- ✅ Nombres y apellidos colombianos comunes
- ✅ Documentos con formato válido
- ✅ Teléfonos con códigos de área reales
- ✅ Direcciones con formato colombiano
- ✅ Emails con dominios EPTI

---

## 📋 PRÓXIMA IMPLEMENTACIÓN

1. **Crear script generador completo**
2. **Implementar validaciones de integridad**
3. **Configurar exportación SQL**
4. **Documentar proceso de carga**
5. **Crear herramientas de verificación**

¿Procedemos con la implementación del generador de datos o prefieres ajustar algún aspecto del esquema?
