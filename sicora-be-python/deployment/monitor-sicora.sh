#!/bin/bash
# Script de monitoreo para SICORA Backend

echo "=== SICORA Backend Status Report ==="
echo "Fecha: $(date)"
echo "Hostname: $(hostname)"
echo ""

echo "=== Docker Containers ==="
docker ps --format "table {{.Names}}\t{{.Status}}\t{{.Ports}}"
echo ""

echo "=== Health Checks ==="
API_HEALTH=$(curl -s http://localhost:8000/health 2>/dev/null || echo "FAILED")
NOTIFICATION_HEALTH=$(curl -s http://localhost:8001/health 2>/dev/null || echo "FAILED")

if [[ "$API_HEALTH" == *"ok"* ]]; then
    echo "✅ API Gateway: OK"
else
    echo "❌ API Gateway: FAILED"
fi

if [[ "$NOTIFICATION_HEALTH" == *"ok"* ]]; then
    echo "✅ Notification Service: OK"
else
    echo "❌ Notification Service: FAILED"
fi

echo ""
echo "=== System Resources ==="
echo "Memoria:"
free -h
echo ""
echo "Disco:"
df -h / /var
echo ""
echo "CPU Load:"
uptime

echo ""
echo "=== Recent Docker Logs (Last 5 lines) ==="
echo "--- API Gateway ---"
docker logs --tail 5 sicora-backend_apigateway_1 2>/dev/null || echo "Container not found"
echo ""
echo "--- Notification Service ---"
docker logs --tail 5 sicora-backend_notification_1 2>/dev/null || echo "Container not found"
echo ""
echo "--- PostgreSQL ---"
docker logs --tail 5 sicora-backend_postgres_1 2>/dev/null || echo "Container not found"

echo ""
echo "=== Network Status ==="
echo "Nginx Status: $(systemctl is-active nginx 2>/dev/null || echo 'not-running')"
echo "Listening Ports:"
netstat -tlnp 2>/dev/null | grep -E ':(80|443|8000|8001|5432|6379)' || ss -tlnp | grep -E ':(80|443|8000|8001|5432|6379)'
