#!/bin/bash

# AutoCommit Service Activator for ProjectEvalService
# Sets up automatic commit monitoring and execution

set -e

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

# Configuration
WATCH_INTERVAL=30  # seconds
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
AUTOCOMMIT_SCRIPT="$SCRIPT_DIR/autocommit.sh"
PID_FILE="$SCRIPT_DIR/.autocommit.pid"

# Functions
start_autocommit() {
    if [ -f "$PID_FILE" ] && kill -0 $(cat "$PID_FILE") 2>/dev/null; then
        echo -e "${YELLOW}⚠️  AutoCommit service is already running (PID: $(cat $PID_FILE))${NC}"
        return 1
    fi

    echo -e "${BLUE}🚀 Starting AutoCommit service...${NC}"
    echo -e "${BLUE}📁 Monitoring: $(pwd)${NC}"
    echo -e "${BLUE}⏱️  Check interval: ${WATCH_INTERVAL}s${NC}"

    # Make autocommit script executable
    chmod +x "$AUTOCOMMIT_SCRIPT"

    # Start monitoring in background
    {
        while true; do
            # Check if there are changes
            if ! git diff --quiet || ! git diff --staged --quiet; then
                echo -e "${YELLOW}🔄 Changes detected, running autocommit...${NC}"
                if bash "$AUTOCOMMIT_SCRIPT"; then
                    echo -e "${GREEN}✅ AutoCommit successful${NC}"
                else
                    echo -e "${RED}❌ AutoCommit failed${NC}"
                fi
            fi
            sleep $WATCH_INTERVAL
        done
    } &

    # Save PID
    echo $! > "$PID_FILE"
    echo -e "${GREEN}✅ AutoCommit service started (PID: $!)${NC}"
    echo -e "${BLUE}💡 Use 'bash scripts/activate-autocommit.sh stop' to stop${NC}"
}

stop_autocommit() {
    if [ ! -f "$PID_FILE" ]; then
        echo -e "${YELLOW}⚠️  AutoCommit service is not running${NC}"
        return 1
    fi

    PID=$(cat "$PID_FILE")
    if kill -0 "$PID" 2>/dev/null; then
        kill "$PID"
        rm -f "$PID_FILE"
        echo -e "${GREEN}✅ AutoCommit service stopped (PID: $PID)${NC}"
    else
        rm -f "$PID_FILE"
        echo -e "${YELLOW}⚠️  AutoCommit service was not running${NC}"
    fi
}

status_autocommit() {
    if [ -f "$PID_FILE" ] && kill -0 $(cat "$PID_FILE") 2>/dev/null; then
        echo -e "${GREEN}✅ AutoCommit service is running (PID: $(cat $PID_FILE))${NC}"
        echo -e "${BLUE}📁 Monitoring: $(pwd)${NC}"
        echo -e "${BLUE}⏱️  Check interval: ${WATCH_INTERVAL}s${NC}"
    else
        echo -e "${RED}❌ AutoCommit service is not running${NC}"
        [ -f "$PID_FILE" ] && rm -f "$PID_FILE"
    fi
}

manual_commit() {
    echo -e "${BLUE}🔧 Running manual commit...${NC}"
    bash "$AUTOCOMMIT_SCRIPT"
}

show_help() {
    echo -e "${BLUE}AutoCommit Service for ProjectEvalService${NC}"
    echo ""
    echo "Usage: bash scripts/activate-autocommit.sh [COMMAND]"
    echo ""
    echo "Commands:"
    echo "  start     Start the autocommit service"
    echo "  stop      Stop the autocommit service"
    echo "  status    Show service status"
    echo "  restart   Restart the autocommit service"
    echo "  commit    Run manual commit"
    echo "  help      Show this help message"
    echo ""
    echo "Examples:"
    echo "  bash scripts/activate-autocommit.sh start"
    echo "  bash scripts/activate-autocommit.sh status"
    echo "  bash scripts/activate-autocommit.sh commit"
}

# Check if we're in the right directory
if [ ! -f "go.mod" ] || ! grep -q "projectevalservice" go.mod; then
    echo -e "${RED}❌ Error: Not in projectevalservice directory${NC}"
    echo -e "${YELLOW}💡 Run this script from: 02-go/projectevalservice/${NC}"
    exit 1
fi

# Handle commands
case "${1:-start}" in
    "start")
        start_autocommit
        ;;
    "stop")
        stop_autocommit
        ;;
    "status")
        status_autocommit
        ;;
    "restart")
        stop_autocommit
        sleep 2
        start_autocommit
        ;;
    "commit")
        manual_commit
        ;;
    "help"|"-h"|"--help")
        show_help
        ;;
    *)
        echo -e "${RED}❌ Unknown command: $1${NC}"
        show_help
        exit 1
        ;;
esac
