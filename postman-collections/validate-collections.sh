#!/bin/bash

# Validar que todas las collections se importaron correctamente
echo "🔍 Validando collections..."

COLLECTIONS_DIR="collections"
EXPECTED_COLLECTIONS=(
    "UserService_Go.postman_collection.json"
    "UserService_Python.postman_collection.json"
    "AttendanceService_Go.postman_collection.json"
    "ScheduleService_Go.postman_collection.json"
    "ProjectEvalService_Go.postman_collection.json"
    "APIGateway_Python.postman_collection.json"
    "AIService_Python.postman_collection.json"
    "NotificationService_Python.postman_collection.json"
)

echo "📋 Checklist de Collections:"
for collection in "${EXPECTED_COLLECTIONS[@]}"; do
    if [[ -f "$COLLECTIONS_DIR/$collection" ]]; then
        echo "✅ $collection"
    else
        echo "❌ $collection - FALTANTE"
    fi
done

echo -e "\n🌍 Checklist de Environments:"
ENVIRONMENTS_DIR="environments"
EXPECTED_ENVIRONMENTS=(
    "sicora-development.postman_environment.json"
    "sicora-staging.postman_environment.json"
    "sicora-production.postman_environment.json"
)

for env in "${EXPECTED_ENVIRONMENTS[@]}"; do
    if [[ -f "$ENVIRONMENTS_DIR/$env" ]]; then
        echo "✅ $env"
    else
        echo "❌ $env - FALTANTE"
    fi
done

echo -e "\n📊 Estadísticas:"
echo "Collections: $(ls -1 $COLLECTIONS_DIR/*.json 2>/dev/null | wc -l)"
echo "Environments: $(ls -1 $ENVIRONMENTS_DIR/*.json 2>/dev/null | wc -l)"
echo "Documentation: $(ls -1 documentation/*.md 2>/dev/null | wc -l)"

echo -e "\n🎯 Siguiente paso: Importar en Postman"
