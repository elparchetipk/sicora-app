// MongoDB Sample Data for SICORA OneVision
// This script populates the database with sample data for development

// Switch to main application database
db = db.getSiblingDB('sicora_mongodb');

// Insert sample user preferences
db.user_preferences.insertMany([
  {
    userId: 'user_001',
    preferences: {
      theme: 'dark',
      language: 'es',
      notifications: {
        email: true,
        browser: true,
        sms: false,
      },
      dashboard: {
        layout: 'grid',
        widgets: ['calendar', 'tasks', 'notifications'],
      },
    },
    createdAt: new Date(),
    updatedAt: new Date(),
  },
  {
    userId: 'user_002',
    preferences: {
      theme: 'light',
      language: 'es',
      notifications: {
        email: true,
        browser: false,
        sms: true,
      },
      dashboard: {
        layout: 'list',
        widgets: ['calendar', 'grades'],
      },
    },
    createdAt: new Date(),
    updatedAt: new Date(),
  },
]);

// Insert sample file metadata
db.file_metadata.insertMany([
  {
    filename: 'proyecto_final.pdf',
    originalName: 'Proyecto Final - Desarrollo Web.pdf',
    userId: 'user_001',
    fileSize: 2048000,
    mimeType: 'application/pdf',
    uploadedAt: new Date(),
    tags: ['proyecto', 'desarrollo', 'web'],
    description: 'Documento del proyecto final de desarrollo web',
  },
  {
    filename: 'presentacion.pptx',
    originalName: 'Presentación - OneVision.pptx',
    userId: 'user_002',
    fileSize: 5120000,
    mimeType:
      'application/vnd.openxmlformats-officedocument.presentationml.presentation',
    uploadedAt: new Date(),
    tags: ['presentacion', 'onevision'],
    description: 'Presentación sobre la plataforma OneVision',
  },
]);

// Switch to AI database
db = db.getSiblingDB('sicora_ai');

// Insert sample AI prompts
db.ai_prompts.insertMany([
  {
    template: 'onevision_coordinator',
    category: 'educational',
    content:
      'Eres un coordinador académico de OneVision especializado en {program}. Asiste con {query}.',
    context: 'OneVision - OneVision Open Source, Educational Platform',
    instructions:
      'Proporciona información precisa sobre programas, procesos y normativas de OneVision.',
    createdAt: new Date(),
    isActive: true,
  },
  {
    template: 'student_assistant',
    category: 'educational',
    content:
      'Eres un asistente educativo que ayuda a estudiantes de OneVision con {subject}. Responde a: {query}',
    context: 'Asistente educativo para estudiantes OneVision',
    instructions:
      'Proporciona explicaciones claras y ejemplos prácticos. Adapta el lenguaje al nivel del estudiante.',
    createdAt: new Date(),
    isActive: true,
  },
]);

// Insert sample AI models configuration
db.ai_models.insertMany([
  {
    modelName: 'gpt-3.5-turbo',
    provider: 'openai',
    configuration: {
      temperature: 0.7,
      maxTokens: 1000,
      topP: 1.0,
    },
    isActive: true,
    usage: {
      totalRequests: 0,
      totalTokens: 0,
    },
    createdAt: new Date(),
  },
]);

// Switch to Knowledge Base database
db = db.getSiblingDB('sicora_kb');

// Insert sample documents
db.documents.insertMany([
  {
    title: 'Guía de OneVision Open Source',
    content:
      'OneVision es una plataforma educativa open source diseñada para instituciones académicas. Proporciona herramientas para gestión de estudiantes, evaluaciones, y seguimiento académico.',
    category: 'documentation',
    author: 'OneVision Team',
    uploadedAt: new Date(),
    isPublic: true,
    tags: ['onevision', 'guia', 'open-source'],
    version: '1.0',
  },
  {
    title: 'Manual de Usuario - Sistema de Evaluaciones',
    content:
      'El sistema de evaluaciones de OneVision permite a instructores crear, gestionar y calificar evaluaciones de manera eficiente. Incluye soporte para diferentes tipos de preguntas y calificación automática.',
    category: 'manual',
    author: 'OneVision Team',
    uploadedAt: new Date(),
    isPublic: true,
    tags: ['evaluaciones', 'manual', 'instructores'],
    version: '1.0',
  },
]);

// Switch to logs database
db = db.getSiblingDB('sicora_logs');

// Insert sample application logs
db.application_logs.insertMany([
  {
    timestamp: new Date(),
    level: 'INFO',
    service: 'userservice',
    message: 'User authentication successful',
    userId: 'user_001',
    metadata: {
      ip: '192.168.1.100',
      userAgent: 'Mozilla/5.0...',
    },
  },
  {
    timestamp: new Date(),
    level: 'INFO',
    service: 'aiservice',
    message: 'AI prompt processed successfully',
    userId: 'user_002',
    metadata: {
      promptType: 'onevision_coordinator',
      tokensUsed: 150,
    },
  },
]);

print('✅ Sample data inserted successfully into MongoDB');
print(
  '📊 Data inserted into: sicora_mongodb, sicora_ai, sicora_kb, sicora_logs'
);
print('🧪 Ready for development and testing');
