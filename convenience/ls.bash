#!/bin/bash
# 
# ls.bash                                                               
# 
# D. Clarke
# 
# Show file with provided LFN. If no LFN provided, show
# first 100 HotQCD limes. You can see more entries using
# pagination. So for example
#   - ./ls.bash                    : items 0–99
#   - ./ls.bash --offset 100       : items 100–199
#   - ./ls.bash --offset 200       : items 200–299
#   - ./ls.bash --lfn /some/lfn    : show specific file
# The Total = ... line printed at the end tells you how many items
# exist in total, so you know how many pages there are.
# 

source "${HOTQCDPACKER_DIR}/env.bash"
source "${HOTQCDPACKER_DIR}/convenience/convenience.bash"

LFN=""
OFFSET=""

while [[ $# -gt 0 ]]; do
  case "$1" in
    --lfn)
      LFN="$2"
      shift 2
      ;;
    --offset)
      OFFSET="$2"
      shift 2
      ;;
    *)
      echo "Unknown argument: $1"
      exit 1
      ;;
  esac
done

if [ -n "$LFN" ] && [ -n "$OFFSET" ]; then
  _bashError "--lfn and --offset cannot be used together"
  exit 1
fi

if [ -z "$LFN" ]; then
  if [ -n "$OFFSET" ]; then
    _bashInfo "No LFN provided, showing HotQCD limes with offset ${OFFSET}"
    ${ILDGFC} +${OFFSET} -lsa ${HOTQCDALLOC}
  else
    _bashInfo "No LFN provided, showing first 100 HotQCD limes"
    ${ILDGFC} -lsa ${HOTQCDALLOC}
  fi
else
  ${ILDGSE} -list ${LFN} -lol
fi
