#!/usr/bin/env bash

# ensures command failure results in crash instead of unexpected behaviour
set -euo pipefail
 
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# checks for tty terminal - only printed when launched via terminal 
if [ -t 1 ]; then
    cat <<'BANNER'
 .d8888b.  888                                
d88P  Y88b 888                                
888    888 888                                
888        88888b.   .d88b.  888  888  .d88b. 
888        888 "88b d8P  Y8b `Y8bd8P' d8P  Y8b
888    888 888  888 88888888   X88K   88888888
Y88b  d88P 888  888 Y8b.     .d8""8b. Y8b.    
 "Y8888P"  888  888  "Y8888  888  888  "Y8888 
 
                                 Verelous Labs
BANNER
    echo
fi
 
# connects directly to python
exec python3 "$SCRIPT_DIR/src/uci.py"
