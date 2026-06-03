#!/bin/bash
# 
# search_conf.bash                                                               
# 
# D. Clarke
# 
# Search the metadata catalogue for configurations belonging 
# to ensemble with given mcURI. 
# 

source "$(dirname "$0")/../env.bash"
source convenience.bash

MC="$1"

_checkIfEmpty "mcURI" "${MC}"

${ILDGMDC} -lc "${MC}"

