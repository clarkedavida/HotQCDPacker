#!/bin/bash
# 
# ls.bash                                                               
# 
# D. Clarke
# 
# Show file with provided LFN. If no LFN provided, show
# first 100 HotQCD limes. You can see more entries using
# pagination. So for example
#   - try-fc -lsa j-hotqcd : items 0–99 
#   - try-fc +100 -lsa j-hotqcd : items 100–199
#   - try-fc +200 -lsa j-hotqcd : items 200–299
# The Total = ... line printed at the end tells you how many items 
# exist in total, so you know how many pages there are.
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
