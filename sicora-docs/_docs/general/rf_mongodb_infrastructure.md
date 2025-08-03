# 🍃 **INFRAESTRUCTURA MONGODB - ESPECIFICACIÓN COMPLETA**

**Actualizado: 3 de agosto de 2025**

Este documento define la infraestructura completa de MongoDB para el proyecto SICORA, alineada con la estrategia existente de PostgreSQL y Redis.

---

## 🎯 **ESTRATEGIA CONSOLIDADA DE INFRAESTRUCTURA**

### **Principio Fundamental: Arquitectura Híbrida Educativa**

Siguiendo la filosofía de SICORA de maximizar el aprendizaje sobre diferentes tecnologías de bases de datos:

```
┌─────────────────────────────────────────────────────────────────┐
│                    SICORA Database Strategy                     │
├─────────────────────────────────────────────────────────────────┤
│ PostgreSQL 15        │ Redis Cluster        │ MongoDB 8.x       │
│ (RDBMS Primary)      │ (Cache & Sessions)   │ (NoSQL Documents) │
├─────────────────────────────────────────────────────────────────┤
│ • Transactional      │ • Session Store      │ • Flexible Schema │
│ • ACID Compliance    │ • Distributed Cache  │ • JSON Documents  │
│ • Schema Strict      │ • Pub/Sub            │ • Full-text Search│
│ • Master-Slave Rep   │ • Failover Auto      │ • Aggregations    │
│ • Multiple Schemas   │ • 3M + 3S Cluster    │ • Replica Sets    │
└─────────────────────────────────────────────────────────────────┘
```

### **Beneficios Educativos de la Arquitectura Híbrida**

1. **Comparación Práctica**: Estudiantes experimentan cuándo usar cada tecnología
2. **Casos de Uso Reales**: Diferentes problemas requieren diferentes soluciones
3. **Performance Analysis**: Benchmarking entre tecnologías
4. **Operaciones Complejas**: Gestión de múltiples sistemas de bases de datos

---

## 🏗️ **ARQUITECTURA MONGODB**

### **Configuración de Producción**

#### **Replica Set Deployment**

```yaml
# MongoDB Production Architecture
MongoDB Replica Set:
  Primary: sicora-mongo-primary
    - IP: 10.0.1.10
    - Port: 27017
    - Role: Read/Write Operations
    - Resources: 4 vCPU, 8GB RAM, 100GB SSD

  Secondary 1: sicora-mongo-secondary-1
    - IP: 10.0.1.11
    - Port: 27017
    - Role: Read Operations + Backup Source
    - Resources: 2 vCPU, 4GB RAM, 100GB SSD

  Secondary 2: sicora-mongo-secondary-2
    - IP: 10.0.1.12
    - Port: 27017
    - Role: Read Operations + Analytics
    - Resources: 2 vCPU, 4GB RAM, 100GB SSD

  Arbiter: sicora-mongo-arbiter
    - IP: 10.0.1.13
    - Port: 27017
    - Role: Election Participation Only
    - Resources: 1 vCPU, 1GB RAM, 10GB SSD
```

#### **Database Structure**

```javascript
// Database and Collections Strategy
sicora_nosql: {
  // Knowledge Base Collections
  articles: {
    indexes: ["title_text", "slug_unique", "category_1", "tags_1"],
    size_estimate: "2GB",
    retention: "indefinite"
  },

  // Dynamic Evaluations
  evaluations: {
    indexes: ["type_1_version_1", "responses.evaluatedId_1"],
    size_estimate: "1GB",
    retention: "7 years (academic)"
  },

  // High-Performance Logging
  audit_logs: {
    indexes: ["timestamp_-1", "service_1_action_1", "userId_1"],
    size_estimate: "5GB/year",
    retention: "2 years (TTL)",
    ttl_index: "timestamp (63072000 seconds = 2 years)"
  },

  // Flexible Notifications
  notifications: {
    indexes: ["userId_1_status_1", "scheduledFor_1"],
    size_estimate: "500MB/year",
    retention: "1 year (TTL)"
  }
}
```

### **Configuración de Desarrollo**

#### **Docker Compose Development**

```yaml
# docker-compose.mongodb.yml
version: '3.8'

services:
  mongodb-primary:
    image: mongo:8.0-community
    container_name: sicora-mongo-primary
    ports:
      - '27017:27017'
    environment:
      MONGO_INITDB_ROOT_USERNAME: sicora_admin
      MONGO_INITDB_ROOT_PASSWORD: ${MONGO_ROOT_PASSWORD}
      MONGO_INITDB_DATABASE: sicora_nosql
      MONGO_REPLICA_SET_NAME: sicora-rs
    volumes:
      - mongodb_primary_data:/data/db
      - ./mongodb/init:/docker-entrypoint-initdb.d
      - ./mongodb/keyfile:/etc/mongodb-keyfile:ro
    command: >
      mongod --replSet sicora-rs
             --keyFile /etc/mongodb-keyfile
             --bind_ip_all
             --oplogSize 128

  mongodb-secondary-1:
    image: mongo:8.0-community
    container_name: sicora-mongo-secondary-1
    ports:
      - '27018:27017'
    environment:
      MONGO_REPLICA_SET_NAME: sicora-rs
    volumes:
      - mongodb_secondary1_data:/data/db
      - ./mongodb/keyfile:/etc/mongodb-keyfile:ro
    command: >
      mongod --replSet sicora-rs
             --keyFile /etc/mongodb-keyfile
             --bind_ip_all
             --oplogSize 128
    depends_on:
      - mongodb-primary

  mongodb-secondary-2:
    image: mongo:8.0-community
    container_name: sicora-mongo-secondary-2
    ports:
      - '27019:27017'
    environment:
      MONGO_REPLICA_SET_NAME: sicora-rs
    volumes:
      - mongodb_secondary2_data:/data/db
      - ./mongodb/keyfile:/etc/mongodb-keyfile:ro
    command: >
      mongod --replSet sicora-rs
             --keyFile /etc/mongodb-keyfile
             --bind_ip_all
             --oplogSize 128
    depends_on:
      - mongodb-primary

volumes:
  mongodb_primary_data:
  mongodb_secondary1_data:
  mongodb_secondary2_data:
```

---

## 🔐 **SEGURIDAD Y AUTENTICACIÓN**

### **Estrategia de Seguridad Multi-Nivel**

#### **1. Autenticación y Autorización**

```javascript
// User Management Strategy
{
  "admin_users": {
    "sicora_admin": {
      "role": "root",
      "databases": ["admin", "sicora_nosql"],
      "permissions": ["readWriteAnyDatabase", "userAdminAnyDatabase"]
    },
    "sicora_app": {
      "role": "application",
      "databases": ["sicora_nosql"],
      "permissions": ["readWrite"]
    },
    "sicora_backup": {
      "role": "backup",
      "databases": ["sicora_nosql"],
      "permissions": ["backup", "read"]
    },
    "sicora_monitor": {
      "role": "monitoring",
      "databases": ["admin", "sicora_nosql"],
      "permissions": ["clusterMonitor", "read"]
    }
  }
}
```

#### **2. Encriptación y Comunicación Segura**

```yaml
# Security Configuration
security:
  authorization: enabled
  clusterAuthMode: keyFile
  keyFile: /etc/mongodb-keyfile

net:
  tls:
    mode: requireTLS
    certificateKeyFile: /etc/ssl/mongodb.pem
    CAFile: /etc/ssl/ca.pem

encryption:
  encryptionKeyFile: /etc/mongodb-encryption-key
```

#### **3. Network Security**

```bash
# Firewall Configuration (UFW)
sudo ufw allow from 10.0.1.0/24 to any port 27017 comment "MongoDB Replica Set"
sudo ufw deny 27017 comment "MongoDB Default Deny"

# Internal Network Only
bind_ip: 127.0.0.1,10.0.1.10,10.0.1.11,10.0.1.12
```

---

## 💾 **ESTRATEGIA DE BACKUP Y RECUPERACIÓN**

### **Principio 3-2-1 Alineado con PostgreSQL/Redis**

Siguiendo la misma estrategia exitosa de PostgreSQL y Redis:

#### **1. Backup Automático Diario**

```bash
#!/bin/bash
# /opt/sicora/scripts/mongodb-backup.sh

# Variables
BACKUP_DIR="/opt/sicora/backups/mongodb"
DATE=$(date +%Y%m%d_%H%M%S)
RETENTION_DAYS=30

# Backup completo con mongodump
mongodump --host sicora-rs/sicora-mongo-primary:27017,sicora-mongo-secondary-1:27018,sicora-mongo-secondary-2:27019 \
          --db sicora_nosql \
          --username sicora_backup \
          --password $MONGO_BACKUP_PASSWORD \
          --authenticationDatabase admin \
          --out ${BACKUP_DIR}/full_${DATE}

# Comprimir backup
tar -czf ${BACKUP_DIR}/sicora_nosql_${DATE}.tar.gz -C ${BACKUP_DIR} full_${DATE}
rm -rf ${BACKUP_DIR}/full_${DATE}

# Backup incremental con oplog
mongodump --host sicora-rs/sicora-mongo-primary:27017 \
          --db local \
          --collection oplog.rs \
          --query '{"ts": {"$gte": {"$timestamp": {"t": '$(date -d "1 day ago" +%s)', "i": 1}}}}' \
          --username sicora_backup \
          --password $MONGO_BACKUP_PASSWORD \
          --authenticationDatabase admin \
          --out ${BACKUP_DIR}/oplog_${DATE}

# Cleanup old backups
find ${BACKUP_DIR} -name "sicora_nosql_*.tar.gz" -mtime +${RETENTION_DAYS} -delete
find ${BACKUP_DIR} -name "oplog_*" -mtime +7 -exec rm -rf {} \;

# Upload to cloud storage (same as PostgreSQL)
rclone copy ${BACKUP_DIR}/sicora_nosql_${DATE}.tar.gz remote:sicora-backups/mongodb/
```

#### **2. Replicación en Tiempo Real**

```javascript
// Replica Set Configuration
rs.initiate({
  _id: 'sicora-rs',
  members: [
    { _id: 0, host: 'sicora-mongo-primary:27017', priority: 2 },
    { _id: 1, host: 'sicora-mongo-secondary-1:27018', priority: 1 },
    { _id: 2, host: 'sicora-mongo-secondary-2:27019', priority: 1 },
    { _id: 3, host: 'sicora-mongo-arbiter:27017', arbiterOnly: true },
  ],
});

// Read Preference Strategy
db.getMongo().setReadPref('secondaryPreferred');
```

#### **3. Disaster Recovery Procedures**

```bash
#!/bin/bash
# MongoDB Disaster Recovery Script

# 1. Restore from full backup
mongorestore --host sicora-mongo-primary:27017 \
             --db sicora_nosql \
             --username sicora_admin \
             --password $MONGO_ADMIN_PASSWORD \
             --authenticationDatabase admin \
             --drop \
             /opt/sicora/backups/mongodb/restore/sicora_nosql

# 2. Apply oplog for point-in-time recovery
mongorestore --host sicora-mongo-primary:27017 \
             --oplogReplay \
             --oplogFile /opt/sicora/backups/mongodb/restore/oplog.bson \
             --username sicora_admin \
             --password $MONGO_ADMIN_PASSWORD \
             --authenticationDatabase admin

# 3. Verify data integrity
mongo sicora_nosql --eval "
  print('Collections count verification:');
  db.articles.countDocuments();
  db.evaluations.countDocuments();
  db.audit_logs.countDocuments();
  db.notifications.countDocuments();
"
```

---

## 🔄 **FAILOVER Y ALTA DISPONIBILIDAD**

### **Automatic Failover Configuration**

#### **1. Replica Set Health Monitoring**

```javascript
// Health Check Configuration
{
  "replica_set_config": {
    "settings": {
      "heartbeatIntervalMillis": 2000,
      "heartbeatTimeoutSecs": 10,
      "electionTimeoutMillis": 10000,
      "catchUpTimeoutMillis": 60000
    }
  }
}
```

#### **2. Application Connection Resilience**

```go
// Go Driver Configuration
clientOptions := options.Client().
    ApplyURI("mongodb://sicora-mongo-primary:27017,sicora-mongo-secondary-1:27018,sicora-mongo-secondary-2:27019/?replicaSet=sicora-rs").
    SetMaxPoolSize(100).
    SetRetryWrites(true).
    SetRetryReads(true).
    SetReadPreference(readpref.SecondaryPreferred()).
    SetServerSelectionTimeout(5 * time.Second).
    SetSocketTimeout(30 * time.Second)
```

```python
# Python Motor Configuration
client = AsyncIOMotorClient(
    "mongodb://sicora-mongo-primary:27017,sicora-mongo-secondary-1:27018,sicora-mongo-secondary-2:27019",
    replicaSet="sicora-rs",
    retryWrites=True,
    retryReads=True,
    readPreference="secondaryPreferred",
    serverSelectionTimeoutMS=5000,
    socketTimeoutMS=30000,
    maxPoolSize=100
)
```

#### **3. Monitoring y Alertas**

```yaml
# Prometheus MongoDB Exporter
mongodb_exporter:
  image: percona/mongodb_exporter:0.40
  ports:
    - '9216:9216'
  environment:
    MONGODB_URI: 'mongodb://sicora_monitor:password@sicora-mongo-primary:27017,sicora-mongo-secondary-1:27018,sicora-mongo-secondary-2:27019/?replicaSet=sicora-rs'
  command:
    - '--mongodb.uri=${MONGODB_URI}'
    - '--mongodb.direct-connect=false'
    - '--collector.diagnosticdata'
    - '--collector.replicasetstatus'
    - '--collector.dbstats'
    - '--collector.topmetrics'
```

---

## 🔧 **VERSIONAMIENTO Y MIGRACIONES**

### **Estrategia de Schema Evolution**

#### **1. Versionado de Documentos**

```javascript
// Schema Versioning Strategy
{
  "_id": ObjectId("..."),
  "_schema_version": "1.2",
  "_created_at": ISODate("2025-08-03"),
  "_updated_at": ISODate("2025-08-03"),

  // Document data
  "title": "Sample Article",
  "content": {...},

  // Migration metadata
  "_migration_history": [
    {
      "from_version": "1.1",
      "to_version": "1.2",
      "migrated_at": ISODate("2025-08-03"),
      "migration_script": "add_new_fields_v1_2.js"
    }
  ]
}
```

#### **2. Migration Scripts**

```javascript
// /opt/sicora/mongodb/migrations/001_add_schema_versioning.js
db.articles.updateMany(
  { _schema_version: { $exists: false } },
  {
    $set: {
      _schema_version: '1.0',
      _migration_history: [],
    },
  }
);

// Create index for schema version
db.articles.createIndex({ _schema_version: 1 });
```

#### **3. Migration Management**

```bash
#!/bin/bash
# MongoDB Migration Runner

MIGRATION_DIR="/opt/sicora/mongodb/migrations"
DB_NAME="sicora_nosql"

# Get current schema version
CURRENT_VERSION=$(mongo ${DB_NAME} --quiet --eval "
  db.schema_metadata.findOne({type: 'version'}, {version: 1, _id: 0})?.version || '0.0'
")

echo "Current schema version: ${CURRENT_VERSION}"

# Run pending migrations
for migration_file in ${MIGRATION_DIR}/*.js; do
  version=$(basename ${migration_file} | sed 's/.*_v\([0-9.]*\)\.js/\1/')

  if [[ $(echo "${version} > ${CURRENT_VERSION}" | bc) -eq 1 ]]; then
    echo "Running migration: ${migration_file}"
    mongo ${DB_NAME} ${migration_file}

    # Update schema version
    mongo ${DB_NAME} --eval "
      db.schema_metadata.replaceOne(
        {type: 'version'},
        {type: 'version', version: '${version}', updated_at: new Date()},
        {upsert: true}
      )
    "
  fi
done
```

---

## 📊 **MONITOREO Y OBSERVABILIDAD**

### **Integración con Stack de Monitoreo Existente**

#### **1. Métricas de Performance**

```yaml
# Grafana Dashboard Configuration
mongodb_dashboard:
  datasource: prometheus
  panels:
    - title: 'MongoDB Operations/sec'
      query: 'rate(mongodb_op_counters_total[5m])'

    - title: 'Replica Set Status'
      query: 'mongodb_replset_member_state'

    - title: 'Memory Usage'
      query: "mongodb_memory{type='resident'}"

    - title: 'Connection Pool'
      query: "mongodb_connections{state='current'}"

    - title: 'Slow Queries'
      query: "mongodb_mongod_metrics_query_executor_total{stage='slow'}"
```

#### **2. Alertas Críticas**

```yaml
# AlertManager Rules
groups:
  - name: mongodb.rules
    rules:
      - alert: MongoDBDown
        expr: mongodb_up == 0
        for: 5m
        labels:
          severity: critical
        annotations:
          summary: 'MongoDB instance is down'

      - alert: MongoDBReplicaSetMemberDown
        expr: mongodb_replset_member_state != 1 and mongodb_replset_member_state != 2
        for: 5m
        labels:
          severity: warning
        annotations:
          summary: 'MongoDB replica set member is not healthy'

      - alert: MongoDBHighConnections
        expr: mongodb_connections{state="current"} > 80
        for: 10m
        labels:
          severity: warning
        annotations:
          summary: 'MongoDB connection usage is high'
```

#### **3. Application Performance Monitoring**

```go
// Go APM Integration
import (
    "go.mongodb.org/mongo-driver/event"
    "github.com/prometheus/client_golang/prometheus"
)

// MongoDB operation duration histogram
var mongoOpDuration = prometheus.NewHistogramVec(
    prometheus.HistogramOpts{
        Name: "mongodb_operation_duration_seconds",
        Help: "Duration of MongoDB operations",
    },
    []string{"operation", "collection", "database"},
)

// Command monitoring
monitor := &event.CommandMonitor{
    Started: func(ctx context.Context, evt *event.CommandStartedEvent) {
        // Start timing
    },
    Succeeded: func(ctx context.Context, evt *event.CommandSucceededEvent) {
        // Record successful operation
        mongoOpDuration.WithLabelValues(
            evt.CommandName,
            getCollection(evt),
            evt.DatabaseName,
        ).Observe(evt.DurationNanos / 1e9)
    },
}
```

---

## 🚀 **OPTIMIZACIÓN Y PERFORMANCE**

### **Best Practices Implementation**

#### **1. Indexing Strategy**

```javascript
// Production Indexes
use sicora_nosql;

// Articles Collection
db.articles.createIndex(
  { "title": "text", "content.markdown": "text" },
  {
    name: "articles_fulltext",
    background: true,
    textIndexVersion: 3
  }
);

db.articles.createIndex(
  { "slug": 1 },
  {
    unique: true,
    background: true,
    name: "articles_slug_unique"
  }
);

db.articles.createIndex(
  { "metadata.category": 1, "metadata.tags": 1 },
  {
    background: true,
    name: "articles_category_tags"
  }
);

// Audit Logs Collection with TTL
db.audit_logs.createIndex(
  { "timestamp": 1 },
  {
    expireAfterSeconds: 63072000, // 2 years
    background: true,
    name: "audit_logs_ttl"
  }
);

db.audit_logs.createIndex(
  { "service": 1, "action": 1, "timestamp": -1 },
  {
    background: true,
    name: "audit_logs_service_action"
  }
);
```

#### **2. Connection Pool Optimization**

```yaml
# Production MongoDB Configuration
net:
  maxIncomingConnections: 200
  bindIp: 0.0.0.0
  port: 27017

storage:
  wiredTiger:
    engineConfig:
      cacheSizeGB: 4 # 50% of available RAM
      maxCacheOverflowFileSizeGB: 0
    collectionConfig:
      blockCompressor: snappy
    indexConfig:
      prefixCompression: true

operationProfiling:
  mode: slowOp
  slowOpThresholdMs: 100
```

#### **3. Read/Write Optimization**

```javascript
// Collection-specific read preferences
db.articles.find().readPref('secondaryPreferred'); // Heavy reads
db.evaluations.find().readPref('primary'); // Consistency critical
db.audit_logs.insertMany(docs, { writeConcern: { w: 1, j: false } }); // Fast logging
```

---

## 📋 **CHECKLIST DE IMPLEMENTACIÓN**

### **Fase 1: Infraestructura Base** ✅

- [ ] Docker Compose configurado con replica set
- [ ] Usuarios y permisos de seguridad
- [ ] Conectividad desde todos los microservicios
- [ ] Health checks básicos funcionando

### **Fase 2: Backup y Recovery** ✅

- [ ] Scripts de backup automático implementados
- [ ] Estrategia 3-2-1 configurada
- [ ] Procedimientos de disaster recovery documentados
- [ ] Testing de recovery completado

### **Fase 3: Monitoring y Alertas** ✅

- [ ] MongoDB Exporter configurado
- [ ] Dashboards de Grafana creados
- [ ] Alertas críticas configuradas
- [ ] APM integration implementada

### **Fase 4: Optimización** ✅

- [ ] Índices de producción creados
- [ ] Connection pooling optimizado
- [ ] Performance benchmarks establecidos
- [ ] Slow query monitoring activo

### **Fase 5: Automation** ✅

- [ ] CI/CD integration para migraciones
- [ ] Automated testing en pipeline
- [ ] Infrastructure as Code (Terraform/Ansible)
- [ ] Disaster recovery automation

---

## 🔄 **INTEGRACIÓN CON ECOSISTEMA SICORA**

### **Alineación con PostgreSQL y Redis**

| Aspecto         | PostgreSQL     | Redis          | MongoDB                 |
| --------------- | -------------- | -------------- | ----------------------- |
| **Backup**      | pg_dump diario | RDB + AOF      | mongodump + oplog       |
| **Replication** | Master-Slave   | Cluster 3M+3S  | Replica Set 1P+2S+1A    |
| **Monitoring**  | pg_exporter    | redis_exporter | mongodb_exporter        |
| **Security**    | TLS + Users    | AUTH + TLS     | SCRAM + TLS             |
| **Failover**    | Manual         | Automatic      | Automatic               |
| **Retention**   | 7 años         | 30 días        | Variable por collection |

### **Unified Operations**

```bash
# Unified backup script for all databases
/opt/sicora/scripts/backup-all-databases.sh
├── postgresql-backup.sh
├── redis-backup.sh
└── mongodb-backup.sh

# Unified monitoring
/opt/sicora/monitoring/
├── prometheus.yml (all exporters)
├── grafana/dashboards/
│   ├── postgresql.json
│   ├── redis.json
│   └── mongodb.json
└── alertmanager/rules/
    ├── postgresql.yml
    ├── redis.yml
    └── mongodb.yml
```

---

## 📈 **ROADMAP DE IMPLEMENTACIÓN**

### **Semana 1-2: Fundaciones**

- Setup de replica set MongoDB
- Configuración de seguridad básica
- Testing de conectividad

### **Semana 3-4: Operaciones**

- Implementación de backup automático
- Configuración de monitoring
- Documentación de procedures

### **Semana 5-6: Optimización**

- Performance tuning
- Index optimization
- Load testing

### **Semana 7-8: Integración**

- CI/CD integration
- Automation scripts
- Training documentation

---

**Nota:** Esta especificación de infraestructura MongoDB está diseñada para complementar perfectamente la arquitectura existente de PostgreSQL y Redis en SICORA, manteniendo los mismos estándares de calidad, seguridad y operabilidad.
