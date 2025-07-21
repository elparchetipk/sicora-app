#!/bin/bash
# Script para monitorear el autocommit automático de SICORA

echo "🔍 SICORA Autocommit Status Monitor"
echo "====================================="
echo ""

# Verificar que cron esté ejecutándose
echo "📋 Cron Service Status:"
if systemctl is-active crond >/dev/null 2>&1 || systemctl is-active cron >/dev/null 2>&1; then
    echo "✅ Cron service is running"
else
    echo "❌ Cron service is NOT running"
fi
echo ""

# Mostrar el crontab configurado para autocommit
echo "⏰ Crontab Configuration:"
crontab -l | grep -A1 -B1 "autocommit" || echo "❌ No autocommit job found"
echo ""

# Verificar el log de autocommit
echo "📝 Recent Autocommit Activity:"
if [ -f "/tmp/sicora-autocommit.log" ]; then
    echo "Last 10 lines from autocommit log:"
    tail -10 /tmp/sicora-autocommit.log
else
    echo "⚠️  No autocommit log found yet (may not have run)"
fi
echo ""

# Verificar commits recientes
echo "📊 Recent Commits (last 5):"
cd /home/epti/Documentos/epti-dev/sicora-app
git log --oneline -5 || echo "❌ Could not access git repository"
echo ""

# Verificar si hay cambios pendientes
echo "🔄 Current Git Status:"
git status --porcelain | head -5 || echo "❌ Could not check git status"
if [ -z "$(git status --porcelain)" ]; then
    echo "✅ No pending changes"
else
    echo "⚠️  There are pending changes (will be committed in next cycle)"
fi
echo ""

# Calcular próxima ejecución
current_minute=$(date +%M)
next_minute=$(( (current_minute / 5 + 1) * 5 ))
if [ $next_minute -ge 60 ]; then
    next_minute=0
    next_hour=$(( $(date +%H) + 1 ))
    if [ $next_hour -ge 24 ]; then
        next_hour=0
    fi
else
    next_hour=$(date +%H)
fi

echo "⏳ Next autocommit scheduled: $(printf "%02d:%02d" $next_hour $next_minute)"
echo ""
echo "💡 Tips:"
echo "   - View live log: tail -f /tmp/sicora-autocommit.log"
echo "   - Disable autocommit: crontab -e (comment out the line)"
echo "   - Manual run: cd /home/epti/Documentos/epti-dev/sicora-app && bash scripts/universal-autocommit.sh"
