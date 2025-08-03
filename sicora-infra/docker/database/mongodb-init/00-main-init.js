// MongoDB Initialization Script for SICORA
// This script creates the initial databases and collections for MongoDB integration

print('🍃 Starting MongoDB initialization for SICORA...');

// Switch to sicora_nosql database
db = db.getSiblingDB('sicora_nosql');

print('📊 Creating sicora_nosql database...');

// Create collections with validation schemas
print('📋 Creating Knowledge Base collections...');

// Knowledge Base Articles Collection
db.createCollection('kb_articles', {
  validator: {
    $jsonSchema: {
      bsonType: 'object',
      required: ['title', 'content', 'category', 'author', 'created_at'],
      properties: {
        title: {
          bsonType: 'string',
          description: 'Article title - required',
        },
        content: {
          bsonType: 'string',
          description: 'Article content - required',
        },
        category: {
          bsonType: 'string',
          enum: [
            'tutorial',
            'faq',
            'documentation',
            'guide',
            'troubleshooting',
          ],
          description: 'Article category - required',
        },
        author: {
          bsonType: 'string',
          description: 'Author name - required',
        },
        tags: {
          bsonType: 'array',
          items: {
            bsonType: 'string',
          },
          description: 'Article tags for search',
        },
        status: {
          bsonType: 'string',
          enum: ['draft', 'published', 'archived'],
          description: 'Article status',
        },
        created_at: {
          bsonType: 'date',
          description: 'Creation timestamp - required',
        },
        updated_at: {
          bsonType: 'date',
          description: 'Last update timestamp',
        },
        metadata: {
          bsonType: 'object',
          description: 'Additional metadata as flexible object',
        },
      },
    },
  },
});

// Dynamic Evaluations Collection
print('📝 Creating Evaluation collections...');

db.createCollection('dynamic_evaluations', {
  validator: {
    $jsonSchema: {
      bsonType: 'object',
      required: ['evaluation_id', 'form_schema', 'created_at'],
      properties: {
        evaluation_id: {
          bsonType: 'string',
          description: 'Unique evaluation identifier - required',
        },
        form_schema: {
          bsonType: 'object',
          description: 'Dynamic form schema definition - required',
        },
        responses: {
          bsonType: 'array',
          items: {
            bsonType: 'object',
          },
          description: 'Evaluation responses array',
        },
        created_at: {
          bsonType: 'date',
          description: 'Creation timestamp - required',
        },
        updated_at: {
          bsonType: 'date',
          description: 'Last update timestamp',
        },
      },
    },
  },
});

// Audit Logs Collection
print('🔍 Creating Audit Log collections...');

db.createCollection('audit_logs', {
  validator: {
    $jsonSchema: {
      bsonType: 'object',
      required: ['action', 'user_id', 'timestamp', 'details'],
      properties: {
        action: {
          bsonType: 'string',
          description: 'Action performed - required',
        },
        user_id: {
          bsonType: 'string',
          description: 'User who performed the action - required',
        },
        timestamp: {
          bsonType: 'date',
          description: 'Action timestamp - required',
        },
        details: {
          bsonType: 'object',
          description: 'Action details - required',
        },
        ip_address: {
          bsonType: 'string',
          description: 'Client IP address',
        },
        user_agent: {
          bsonType: 'string',
          description: 'Client user agent',
        },
      },
    },
  },
});

// Notifications Collection
print('📧 Creating Notification collections...');

db.createCollection('notifications', {
  validator: {
    $jsonSchema: {
      bsonType: 'object',
      required: ['recipient_id', 'message', 'type', 'created_at'],
      properties: {
        recipient_id: {
          bsonType: 'string',
          description: 'Notification recipient - required',
        },
        message: {
          bsonType: 'object',
          description: 'Notification message content - required',
        },
        type: {
          bsonType: 'string',
          enum: ['email', 'push', 'in_app', 'sms'],
          description: 'Notification type - required',
        },
        status: {
          bsonType: 'string',
          enum: ['pending', 'sent', 'delivered', 'failed'],
          description: 'Notification status',
        },
        created_at: {
          bsonType: 'date',
          description: 'Creation timestamp - required',
        },
        sent_at: {
          bsonType: 'date',
          description: 'Sent timestamp',
        },
        metadata: {
          bsonType: 'object',
          description: 'Additional notification metadata',
        },
      },
    },
  },
});

// Create indexes for performance
print('🚀 Creating indexes for performance...');

// KB Articles indexes
db.kb_articles.createIndex(
  { title: 'text', content: 'text', tags: 'text' },
  { name: 'text_search_index' }
);
db.kb_articles.createIndex({ category: 1 });
db.kb_articles.createIndex({ status: 1 });
db.kb_articles.createIndex({ created_at: -1 });

// Dynamic Evaluations indexes
db.dynamic_evaluations.createIndex({ evaluation_id: 1 }, { unique: true });
db.dynamic_evaluations.createIndex({ created_at: -1 });

// Audit Logs indexes
db.audit_logs.createIndex({ user_id: 1 });
db.audit_logs.createIndex({ action: 1 });
db.audit_logs.createIndex({ timestamp: -1 });
db.audit_logs.createIndex({ user_id: 1, timestamp: -1 });

// Notifications indexes
db.notifications.createIndex({ recipient_id: 1 });
db.notifications.createIndex({ status: 1 });
db.notifications.createIndex({ type: 1 });
db.notifications.createIndex({ created_at: -1 });

// Insert sample data for educational purposes
print('📊 Inserting sample data...');

// Sample KB Article
db.kb_articles.insertOne({
  title: 'Cómo usar MongoDB en SICORA',
  content:
    'MongoDB es una base de datos NoSQL que nos permite almacenar documentos JSON flexibles...',
  category: 'tutorial',
  author: 'OneVision Team',
  tags: ['mongodb', 'nosql', 'tutorial', 'sicora'],
  status: 'published',
  created_at: new Date(),
  updated_at: new Date(),
  metadata: {
    difficulty: 'beginner',
    reading_time: '5 minutes',
    language: 'español',
  },
});

// Sample Dynamic Evaluation
db.dynamic_evaluations.insertOne({
  evaluation_id: 'eval_mongodb_intro',
  form_schema: {
    title: 'Evaluación MongoDB - Introducción',
    fields: [
      {
        name: 'nombre',
        type: 'text',
        required: true,
        label: 'Nombre completo',
      },
      {
        name: 'experiencia_mongodb',
        type: 'select',
        options: ['Ninguna', 'Básica', 'Intermedia', 'Avanzada'],
        label: 'Nivel de experiencia con MongoDB',
      },
      {
        name: 'comentarios',
        type: 'textarea',
        label: 'Comentarios adicionales',
      },
    ],
  },
  responses: [],
  created_at: new Date(),
  updated_at: new Date(),
});

// Sample Audit Log
db.audit_logs.insertOne({
  action: 'mongodb_init',
  user_id: 'system',
  timestamp: new Date(),
  details: {
    operation: 'database_initialization',
    collections_created: [
      'kb_articles',
      'dynamic_evaluations',
      'audit_logs',
      'notifications',
    ],
    indexes_created: 12,
  },
  ip_address: '127.0.0.1',
  user_agent: 'MongoDB Shell',
});

// Sample Notification
db.notifications.insertOne({
  recipient_id: 'admin@onevision.com',
  message: {
    subject: 'MongoDB integrado exitosamente en SICORA',
    body: 'La base de datos MongoDB ha sido configurada correctamente y está lista para usar.',
    priority: 'info',
  },
  type: 'in_app',
  status: 'pending',
  created_at: new Date(),
  metadata: {
    category: 'system',
    auto_generated: true,
  },
});

print('✅ MongoDB initialization completed successfully!');
print(
  '📊 Collections created: kb_articles, dynamic_evaluations, audit_logs, notifications'
);
print('🚀 Indexes created for optimal performance');
print('📋 Sample data inserted for educational purposes');
print('🎯 SICORA MongoDB is ready to use!');
