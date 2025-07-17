# 📊 SICORA Services Monitoring Dashboard

> **Real-time status of all SICORA backend services**

## 🚀 Quick Commands

```bash
# Start all services monitoring
./scripts/endpoint-automation.sh monitor

# Check all health endpoints
./scripts/endpoint-automation.sh health-check

# Generate full report
./scripts/endpoint-automation.sh report

# Test specific service
./scripts/endpoint-automation.sh test-service userservice go
```

## 📈 Service Metrics

### Go Services (Port 8000-8099)
- **UserService**: :8001 - Authentication & User Management
- **AttendanceService**: :8002 - Attendance Tracking
- **ScheduleService**: :8003 - Schedule Management  
- **EvalInService**: :8004 - Instructor Evaluations
- **KbService**: :8005 - Knowledge Base
- **SoftwareFactoryService**: :8006 - Software Factory
- **MevalService**: :8007 - Meta Evaluations
- **ProjectEvalService**: :8008 - Project Evaluations

### Python Services (Port 9000-9099)
- **API Gateway**: :9000 - Central Gateway
- **UserService**: :9001 - User Management (Python)
- **ScheduleService**: :9002 - Schedule Management (Python)
- **EvalInService**: :9003 - Evaluations (Python)
- **AttendanceService**: :9004 - Attendance (Python)
- **KbService**: :9005 - Knowledge Base (Python)
- **ProjectEvalService**: :9006 - Project Evals (Python)

## 🔧 Health Check Endpoints

All services should respond to:
- `GET /health` - Basic health check
- `GET /ready` - Readiness probe (when available)
- `GET /metrics` - Prometheus metrics (when available)

## 📊 Expected Response Times

- **Health checks**: < 100ms
- **Simple queries**: < 500ms
- **Complex operations**: < 2s
- **Bulk operations**: < 10s

## 🚨 Alert Thresholds

- **Response time > 5s**: Warning
- **Response time > 10s**: Critical
- **Health check failure**: Critical
- **Service unavailable**: Critical

---
*Updated automatically by endpoint monitoring system*
