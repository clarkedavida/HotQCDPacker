#!/bin/bash
# 
# search_conf.bash                                                               
# 
# D. Clarke
# 
# Search the metadata catalogue for configurations belonging 
# to ensemble with given mcURI. 
# 

source "${HOTQCDPACKER_DIR}/env.bash"
source "${HOTQCDPACKER_DIR}/convenience/convenience.bash"

MC="$1"

_checkIfEmpty "mcURI" "${MC}"

${ILDGMDC} -lc "${MC}"

