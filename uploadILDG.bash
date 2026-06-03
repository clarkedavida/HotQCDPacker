#!/bin/bash
#
# uploadILDG.bash
#
# D. Clarke
#
# Wrap together the commands needed to upload to ILDG. Call with
#   uploadILDG.bash <lime-xml-file-name>
#

source env.bash

UPLOADENSEMBLE=false

# Get limeXML from user.
if [ -z "$1" ]; then
    echo "ERROR: no lime XML file provided. Usage: uploadILDG.bash <limeXML>"
    exit 1
fi
LIMEXML="$1"

# Written by Claude, sorry that this is unreadable.
LFN=$(sed -n 's|.*<dataLFN>\(.*\)</dataLFN>.*|\1|p' "${LIMEXML}")
ENS=$(basename "$(sed -n 's|.*<markovChainURI>\(.*\)</markovChainURI>.*|\1|p' "${LIMEXML}")")
ENSXML="${ENS}.xml"
LIME=$(basename "${LFN}")
SURL="${SE}/${LFN#lfn://}"

# A weak check that these variables were actually populated
for var in LFN ENS ENSXML LIME SURL; do
    if [ -z "${!var}" ]; then
        echo "ERROR: ${var} is empty. Check ${LIMEXML}."
        exit 1
    fi
done

# Optionally upload ensemble XML (only needed for first conf of ens)
if [ "$UPLOADENSEMBLE" = true ]; then
    ${ILDGMDC} -ie ${ENSXML}
fi

# Upload lime XML
${ILDGMDC} -ic ${LIMEXML}

# Upload lime file
${ILDGSE} -put ${LIME} ${SURL}

# Link LFN to SURL
${ILDGFC} -i ${LFN} ${SURL}

