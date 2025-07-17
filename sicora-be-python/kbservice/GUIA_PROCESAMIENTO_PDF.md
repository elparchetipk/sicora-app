# Guía de Procesamiento Automático de PDFs - Reglamento del Aprendiz

## 🎯 Problema Resuelto

¿Cansado de copiar y pegar manualmente desde PDFs del reglamento del aprendiz? Esta solución automatiza completamente el proceso de:

1. ✅ **Extracción automática** de texto desde PDFs (incluso escaneados con OCR)
2. ✅ **Segmentación inteligente** por capítulos, artículos y secciones
3. ✅ **Auto-categorización** de contenido (derechos, deberes, sanciones, etc.)
4. ✅ **Limpieza y normalización** automática del texto
5. ✅ **Integración directa** con la base de conocimiento

## 🚀 Formas de Usar la Solución

### Método 1: Vía API Web (Recomendado)

```bash
# 1. Levantar el KBService
cd sicora-be-python/kbservice
pip install -r requirements.txt
uvicorn main:app --reload --port 8003

# 2. Usar el endpoint de upload
curl -X POST "http://localhost:8003/api/pdf/upload-pdf" \
     -H "Authorization: Bearer tu_token" \
     -F "file=@reglamento_aprendiz.pdf" \
     -F "content_type=policy" \
     -F "category=reglamentacion" \
     -F "target_audience=aprendices" \
     -F "auto_categorize=true"
```

### Método 2: Script CLI Especializado

```bash
# Procesar reglamento con segmentación automática
cd sicora-be-python/kbservice
python process_reglamento.py reglamento_aprendiz.pdf

# Con opciones avanzadas
python process_reglamento.py reglamento_aprendiz.pdf \
    --output reglamento_sections.json \
    --create-kb-items \
    --dry-run
```

### Método 3: Procesamiento Batch

```bash
# Para procesar múltiples documentos
python pdf_processor.py \
    --input-dir ./pdfs_reglamentos \
    --output-dir ./processed \
    --content-type policy \
    --auto-categorize
```

## 🛠️ Instalación y Configuración

### Dependencias Principales

```bash
# Navegar al directorio del KBService
cd sicora-be-python/kbservice

# Instalar dependencias
pip install -r requirements.txt

# Dependencias adicionales del sistema (Ubuntu/Debian)
sudo apt-get install tesseract-ocr tesseract-ocr-spa
sudo apt-get install libmagic1

# Para macOS
brew install tesseract tesseract-lang
brew install libmagic

# Para sistemas sin OCR (opcional)
# El sistema funcionará sin OCR, pero tendrá limitaciones con PDFs escaneados
```

### Variables de Entorno

```bash
# .env del KBService
ENABLE_PDF_PROCESSING=true
ENABLE_OCR=true  # false si no tienes tesseract
OCR_LANGUAGE=spa  # español
MAX_PDF_SIZE_MB=50
ALLOWED_PDF_TYPES=application/pdf,application/x-pdf
```

## 📋 Características del Procesador

### Extracción de Texto Multi-Método

El sistema utiliza múltiples librerías para garantizar la mejor extracción:

1. **pdfplumber** - Excelente para tablas y layout complejo
2. **PyMuPDF** - Rápido y efectivo para la mayoría de PDFs
3. **PyPDF2** - Método de fallback confiable
4. **OCR (Tesseract)** - Para PDFs escaneados (opcional)

### Segmentación Inteligente

Reconoce automáticamente la estructura del reglamento:

- ✅ **CAPÍTULOS** (I, II, III o 1, 2, 3)
- ✅ **TÍTULOS** y **SECCIONES**
- ✅ **ARTÍCULOS** (numerados)
- ✅ **Párrafos** (cuando no hay estructura clara)

### Auto-Categorización

Clasifica automáticamente el contenido:

- 📋 **derechos** - Derechos del aprendiz
- 📋 **deberes** - Obligaciones y responsabilidades
- 📋 **prohibiciones** - Conductas prohibidas
- 📋 **sanciones** - Faltas y sanciones disciplinarias
- 📋 **procedimientos** - Procesos y trámites
- 📋 **normatividad** - Normas generales

### Audiencia Objetivo

Determina automáticamente a quién va dirigido:

- 👥 **aprendices** - Contenido para estudiantes
- 👨‍🏫 **instructores** - Para docentes y formadores
- 🏢 **administrativos** - Para coordinadores y directivos
- 🌐 **all** - Contenido general

## 🔧 Demostración Rápida

```bash
# Ejecutar demostración completa
cd sicora-be-python/kbservice
python demo_pdf_processing.py
```

Esta demo:

1. Crea un PDF de ejemplo con contenido del reglamento
2. Demuestra la extracción de texto
3. Muestra la limpieza y normalización
4. Ejemplifica la segmentación automática
5. Prueba la auto-categorización

## 📊 Ejemplo de Resultado

### Input: PDF del Reglamento

```
[reglamento_aprendiz.pdf - 50 páginas]
```

### Output: Secciones Estructuradas

```json
[
  {
    "title": "CAPÍTULO I - DISPOSICIONES GENERALES",
    "content": "El presente reglamento tiene por objeto...",
    "content_type": "policy",
    "category": "normatividad",
    "target_audience": "all",
    "tags": ["reglamento", "disposiciones", "generales"],
    "metadata": {
      "section_type": "CAPÍTULO",
      "section_number": "I",
      "word_count": 245,
      "auto_category": "normatividad"
    }
  },
  {
    "title": "ARTÍCULO 3 - DERECHOS FUNDAMENTALES",
    "content": "Los aprendices del SENA tienen derecho a...",
    "content_type": "policy",
    "category": "derechos",
    "target_audience": "aprendices",
    "tags": ["derechos", "fundamentales", "aprendices"],
    "metadata": {
      "section_type": "ARTÍCULO",
      "section_number": "3",
      "word_count": 156
    }
  }
]
```

## 🔄 Integración con el Sistema

### Con el API Gateway

El endpoint está expuesto a través del API Gateway:

```bash
# A través del API Gateway
curl -X POST "http://localhost:8000/api/kb/upload-pdf" \
     -H "Authorization: Bearer tu_token" \
     -F "file=@reglamento.pdf"
```

### Con el Frontend (React)

```typescript
// Componente de ejemplo para el frontend
const uploadReglamento = async (file: File) => {
  const formData = new FormData();
  formData.append('file', file);
  formData.append('content_type', 'policy');
  formData.append('auto_categorize', 'true');

  const response = await fetch('/api/kb/upload-pdf', {
    method: 'POST',
    headers: {
      Authorization: `Bearer ${token}`,
    },
    body: formData,
  });

  const result = await response.json();
  // result contiene las secciones procesadas
};
```

## 🎯 Casos de Uso Específicos

### 1. Reglamento del Aprendiz Completo

```bash
python process_reglamento.py reglamento_aprendiz_2024.pdf
# → Genera ~50-80 secciones categorizadas automáticamente
```

### 2. Manuales de Procedimientos

```bash
python pdf_processor.py manual_procedimientos.pdf \
    --content-type guide \
    --category procedimientos
```

### 3. Políticas Institucionales

```bash
curl -X POST "/api/pdf/upload-pdf" \
     -F "file=@politica_evaluacion.pdf" \
     -F "content_type=policy" \
     -F "category=evaluacion"
```

## 🚨 Solución de Problemas

### PDF no se procesa correctamente

```bash
# Verificar dependencias
pip list | grep -E "(PyPDF2|pdfplumber|pymupdf)"

# Probar con OCR habilitado
python process_reglamento.py archivo.pdf --use-ocr
```

### Texto extraído con errores

```bash
# El sistema intenta múltiples métodos automáticamente
# Revisa los logs para ver qué método funcionó mejor
tail -f logs/kbservice.log
```

### Categorización incorrecta

```bash
# Usar categorización manual
curl -X POST "/api/pdf/upload-pdf" \
     -F "file=@documento.pdf" \
     -F "category=categoria_especifica" \
     -F "auto_categorize=false"
```

## 📈 Beneficios vs Método Manual

| Aspecto               | Manual (Copy/Paste)         | Automático (Este Sistema)  |
| --------------------- | --------------------------- | -------------------------- |
| ⏱️ **Tiempo**         | 2-4 horas por documento     | 2-5 minutos por documento  |
| 🎯 **Precisión**      | Errores de transcripción    | Extracción exacta del PDF  |
| 📊 **Estructuración** | Manual y propensa a errores | Automática y consistente   |
| 🏷️ **Categorización** | Manual                      | Automática con IA          |
| 📋 **Metadatos**      | No incluidos                | Automáticos y enriquecidos |
| 🔄 **Escalabilidad**  | No escalable                | Procesamiento batch        |
| 💾 **Consistencia**   | Variable                    | Estándar y reproducible    |

## 🎉 ¡Listo para Usar!

Tu solución para automatizar la carga del reglamento del aprendiz ya está implementada. Solo necesitas:

1. **Instalar dependencias** (`pip install -r requirements.txt`)
2. **Configurar OCR** (opcional, para PDFs escaneados)
3. **Subir tu PDF** (vía API o script)
4. **¡Disfrutar del contenido estructurado!**

¿Necesitas procesar el reglamento ahora mismo? Ejecuta:

```bash
cd sicora-be-python/kbservice
python demo_pdf_processing.py  # Para ver cómo funciona
# Luego usa tu PDF real:
python process_reglamento.py tu_reglamento.pdf
```
