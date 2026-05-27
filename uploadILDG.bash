#
# uploadILDG.bash
#
# D. Clarke
#
# Wrap together the commands needed to upload to ILDG. 
#

import sys
from packILDGcommon import ILDGMDC, ILDGFC, ILDGSE
from latqcdtools.base.utilities import shellVerbose
import latqcdtools.base.logger as logger

SHOWALLOCATIONS = True 
SE              = 'https://dcache.fz-juelich.de:2880/pnfs/fz-juelich.de/data/ildg'
ENSXML          = 'l6420f21b7570m003946m01973.xml'
ALLOC           = 'j-hotqcd'



{ILDGFC} -la

export BEARER_TOKEN={BEARER_TOKEN}

~/try-client/try-mdc -ie {ENSXML}
~/try-client/try-mdc -ic {LIMEXML} 
export SE={SE}

#                                            SURL
~/try-client/try-se -put 1_10010to10140.lime ${SE}/ldg/hotqcd/l6420f21b7570m003946m01973/1_10010to10140.lime

~/try-client/try-fc -i lfn://ldg/hotqcd/f21_highTspf/l6420f21b7570m003946m01973/1_10010to10140.lime ${SE}/ldg/hotqcd/l6420f21b7570m003946m01973/1_10010to10140.lime

~/try-client/try-se -list lfn://ldg/hotqcd/f21_highTspf/l6420f21b7570m003946m01973/1_10010to10140.lime -lol

~/try-client/try-se -lsa {ALLOC}

