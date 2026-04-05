# 
# unpackILDG.py                                                               
# 
# D. Clarke
# 
# Use lime file and QCDml to extract configurations.
# 

import argparse

from latqcdtools.base.utilities import getArgs
from latqcdtools.interfaces.interfaces import readXML
from latqcdtools.base.fileSystem import ls, rm
import latqcdtools.base.logger as logger
from packILDGcommon import *


parser = argparse.ArgumentParser(description='Unpack gauge configurations from LIME')
parser.add_argument('--lime', dest='lime', required=True, type=str, help='HotQCD lime file')
args = getArgs(parser)

limeFile = args.lime

if not limeFile.endswith('.lime'):
    logger.TBError('Must pass a .lime file')

confQCDml = readXML( limeFile.split('.')[0]+'.xml' )
enslabel  = limeFile.split('_')[0]
ensQCDml  = readXML( enslabel+'.xml' )
Ns, Nt    = paramsFromEnsQCDml(ensQCDml)
prec      = confQCDml['gaugeConfiguration']['precision']
series    = confQCDml['gaugeConfiguration']['markovSequence']['series']
mstep     = confQCDml['gaugeConfiguration']['markovSequence']['markovStep']


#
# Construct the unpacking command and restore headers
#
unpacker_lines = ['#!/bin/bash\n']
confs, trajs = [], []
for i in range(len(mstep)):
    info  = mstep[i]
    trU   = info['annotation'].split('=')[1].strip()
    traj  = info['update']
    cksum = info['record']['crcCheckSum']
    plaq  = info['record']['avePlaquette']
    conf  = f'{enslabel}_{series}.{traj}'
    confs.append(conf)
    trajs.append(traj)
    writeHeader(enslabel,Ns,Nt,series,traj,cksum,trU,plaq,prec)
    unpacker_lines.append(f'out{i}={conf}.naked\n')
unpacker_lines.append(f'limein={limeFile}\n')
unpack_cmd = (f'{ILDGBINARY} -x $limein')
for i in range(len(confs)):
    unpack_cmd += f' -{su3rep} +{trajs[i]} $out{i}'
unpacker_lines.append(unpack_cmd + '\n')
with open(ILDGUNPACKER, 'w') as fh:
    fh.writelines(unpacker_lines)


#
# Unpack the lime file
#
logger.info(f'Unpacking {limeFile}...')
shell(f'bash {ILDGUNPACKER}')


#
# Prepend headers to front of configurations
#
logger.info(f'Reconstrucing configurations...')
for i in range(len(mstep)):
    info  = mstep[i]
    traj  = info['update']
    conf  = f'{enslabel}_{series}.{traj}'
    shell(f'cat {conf}.header {conf}.naked > {conf}')


#
# Clean up after yourself
#
for naked_file in ls('*.naked'):
    rm(naked_file)
for header in ls('*.header'):
    rm(header)
rm(ILDGUNPACKER)

logger.info('Done!')
