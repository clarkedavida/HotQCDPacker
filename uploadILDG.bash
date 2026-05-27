#!/bin/bash
#
# uploadILDG.bash
#
# D. Clarke
#
# Wrap together the commands needed to upload to ILDG.
#

source env.bash

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

# Upload ensemble and lime XML files
${ILDGMDC} -ie ${ENSXML}
${ILDGMDC} -ic ${LIMEXML}

# Upload lime file
${ILDGSE} -put ${LIME} ${SURL}

# Link LFN to SURL
${ILDGFC} -i ${LFN} ${SURL}

# See everything that has been uploaded
#${ILDGSE} -list ${LFN} -lol
#${ILDGSE} -lsa ${HOTQCDALLOC}
