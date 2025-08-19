#!/bin/bash

# Kill Flask Application Script
# Reads port from config.yaml and kills any process running on that port

set -e  # Exit on any error

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Function to print colored output
print_status() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

print_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Function to get port from config.yaml
get_port_from_config() {
    local config_file="config.yaml"
    
    if [ ! -f "$config_file" ]; then
        print_error "Config file $config_file not found!"
        return 1
    fi
    
    # Extract port using python -c with yaml parsing
    if command -v python3 &> /dev/null; then
        python3 -c "
import yaml
import sys
try:
    with open('$config_file', 'r') as f:
        config = yaml.safe_load(f)
    port = config.get('app', {}).get('port', 5000)
    print(port)
except Exception as e:
    print('5000', file=sys.stderr)  # Default fallback
    sys.exit(1)
" 2>/dev/null || echo "5000"
    else
        # Fallback: use grep/sed if python is not available
        grep -E "^\s*port:\s*[0-9]+" "$config_file" 2>/dev/null | sed 's/.*port:\s*//' | tr -d ' ' || echo "5000"
    fi
}

# Function to find process using a port
find_process_on_port() {
    local port=$1
    
    # Try different methods to find the process
    if command -v lsof &> /dev/null; then
        lsof -ti:$port 2>/dev/null
    elif command -v netstat &> /dev/null; then
        netstat -tlnp 2>/dev/null | grep ":$port " | awk '{print $7}' | cut -d'/' -f1 | grep -v '-'
    elif command -v ss &> /dev/null; then
        ss -tlnp 2>/dev/null | grep ":$port " | sed 's/.*pid=\([0-9]*\).*/\1/' | head -1
    else
        print_error "No suitable tool found to check port usage (lsof, netstat, or ss required)"
        return 1
    fi
}

# Function to get process info
get_process_info() {
    local pid=$1
    
    if [ -n "$pid" ] && kill -0 "$pid" 2>/dev/null; then
        if command -v ps &> /dev/null; then
            ps -p "$pid" -o pid,ppid,cmd --no-headers 2>/dev/null
        fi
    fi
}

# Function to kill process gracefully
kill_process() {
    local pid=$1
    local port=$2
    
    if [ -z "$pid" ]; then
        return 0
    fi
    
    print_status "Attempting to kill process $pid on port $port..."
    
    # Try graceful termination first (SIGTERM)
    if kill -TERM "$pid" 2>/dev/null; then
        print_status "Sent SIGTERM to process $pid"
        
        # Wait for process to terminate gracefully
        local count=0
        while kill -0 "$pid" 2>/dev/null && [ $count -lt 10 ]; do
            sleep 1
            count=$((count + 1))
        done
        
        # Check if process is still running
        if kill -0 "$pid" 2>/dev/null; then
            print_warning "Process $pid didn't terminate gracefully, using SIGKILL..."
            kill -KILL "$pid" 2>/dev/null || true
            sleep 1
        fi
        
        # Final check
        if kill -0 "$pid" 2>/dev/null; then
            print_error "Failed to kill process $pid"
            return 1
        else
            print_success "Process $pid terminated successfully"
            return 0
        fi
    else
        print_error "Failed to send signal to process $pid"
        return 1
    fi
}

# Main execution
main() {
    echo "🔪 Flask Application Killer"
    echo "=========================="
    
    # Get port from config
    print_status "Reading port from config.yaml..."
    PORT=$(get_port_from_config)
    
    if [ -z "$PORT" ] || [ "$PORT" = "0" ]; then
        print_error "Could not determine port from config file"
        exit 1
    fi
    
    print_success "Found port: $PORT"
    
    # Find processes using the port
    print_status "Checking for processes on port $PORT..."
    PIDS=$(find_process_on_port $PORT)
    
    if [ -z "$PIDS" ] || [ "$PIDS" = "" ]; then
        print_success "No processes found running on port $PORT"
        exit 0
    fi
    
    # Filter out empty lines and invalid PIDs
    PIDS=$(echo "$PIDS" | grep -E '^[0-9]+$' | sort -u)
    
    # Kill each process found  
    if [ -n "$PIDS" ]; then
        echo "$PIDS" | while read -r pid; do
        if [ -n "$pid" ] && [ "$pid" != "-" ]; then
            print_status "Found process $pid using port $PORT"
            
            # Get process info
            PROCESS_INFO=$(get_process_info "$pid")
            if [ -n "$PROCESS_INFO" ]; then
                echo "  Process info: $PROCESS_INFO"
            fi
            
            # Ask for confirmation if running interactively
            if [ -t 0 ] && [ -t 1 ]; then
                echo -n "Kill this process? (y/N): "
                read -r CONFIRM
                if [[ ! "$CONFIRM" =~ ^[Yy]$ ]]; then
                    print_status "Skipping process $pid"
                    continue
                fi
            fi
            
            # Kill the process
            if kill_process "$pid" "$PORT"; then
                print_success "Successfully killed process $pid"
            else
                print_error "Failed to kill process $pid"
            fi
        fi
        done
    fi
    
    # Final verification
    sleep 1
    REMAINING_PIDS=$(find_process_on_port $PORT)
    if [ -z "$REMAINING_PIDS" ]; then
        print_success "Port $PORT is now free"
    else
        print_warning "Some processes may still be running on port $PORT"
        echo "Remaining PIDs: $REMAINING_PIDS"
    fi
}

# Handle command line arguments
case "${1:-}" in
    -h|--help)
        echo "Usage: $0 [OPTIONS]"
        echo ""
        echo "Kill Flask application processes running on the configured port"
        echo ""
        echo "Options:"
        echo "  -h, --help     Show this help message"
        echo "  -f, --force    Skip confirmation prompts"
        echo "  -p, --port N   Override port (use specific port instead of config)"
        echo ""
        echo "The script reads the port from config.yaml by default"
        echo "If no processes are found, the script exits successfully"
        exit 0
        ;;
    -f|--force)
        # Non-interactive mode - don't ask for confirmation
        exec 0</dev/null
        main
        ;;
    -p|--port)
        if [ -z "$2" ]; then
            print_error "Port number required after -p/--port"
            exit 1
        fi
        PORT="$2"
        print_status "Using specified port: $PORT"
        PIDS=$(find_process_on_port $PORT)
        if [ -z "$PIDS" ]; then
            print_success "No processes found running on port $PORT"
            exit 0
        fi
        echo "$PIDS" | while read -r pid; do
            if [ -n "$pid" ]; then
                kill_process "$pid" "$PORT"
            fi
        done
        ;;
    "")
        main
        ;;
    *)
        print_error "Unknown option: $1"
        echo "Use -h or --help for usage information"
        exit 1
        ;;
esac