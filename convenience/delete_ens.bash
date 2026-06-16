#!/bin/bash
# 
# delete_ens.bash                                                               
# 
# D. Clarke
# 
# Delete ens XML from MDC. You'll need the token from get_token.bash
# 

source "${HOTQCDPACKER_DIR}/env.bash"
source "${HOTQCDPACKER_DIR}/convenience/convenience.bash"

MC="$1"

_checkIfEmpty "MC" "${MC}"

${ILDGMDC} -de "${MC}"
