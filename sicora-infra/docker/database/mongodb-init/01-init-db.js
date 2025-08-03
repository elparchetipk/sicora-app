// MongoDB Initialization Script for SICORA
// This script creates the basic database structure and users

// Switch to admin database
db = db.getSiblingDB('admin');

// Create application user
db.createUser({
  user: 'sicora_mongodb_user',
  pwd: 'sicora_mongodb_2024',
  roles: [
    { role: 'readWrite', db: 'sicora_mongodb' },
    { role: 'readWrite', db: 'sicora_ai' },
    { role: 'readWrite', db: 'sicora_kb' },
    { role: 'readWrite', db: 'sicora_logs' },
  ],
});

// Switch to main application database
db = db.getSiblingDB('sicora_mongodb');

// Create basic collections
db.createCollection('user_sessions');
db.createCollection('user_preferences');
db.createCollection('file_metadata');
db.createCollection('system_logs');

// Create indexes for performance
db.user_sessions.createIndex({ userId: 1 });
db.user_sessions.createIndex({ sessionToken: 1 }, { unique: true });
db.user_sessions.createIndex({ expiresAt: 1 }, { expireAfterSeconds: 0 });

db.user_preferences.createIndex({ userId: 1 }, { unique: true });
db.file_metadata.createIndex({ userId: 1 });
db.file_metadata.createIndex({ filename: 1 });
db.system_logs.createIndex({ timestamp: 1 });
db.system_logs.createIndex({ level: 1 });

// Switch to AI database
db = db.getSiblingDB('sicora_ai');

// Create AI-related collections
db.createCollection('ai_conversations');
db.createCollection('ai_prompts');
db.createCollection('ai_responses');
db.createCollection('ai_models');

// Create indexes for AI collections
db.ai_conversations.createIndex({ userId: 1 });
db.ai_conversations.createIndex({ sessionId: 1 });
db.ai_conversations.createIndex({ timestamp: 1 });

db.ai_prompts.createIndex({ template: 1 });
db.ai_prompts.createIndex({ category: 1 });

db.ai_responses.createIndex({ conversationId: 1 });
db.ai_responses.createIndex({ timestamp: 1 });

// Switch to Knowledge Base database
db = db.getSiblingDB('sicora_kb');

// Create KB collections
db.createCollection('documents');
db.createCollection('document_chunks');
db.createCollection('embeddings');
db.createCollection('search_history');

// Create indexes for KB collections
db.documents.createIndex({ title: 'text', content: 'text' });
db.documents.createIndex({ category: 1 });
db.documents.createIndex({ uploadedAt: 1 });

db.document_chunks.createIndex({ documentId: 1 });
db.embeddings.createIndex({ chunkId: 1 });
db.search_history.createIndex({ userId: 1 });

// Switch to logs database
db = db.getSiblingDB('sicora_logs');

// Create logging collections
db.createCollection('application_logs');
db.createCollection('audit_logs');
db.createCollection('performance_metrics');

// Create indexes for logs
db.application_logs.createIndex({ timestamp: 1 });
db.application_logs.createIndex({ level: 1 });
db.application_logs.createIndex({ service: 1 });

db.audit_logs.createIndex({ timestamp: 1 });
db.audit_logs.createIndex({ userId: 1 });
db.audit_logs.createIndex({ action: 1 });

db.performance_metrics.createIndex({ timestamp: 1 });
db.performance_metrics.createIndex({ service: 1 });

print('✅ MongoDB initialization completed successfully for SICORA OneVision');
print(
  '📊 Databases created: sicora_mongodb, sicora_ai, sicora_kb, sicora_logs'
);
print('👤 User created: sicora_mongodb_user');
print('🔍 Indexes created for optimal performance');
