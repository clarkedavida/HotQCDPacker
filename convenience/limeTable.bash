#!/bin/bash
#
# limeTable.bash
#
# D. Clarke
#
# Build a .txt file listing all HotQCD lime LFNs and SURLs. Paginates
# through all entries (100 at a time) and writes one "LFN SURL" line
# per entry to limeTable.txt.
#

source "${HOTQCDPACKER_DIR}/env.bash"
source "${HOTQCDPACKER_DIR}/convenience/convenience.bash"

OUTFILE="limeTable.txt"
PAGE_SIZE=100

# Get total count from first query
_bashInfo "Querying total lime count..."
TOTAL=$(${ILDGFC} -lsa ${HOTQCDALLOC} | grep "Total = " | awk '{print $3}')

if [ -z "$TOTAL" ]; then
  _bashFail "Could not determine total number of limes"
fi

_bashInfo "Found ${TOTAL} limes. Writing to ${OUTFILE}..."

echo "# LFN SURL" > "${OUTFILE}"

# Written by Claude
OFFSET=0
while [ $OFFSET -lt $TOTAL ]; do
  _bashInfo "Fetching entries ${OFFSET}–$((OFFSET + PAGE_SIZE - 1))..."
  if [ $OFFSET -eq 0 ]; then
    ${ILDGFC} -lsa ${HOTQCDALLOC}
  else
    ${ILDGFC} +${OFFSET} -lsa ${HOTQCDALLOC}
  fi | awk -F'|' '/lfn:\/\//{
    lfn=$1; surl=$2
    gsub(/^[[:space:]]+|[[:space:]]+$/, "", lfn)
    gsub(/^[[:space:]]+|[[:space:]]+$/, "", surl)
    print lfn "    " surl
  }' >> "${OUTFILE}"
  OFFSET=$((OFFSET + PAGE_SIZE))
done

_bashInfo "Done. ${TOTAL} entries written to ${OUTFILE}."
