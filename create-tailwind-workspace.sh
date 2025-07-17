#!/bin/bash

# Script para crear estructura de workspace ws-tw-2025
# Crea una carpeta padre ws-tw-2025 con subcarpetas dia1 a dia48
# Cada día incluye estructura completa con archivos base

set -e

# Colores para output
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

print_status() {
    echo -e "${GREEN}✅ $1${NC}"
}

print_info() {
    echo -e "${BLUE}ℹ️  $1${NC}"
}

print_warning() {
    echo -e "${YELLOW}⚠️  $1${NC}"
}

# Configuración
WORKSPACE_NAME="ws-tw-2025"
TOTAL_DAYS=48

echo ""
echo -e "${BLUE}🚀 Creando workspace Workdskills Tecnologías Web 2025${NC}"
echo -e "${BLUE}═══════════════════════════════════════${NC}"
echo ""

# Verificar si ya existe
if [ -d "$WORKSPACE_NAME" ]; then
    print_warning "La carpeta $WORKSPACE_NAME ya existe"
    echo "¿Deseas eliminarla y crearla nuevamente? [y/N]"
    read -r response
    if [[ "$response" =~ ^[Yy]$ ]]; then
        rm -rf "$WORKSPACE_NAME"
        print_status "Carpeta anterior eliminada"
    else
        print_info "Cancelado por el usuario"
        exit 0
    fi
fi

# Crear carpeta principal
mkdir -p "$WORKSPACE_NAME"
print_status "Carpeta principal creada: $WORKSPACE_NAME"

# Función para crear contenido de index.html
create_index_html() {
    local day_number=$1
    cat > "index.html" << EOF
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Día $day_number - WorldSkills Tecnologías Web 2025</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <link rel="stylesheet" href="./_css/styles.css">
</head>
<body class="bg-gray-100 font-sans">
    <div class="container mx-auto px-4 py-8">
        <header class="text-center mb-8">
            <h1 class="text-4xl font-bold text-blue-600 mb-2">
                TailwindCSS Workshop 2025
            </h1>
            <h2 class="text-2xl text-gray-700">
                Día $day_number - Práctica Diaria
            </h2>
        </header>
        
        <main class="max-w-4xl mx-auto">
            <div class="bg-white rounded-lg shadow-md p-6 mb-6">
                <h3 class="text-xl font-semibold mb-4">Objetivo del Día</h3>
                <p class="text-gray-600">
                    Aquí va el contenido y ejercicios para el día $day_number.
                </p>
            </div>
            
            <div class="grid md:grid-cols-2 gap-6">
                <div class="bg-white rounded-lg shadow-md p-6">
                    <h4 class="text-lg font-semibold mb-3">Conceptos</h4>
                    <ul class="space-y-2 text-gray-600">
                        <li>• Concepto 1</li>
                        <li>• Concepto 2</li>
                        <li>• Concepto 3</li>
                    </ul>
                </div>
                
                <div class="bg-white rounded-lg shadow-md p-6">
                    <h4 class="text-lg font-semibold mb-3">Ejercicios</h4>
                    <ul class="space-y-2 text-gray-600">
                        <li>• Ejercicio 1</li>
                        <li>• Ejercicio 2</li>
                        <li>• Ejercicio 3</li>
                    </ul>
                </div>
            </div>
        </main>
        
        <footer class="text-center mt-8 text-gray-500">
            <p>TailwindCSS Workshop 2025 - Día $day_number</p>
        </footer>
    </div>
    
    <script src="./_js/main.js"></script>
</body>
</html>
EOF
}

# Función para crear contenido de README.md
create_readme() {
    local day_number=$1
    cat > "README.md" << EOF
# Día $day_number - TailwindCSS Workshop 2025

## 📋 Objetivo del Día

Descripción de los objetivos y conceptos a aprender en el día $day_number.

## 🎯 Conceptos Clave

- [ ] Concepto 1
- [ ] Concepto 2  
- [ ] Concepto 3

## 🛠️ Ejercicios

### Ejercicio 1
Descripción del primer ejercicio.

### Ejercicio 2
Descripción del segundo ejercicio.

### Ejercicio 3
Descripción del tercer ejercicio.

## 📁 Estructura de Archivos

\`\`\`
dia$day_number/
├── _css/
│   └── styles.css
├── _html/
│   └── (archivos HTML adicionales)
├── _img/
│   └── (imágenes del proyecto)
├── _js/
│   └── main.js
├── index.html
└── README.md
\`\`\`

## 📚 Recursos

- [Documentación TailwindCSS](https://tailwindcss.com/docs)
- [Guía de utilidades](https://tailwindcss.com/docs/utility-first)
- [Ejemplos de componentes](https://tailwindui.com/components)

## ✅ Checklist de Completado

- [ ] Ejercicio 1 completado
- [ ] Ejercicio 2 completado
- [ ] Ejercicio 3 completado
- [ ] Código revisado
- [ ] Documentación actualizada

---

**Día $day_number de 48** | **TailwindCSS Workshop 2025**
EOF
}

# Función para crear CSS base
create_base_css() {
    cat > "styles.css" << EOF
/* Estilos personalizados para el día */
/* TailwindCSS Workshop 2025 */

/* Variables CSS personalizadas */
:root {
  --primary-color: #3b82f6;
  --secondary-color: #64748b;
  --accent-color: #10b981;
}

/* Estilos adicionales que complementan TailwindCSS */
.custom-gradient {
  background: linear-gradient(135deg, var(--primary-color), var(--accent-color));
}

.custom-shadow {
  box-shadow: 0 10px 25px rgba(0, 0, 0, 0.1);
}

/* Animaciones personalizadas */
@keyframes fadeInUp {
  from {
    opacity: 0;
    transform: translateY(20px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

.animate-fadeInUp {
  animation: fadeInUp 0.6s ease-out;
}

/* Responsive helpers adicionales */
@media (max-width: 640px) {
  .mobile-padding {
    padding: 1rem;
  }
}
EOF
}

# Función para crear JS base
create_base_js() {
    local day_number=$1
    cat > "main.js" << EOF
// JavaScript para el Día $day_number
// TailwindCSS Workshop 2025

document.addEventListener('DOMContentLoaded', function() {
    console.log('Día $day_number - TailwindCSS Workshop 2025');
    
    // Inicialización de componentes
    initializeComponents();
    
    // Event listeners
    setupEventListeners();
});

function initializeComponents() {
    // Agregar animaciones a elementos
    const elements = document.querySelectorAll('.animate-fadeInUp');
    elements.forEach((el, index) => {
        el.style.animationDelay = \`\${index * 0.1}s\`;
    });
}

function setupEventListeners() {
    // Event listeners para interacciones
    
    // Ejemplo: Toggle mobile menu
    const menuToggle = document.querySelector('[data-menu-toggle]');
    const mobileMenu = document.querySelector('[data-mobile-menu]');
    
    if (menuToggle && mobileMenu) {
        menuToggle.addEventListener('click', function() {
            mobileMenu.classList.toggle('hidden');
        });
    }
    
    // Ejemplo: Smooth scroll
    const scrollLinks = document.querySelectorAll('a[href^="#"]');
    scrollLinks.forEach(link => {
        link.addEventListener('click', function(e) {
            e.preventDefault();
            const target = document.querySelector(this.getAttribute('href'));
            if (target) {
                target.scrollIntoView({
                    behavior: 'smooth'
                });
            }
        });
    });
}

// Utilidades adicionales
function toggleClass(element, className) {
    element.classList.toggle(className);
}

function addClass(element, className) {
    element.classList.add(className);
}

function removeClass(element, className) {
    element.classList.remove(className);
}

// Función para mostrar notificaciones
function showNotification(message, type = 'info') {
    const notification = document.createElement('div');
    notification.className = \`
        fixed top-4 right-4 p-4 rounded-lg shadow-lg z-50
        \${type === 'success' ? 'bg-green-500' : 
          type === 'error' ? 'bg-red-500' : 
          type === 'warning' ? 'bg-yellow-500' : 'bg-blue-500'}
        text-white transform transition-transform duration-300 translate-x-full
    \`;
    notification.textContent = message;
    
    document.body.appendChild(notification);
    
    // Animar entrada
    setTimeout(() => {
        notification.classList.remove('translate-x-full');
    }, 100);
    
    // Remover después de 3 segundos
    setTimeout(() => {
        notification.classList.add('translate-x-full');
        setTimeout(() => {
            document.body.removeChild(notification);
        }, 300);
    }, 3000);
}
EOF
}

# Crear estructura para cada día
cd "$WORKSPACE_NAME"

for day in $(seq 1 $TOTAL_DAYS); do
    day_folder="dia$day"
    
    # Crear carpeta del día
    mkdir -p "$day_folder"
    cd "$day_folder"
    
    # Crear subcarpetas
    mkdir -p "_css"
    mkdir -p "_html" 
    mkdir -p "_img"
    mkdir -p "_js"
    
    # Crear archivos .gitkeep para mantener carpetas vacías en git
    touch "_css/.gitkeep"
    touch "_html/.gitkeep"
    touch "_img/.gitkeep"
    touch "_js/.gitkeep"
    
    # Crear archivos base
    create_index_html $day
    create_readme $day
    
    # Crear CSS personalizado
    cd "_css"
    create_base_css
    cd ..
    
    # Crear JS base
    cd "_js"
    create_base_js $day
    cd ..
    
    # Volver a la carpeta principal
    cd ..
    
    # Mostrar progreso cada 10 días
    if [ $((day % 10)) -eq 0 ]; then
        print_status "Creados $day de $TOTAL_DAYS días..."
    fi
done

# Crear README principal del workspace
cat > "README.md" << EOF
# 🎨 TailwindCSS Workshop 2025

Workspace completo para aprender TailwindCSS durante 48 días de práctica intensiva.

## 📋 Descripción

Este workspace contiene **48 días de ejercicios prácticos** para dominar TailwindCSS desde conceptos básicos hasta técnicas avanzadas.

## 🗂️ Estructura del Proyecto

\`\`\`
ws-tw-2025/
├── dia1/
│   ├── _css/
│   │   ├── styles.css
│   │   └── .gitkeep
│   ├── _html/
│   │   └── .gitkeep
│   ├── _img/
│   │   └── .gitkeep
│   ├── _js/
│   │   ├── main.js
│   │   └── .gitkeep
│   ├── index.html
│   └── README.md
├── dia2/
│   └── ... (misma estructura)
├── ...
├── dia48/
│   └── ... (misma estructura)
└── README.md
\`\`\`

## 🎯 Objetivos del Workshop

### Semana 1-2 (Días 1-14): Fundamentos
- Configuración y conceptos básicos
- Utilidades de layout y spacing
- Typography y colores
- Responsive design básico

### Semana 3-4 (Días 15-28): Intermedio
- Flexbox y Grid con TailwindCSS
- Componentes interactivos
- Animaciones y transiciones
- Formularios y navegación

### Semana 5-6 (Días 29-42): Avanzado
- Personalización del tema
- Plugins y extensiones
- Optimización y build
- Patrones de diseño avanzados

### Semana 7 (Días 43-48): Proyecto Final
- Desarrollo de proyecto completo
- Best practices
- Performance optimization
- Deployment

## 🚀 Cómo Usar Este Workspace

1. **Navega a cada día**: \`cd dia1\`, \`cd dia2\`, etc.
2. **Lee el README.md** de cada día para entender los objetivos
3. **Abre index.html** en tu navegador para ver el resultado
4. **Edita los archivos** según los ejercicios propuestos
5. **Marca como completado** en el checklist del README

## 📚 Recursos Recomendados

- [Documentación oficial de TailwindCSS](https://tailwindcss.com/docs)
- [TailwindCSS Playground](https://play.tailwindcss.com/)
- [Tailwind UI Components](https://tailwindui.com/components)
- [Headless UI](https://headlessui.com/)

## 🛠️ Herramientas Necesarias

- Editor de código (VS Code recomendado)
- Navegador web moderno
- Extensión TailwindCSS IntelliSense (opcional pero recomendado)
- Node.js (para proyectos avanzados)

## 📈 Progreso

- [ ] Días 1-7: Fundamentos básicos
- [ ] Días 8-14: Layout y responsive
- [ ] Días 15-21: Componentes interactivos
- [ ] Días 22-28: Animaciones y efectos
- [ ] Días 29-35: Personalización avanzada
- [ ] Días 36-42: Optimización y plugins
- [ ] Días 43-48: Proyecto final

## 🎨 Estructura de Archivos por Día

Cada día incluye:
- **index.html**: Archivo principal con ejercicios
- **README.md**: Objetivos y instrucciones del día
- **_css/styles.css**: Estilos personalizados complementarios
- **_js/main.js**: JavaScript para interactividad
- **_html/**: Archivos HTML adicionales
- **_img/**: Imágenes y assets
- **.gitkeep**: Para mantener carpetas en control de versiones

## 📝 Notas

- Cada día está diseñado para **1-2 horas de práctica**
- Los ejercicios van incrementando en dificultad
- Se incluyen **ejemplos prácticos** y **proyectos reales**
- Todos los archivos están **pre-configurados** y listos para usar

---

**¡Bienvenido al TailwindCSS Workshop 2025!** 🚀

*Creado el $(date '+%d de %B de %Y')*
EOF

# Crear archivo .gitignore
cat > ".gitignore" << EOF
# Archivos del sistema
.DS_Store
Thumbs.db

# Logs
*.log
npm-debug.log*

# Dependencias
node_modules/

# Build outputs
dist/
build/

# Archivos temporales
*.tmp
*.temp

# IDE
.vscode/settings.json
.idea/

# Archivos de configuración local
.env.local
EOF

print_status "Workspace completo creado exitosamente!"
echo ""
print_info "📊 Resumen:"
echo "   • Carpeta principal: $WORKSPACE_NAME"
echo "   • Días creados: $TOTAL_DAYS"
echo "   • Archivos por día: 6 (index.html, README.md, styles.css, main.js, 4 .gitkeep)"
echo "   • Total de archivos: $((TOTAL_DAYS * 6 + 3)) archivos"
echo ""
print_info "🚀 Próximos pasos:"
echo "   1. cd $WORKSPACE_NAME"
echo "   2. cd dia1"
echo "   3. Abre index.html en tu navegador"
echo "   4. ¡Comienza a aprender TailwindCSS!"
echo ""
print_status "¡Feliz aprendizaje! 🎨"
