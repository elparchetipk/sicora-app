# 📄 PDF Processing para SICORA KBService

Esta es una extensión del KBService para procesar documentos PDF automáticamente y extraer su contenido para la base de conocimiento.

## 🎯 Funcionalidades

- ✅ **Extracción de texto** de PDFs con múltiples engines
- ✅ **Limpieza automática** de texto extraído
- ✅ **Detección de metadatos** del documento
- ✅ **Segmentación inteligente** por secciones/capítulos
- ✅ **OCR** para PDFs escaneados
- ✅ **Carga automática** al KBService
- ✅ **Procesamiento en batch** de múltiples PDFs

## 📦 Dependencias Adicionales

Agregar al `requirements.txt` del KBService:

```
# PDF Processing
PyPDF2==3.0.1
pdfplumber==0.10.3
pymupdf==1.23.26
pytesseract==0.3.10
Pillow==10.1.0

# Text Processing
python-magic==0.4.27
chardet==5.2.0
langdetect==1.0.9
```

## 🚀 Uso Rápido

```bash
# Procesar un PDF individual
python pdf_processor.py --file reglamento_aprendiz.pdf --content-type policy

# Procesamiento en batch
python pdf_processor.py --batch-dir documentos_sena/ --auto-categorize

# Con OCR para PDFs escaneados
python pdf_processor.py --file documento_escaneado.pdf --ocr --content-type procedure
```
