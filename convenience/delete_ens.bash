#!/bin/bash
# 
# delete_ens.bash                                                               
# 
# D. Clarke
# 
# Delete ens XML from MDC. You'll need the token from get_token.bash
# 

source "$(dirname "$0")/../env.bash"
source convenience.bash

MC="$1"

_checkIfEmpty "MC" "${MC}"

${ILDGMDC} -de "${MC}"
