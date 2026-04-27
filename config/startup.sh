#!/bin/bash

set -euo pipefail

# Configuration
TIMEZONE="${TZ:-America/Phoenix}"
APP_PORT="${PORT:-8080}"
APP_HOME="/weatherBridge"
FLASK_APP="${FLASK_APP:-get_handler.py}"
LOG_DIR="/var/log/weatherbridge"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Logging functions
log_info() {
    echo -e "${GREEN}[$(date +'%Y-%m-%d %H:%M:%S')]${NC} INFO: $*"
}

log_warn() {
    echo -e "${YELLOW}[$(date +'%Y-%m-%d %H:%M:%S')]${NC} WARN: $*"
}

log_error() {
    echo -e "${RED}[$(date +'%Y-%m-%d %H:%M:%S')]${NC} ERROR: $*" >&2
}

# Error handler
trap 'log_error "Script failed at line $LINENO"; exit 1' ERR

# Check prerequisites
check_prerequisites() {
    log_info "Checking prerequisites..."

    if ! command -v python3 &> /dev/null; then
        log_error "Python3 is not installed"
        exit 1
    fi

    log_info "Python version: $(python3 --version)"
}

# Set timezone
set_timezone() {
    log_info "Setting timezone to $TIMEZONE..."

    if [ ! -f "/usr/share/zoneinfo/$TIMEZONE" ]; then
        log_warn "Timezone file not found: /usr/share/zoneinfo/$TIMEZONE"
        log_warn "Using default timezone"
        return 0
    fi

    # Remove existing symlink if it exists and is a symlink
    if [ -L "/etc/localtime" ]; then
        rm -f /etc/localtime
    elif [ -f "/etc/localtime" ]; then
        log_warn "/etc/localtime exists but is not a symlink, skipping"
        return 0
    fi

    ln -s "/usr/share/zoneinfo/$TIMEZONE" /etc/localtime || {
        log_warn "Failed to set timezone, continuing anyway"
        return 0
    }

    log_info "Timezone set successfully"
}

# Setup environment
setup_environment() {
    log_info "Setting up environment variables..."

    # Create log directory if it doesn't exist
    if [ ! -d "$LOG_DIR" ]; then
        mkdir -p "$LOG_DIR" || log_warn "Failed to create log directory"
    fi

    # Export environment variables
    export TZ="$TIMEZONE"
    export FLASK_APP="$FLASK_APP"
    export PYTHONPATH="${PYTHONPATH:-$APP_HOME}"
    export FLASK_ENV="${FLASK_ENV:-production}"

    # Save environment variables
    env > /etc/environment || log_warn "Failed to save environment variables"

    log_info "Environment setup complete"
}

# Health check (optional)
health_check() {
    log_info "Flask health check endpoint would be: http://localhost:$APP_PORT/weather"
}

# Main execution
main() {
    log_info "================================"
    log_info "WeatherBridge Startup Script"
    log_info "================================"

    check_prerequisites
    set_timezone
    setup_environment
    health_check

    log_info "Starting Flask application..."
    log_info "App: $FLASK_APP"
    log_info "Port: $APP_PORT"
    log_info "Log directory: $LOG_DIR"

    # Start Flask with proper signal handling
    cd "$APP_HOME"
    exec python3 -m flask run --host=0.0.0.0 --port="$APP_PORT" --no-reload
}

main "$@"
