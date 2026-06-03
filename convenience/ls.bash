#!/bin/bash
# 
# ls.bash                                                               
# 
# D. Clarke
# 
# Show file with provided LFN. If no LFN provided, show
# first 100 HotQCD limes. 
# 

source "$(dirname "$0")/../env.bash"
source convenience.bash

LFN="$1"

if [ -z "$LFN" ]; then
  _bashInfo "No LFN provided, showing first 100 HotQCD limes"
  ${ILDGFC} -lsa ${HOTQCDALLOC}
else
  ${ILDGSE} -list ${LFN} -lol
fi
