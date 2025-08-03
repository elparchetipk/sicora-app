#!/bin/bash
# MongoDB Health Check Script for SICORA OneVision

echo "🔍 Checking MongoDB health..."

# Test MongoDB connection
mongo_result=$(mongo --host localhost:27017 --eval "db.runCommand('ping').ok" --quiet 2>/dev/null)

if [ "$mongo_result" = "1" ]; then
    echo "✅ MongoDB is running and responding"

    # Check databases
    echo "📊 Checking SICORA databases..."

    databases=$(mongo --host localhost:27017 --eval "db.adminCommand('listDatabases').databases.forEach(function(db) { print(db.name) })" --quiet 2>/dev/null)

    if echo "$databases" | grep -q "sicora_mongodb"; then
        echo "✅ sicora_mongodb database found"
    else
        echo "❌ sicora_mongodb database missing"
    fi

    if echo "$databases" | grep -q "sicora_ai"; then
        echo "✅ sicora_ai database found"
    else
        echo "❌ sicora_ai database missing"
    fi

    if echo "$databases" | grep -q "sicora_kb"; then
        echo "✅ sicora_kb database found"
    else
        echo "❌ sicora_kb database missing"
    fi

    if echo "$databases" | grep -q "sicora_logs"; then
        echo "✅ sicora_logs database found"
    else
        echo "❌ sicora_logs database missing"
    fi

    # Check user authentication
    auth_result=$(mongo --host localhost:27017 -u sicora_mongodb_user -p sicora_mongodb_2024 --authenticationDatabase admin --eval "db.runCommand('ping').ok" --quiet 2>/dev/null)

    if [ "$auth_result" = "1" ]; then
        echo "✅ User authentication working"
    else
        echo "❌ User authentication failed"
    fi

    echo "🎉 MongoDB health check completed"
    exit 0
else
    echo "❌ MongoDB is not responding"
    exit 1
fi
