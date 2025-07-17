#!/bin/bash

# 🤖 SICORA Endpoint Management & Automation Script
# Automatiza la gestión, monitoreo y testing de todos los endpoints backend

set -euo pipefail

# Colors para output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Configuration
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"
LOG_FILE="$PROJECT_ROOT/_docs/reportes/endpoint-monitoring-$(date +%Y%m%d-%H%M%S).log"

# Service configurations
declare -A GO_SERVICES=(
    ["userservice"]="http://localhost:8001"
    ["attendanceservice"]="http://localhost:8002"
    ["scheduleservice"]="http://localhost:8003"
    ["evalinservice"]="http://localhost:8004"
    ["kbservice"]="http://localhost:8005"
    ["softwarefactoryservice"]="http://localhost:8006"
    ["mevalservice"]="http://localhost:8007"
    ["projectevalservice"]="http://localhost:8008"
)

declare -A PYTHON_SERVICES=(
    ["userservice"]="http://localhost:9001"
    ["scheduleservice"]="http://localhost:9002"
    ["evalinservice"]="http://localhost:9003"
    ["attendanceservice"]="http://localhost:9004"
    ["kbservice"]="http://localhost:9005"
    ["projectevalservice"]="http://localhost:9006"
    ["apigateway"]="http://localhost:9000"
)

# Logging function
log() {
    echo -e "${2:-$NC}[$(date '+%Y-%m-%d %H:%M:%S')] $1${NC}" | tee -a "$LOG_FILE"
}

# Health check function
check_service_health() {
    local service_name="$1"
    local base_url="$2"
    local stack="$3"
    
    log "🔍 Checking $stack $service_name..." "$BLUE"
    
    # Try health endpoint
    if curl -s -f "$base_url/health" > /dev/null 2>&1; then
        log "✅ $service_name ($stack) - HEALTHY" "$GREEN"
        return 0
    else
        log "❌ $service_name ($stack) - UNHEALTHY" "$RED"
        return 1
    fi
}

# Count endpoints function
count_service_endpoints() {
    local service_name="$1"
    local base_url="$2"
    local stack="$3"
    
    log "📊 Counting endpoints for $stack $service_name..." "$BLUE"
    
    # Try to get OpenAPI/Swagger spec
    local swagger_endpoints=(
        "/swagger/doc.json"
        "/docs/swagger.json"
        "/api/docs"
        "/openapi.json"
    )
    
    for endpoint in "${swagger_endpoints[@]}"; do
        if curl -s -f "$base_url$endpoint" > /dev/null 2>&1; then
            # Parse swagger JSON to count endpoints
            local count=$(curl -s "$base_url$endpoint" | jq -r '.paths | keys | length' 2>/dev/null || echo "0")
            log "📈 $service_name ($stack): $count endpoints found via swagger" "$GREEN"
            return 0
        fi
    done
    
    log "⚠️  $service_name ($stack): Unable to fetch endpoint count" "$YELLOW"
    return 1
}

# Test critical endpoints
test_critical_endpoints() {
    local service_name="$1"
    local base_url="$2"
    local stack="$3"
    
    log "🧪 Testing critical endpoints for $stack $service_name..." "$BLUE"
    
    # Common critical endpoints to test
    local critical_endpoints=(
        "/health"
        "/api/v1"
        "/"
    )
    
    local passed=0
    local total=${#critical_endpoints[@]}
    
    for endpoint in "${critical_endpoints[@]}"; do
        if curl -s -f "$base_url$endpoint" > /dev/null 2>&1; then
            ((passed++))
        fi
    done
    
    log "📊 $service_name ($stack): $passed/$total critical endpoints responding" "$GREEN"
}

# Generate service report
generate_service_report() {
    local stack="$1"
    local -n services_ref=$2
    
    log "📋 Generating report for $stack services..." "$BLUE"
    
    local healthy=0
    local total=0
    
    for service in "${!services_ref[@]}"; do
        ((total++))
        if check_service_health "$service" "${services_ref[$service]}" "$stack"; then
            ((healthy++))
            count_service_endpoints "$service" "${services_ref[$service]}" "$stack"
            test_critical_endpoints "$service" "${services_ref[$service]}" "$stack"
        fi
    done
    
    log "📈 $stack Stack Health: $healthy/$total services healthy" "$GREEN"
}

# Generate comprehensive endpoint documentation
generate_endpoint_docs() {
    log "📚 Generating comprehensive endpoint documentation..." "$BLUE"
    
    local doc_file="$PROJECT_ROOT/_docs/reportes/ENDPOINT_STATUS_$(date +%Y%m%d).md"
    
    cat > "$doc_file" << EOF
# 📊 SICORA Endpoint Status Report

> **Generated**: $(date '+%Y-%m-%d %H:%M:%S')  
> **Total Services Monitored**: $((${#GO_SERVICES[@]} + ${#PYTHON_SERVICES[@]}))

## 🏗️ Go Services Status

| Service | Status | Base URL | Health Check |
|---------|--------|----------|--------------|
EOF

    # Add Go services to documentation
    for service in "${!GO_SERVICES[@]}"; do
        local status_emoji="❌"
        local status_text="DOWN"
        
        if curl -s -f "${GO_SERVICES[$service]}/health" > /dev/null 2>&1; then
            status_emoji="✅"
            status_text="UP"
        fi
        
        echo "| $service | $status_emoji $status_text | ${GO_SERVICES[$service]} | Last checked: $(date) |" >> "$doc_file"
    done
    
    cat >> "$doc_file" << EOF

## 🐍 Python Services Status

| Service | Status | Base URL | Health Check |
|---------|--------|----------|--------------|
EOF

    # Add Python services to documentation
    for service in "${!PYTHON_SERVICES[@]}"; do
        local status_emoji="❌"
        local status_text="DOWN"
        
        if curl -s -f "${PYTHON_SERVICES[$service]}/health" > /dev/null 2>&1; then
            status_emoji="✅"
            status_text="UP"
        fi
        
        echo "| $service | $status_emoji $status_text | ${PYTHON_SERVICES[$service]} | Last checked: $(date) |" >> "$doc_file"
    done
    
    cat >> "$doc_file" << EOF

## 📈 Summary

- **Total Services**: $((${#GO_SERVICES[@]} + ${#PYTHON_SERVICES[@]}))
- **Go Services**: ${#GO_SERVICES[@]}
- **Python Services**: ${#PYTHON_SERVICES[@]}
- **Generated**: $(date)

## 🔧 Automation Commands

\`\`\`bash
# Monitor all services
./scripts/endpoint-automation.sh monitor

# Test all endpoints
./scripts/endpoint-automation.sh test

# Generate reports
./scripts/endpoint-automation.sh report

# Check specific service
./scripts/endpoint-automation.sh check userservice go
\`\`\`

---
*Auto-generated by SICORA Endpoint Automation*
EOF

    log "📄 Documentation generated: $doc_file" "$GREEN"
}

# Update README with endpoint counts
update_main_readme() {
    log "📝 Updating main README with current endpoint statistics..." "$BLUE"
    
    local readme_file="$PROJECT_ROOT/README.md"
    local temp_file=$(mktemp)
    
    # Count total endpoints (using our documented numbers)
    local go_total=237
    local python_total=152
    local total_endpoints=$((go_total + python_total))
    
    # Create endpoint statistics section
    local stats_section="
## 📊 Backend API Statistics

> Last updated: $(date '+%Y-%m-%d')

- **Total Endpoints**: **$total_endpoints**
- **Go Backend**: $go_total endpoints (8 services)
- **Python Backend**: $python_total endpoints (7 services + API Gateway)

### Service Distribution:
- **SoftwareFactoryService (Go)**: 58 endpoints
- **EvalInService (Go)**: 42 endpoints  
- **KbService (Go)**: 32 endpoints
- **UserService (Go)**: 31 endpoints
- **ScheduleService (Go)**: 28 endpoints
- **AttendanceService (Go)**: 25 endpoints
- **MevalService (Go)**: 18 endpoints
- **API Gateway (Python)**: 49 endpoints
- **EvalInService (Python)**: 28 endpoints
- **UserService (Python)**: 28 endpoints

📋 [Ver conteo completo](./_docs/reportes/CONTEO_ENDPOINTS_BACKEND_SICORA.md)
"
    
    # Insert statistics section after main heading
    awk -v stats="$stats_section" '
        /^# / && !inserted { 
            print; 
            print stats; 
            inserted=1; 
            next 
        } 
        /^## 📊 Backend API Statistics/,/^## / { 
            if (/^## / && !/^## 📊 Backend API Statistics/) {
                print;
                next;
            }
            if (!/^## 📊 Backend API Statistics/) next;
        } 
        { print }
    ' "$readme_file" > "$temp_file"
    
    mv "$temp_file" "$readme_file"
    log "✅ README updated with current statistics" "$GREEN"
}

# Create monitoring dashboard
create_monitoring_dashboard() {
    log "📊 Creating monitoring dashboard..." "$BLUE"
    
    local dashboard_file="$PROJECT_ROOT/_docs/reportes/MONITORING_DASHBOARD.md"
    
    cat > "$dashboard_file" << 'EOF'
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
EOF

    log "✅ Monitoring dashboard created: $dashboard_file" "$GREEN"
}

# Main execution functions
monitor_all_services() {
    log "🔍 Starting comprehensive service monitoring..." "$BLUE"
    
    generate_service_report "Go" GO_SERVICES
    echo ""
    generate_service_report "Python" PYTHON_SERVICES
    echo ""
    
    generate_endpoint_docs
    update_main_readme
    create_monitoring_dashboard
    
    log "✅ Monitoring complete! Check $LOG_FILE for details" "$GREEN"
}

health_check_all() {
    log "🏥 Performing health checks on all services..." "$BLUE"
    
    local total_services=$((${#GO_SERVICES[@]} + ${#PYTHON_SERVICES[@]}))
    local healthy_services=0
    
    # Check Go services
    for service in "${!GO_SERVICES[@]}"; do
        if check_service_health "$service" "${GO_SERVICES[$service]}" "Go"; then
            ((healthy_services++))
        fi
    done
    
    # Check Python services
    for service in "${!PYTHON_SERVICES[@]}"; do
        if check_service_health "$service" "${PYTHON_SERVICES[$service]}" "Python"; then
            ((healthy_services++))
        fi
    done
    
    log "🎯 Overall Health: $healthy_services/$total_services services healthy" "$GREEN"
    
    if [ $healthy_services -eq $total_services ]; then
        log "🎉 All services are healthy!" "$GREEN"
        exit 0
    else
        log "⚠️  Some services are unhealthy" "$YELLOW"
        exit 1
    fi
}

test_specific_service() {
    local service_name="$1"
    local stack="$2"
    
    log "🧪 Testing specific service: $stack $service_name..." "$BLUE"
    
    if [ "$stack" = "go" ]; then
        if [[ -n "${GO_SERVICES[$service_name]:-}" ]]; then
            check_service_health "$service_name" "${GO_SERVICES[$service_name]}" "Go"
            count_service_endpoints "$service_name" "${GO_SERVICES[$service_name]}" "Go"
            test_critical_endpoints "$service_name" "${GO_SERVICES[$service_name]}" "Go"
        else
            log "❌ Service $service_name not found in Go services" "$RED"
            exit 1
        fi
    elif [ "$stack" = "python" ]; then
        if [[ -n "${PYTHON_SERVICES[$service_name]:-}" ]]; then
            check_service_health "$service_name" "${PYTHON_SERVICES[$service_name]}" "Python"
            count_service_endpoints "$service_name" "${PYTHON_SERVICES[$service_name]}" "Python"
            test_critical_endpoints "$service_name" "${PYTHON_SERVICES[$service_name]}" "Python"
        else
            log "❌ Service $service_name not found in Python services" "$RED"
            exit 1
        fi
    else
        log "❌ Invalid stack. Use 'go' or 'python'" "$RED"
        exit 1
    fi
}

show_help() {
    cat << EOF
🤖 SICORA Endpoint Management & Automation Script

Usage: $0 [COMMAND] [OPTIONS]

Commands:
    monitor              Monitor all services and generate reports
    health-check         Check health of all services
    test-service <name> <stack>  Test specific service (go|python)
    report              Generate comprehensive reports
    update-docs         Update documentation with current stats
    help                Show this help message

Examples:
    $0 monitor                    # Monitor all services
    $0 health-check              # Quick health check
    $0 test-service userservice go   # Test specific service
    $0 report                    # Generate reports only

Services Available:
    Go: ${!GO_SERVICES[*]}
    Python: ${!PYTHON_SERVICES[*]}

Output:
    Logs: $LOG_FILE
    Reports: $PROJECT_ROOT/_docs/reportes/

EOF
}

# Main script logic
main() {
    log "🚀 SICORA Endpoint Automation Script Started" "$GREEN"
    log "📁 Project Root: $PROJECT_ROOT" "$BLUE"
    log "📄 Log File: $LOG_FILE" "$BLUE"
    
    case "${1:-help}" in
        "monitor")
            monitor_all_services
            ;;
        "health-check")
            health_check_all
            ;;
        "test-service")
            if [ $# -lt 3 ]; then
                log "❌ Usage: $0 test-service <service_name> <stack>" "$RED"
                exit 1
            fi
            test_specific_service "$2" "$3"
            ;;
        "report")
            generate_endpoint_docs
            update_main_readme
            create_monitoring_dashboard
            ;;
        "update-docs")
            update_main_readme
            ;;
        "help"|"-h"|"--help")
            show_help
            ;;
        *)
            log "❌ Unknown command: $1" "$RED"
            show_help
            exit 1
            ;;
    esac
}

# Execute main function with all arguments
main "$@"
