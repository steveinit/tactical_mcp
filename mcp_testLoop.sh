#!/bin/bash

# MCP Client Test Loop
# Runs MCP client test every 5 seconds

COUNTER=1
LOG_FILE="mcp_test_$(date +%Y%m%d_%H%M%S).log"

echo "Starting MCP client test loop..."
echo "Logging to: $LOG_FILE"
echo "Press Ctrl+C to stop"
echo ""

while true; do
    echo "=== Test Run #$COUNTER at $(date) ===" | tee -a $LOG_FILE
    
    # Run the MCP client test
    python3 test_mcp_client.py 2>&1 | tee -a $LOG_FILE
    
    echo "Test #$COUNTER completed. Waiting 5 seconds..." | tee -a $LOG_FILE
    echo "" | tee -a $LOG_FILE
    
    COUNTER=$((COUNTER + 1))
    sleep 5
done
