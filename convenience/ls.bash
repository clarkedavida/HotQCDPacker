#!/bin/bash
# 
# ls.bash                                                               
# 
# D. Clarke
# 
# List the first 100 files of HotQCD allocation. 
# 

source "$(dirname "$0")/../env.bash"
${ILDGFC} -lsa ${HOTQCDALLOC} 
