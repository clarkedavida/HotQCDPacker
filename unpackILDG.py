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


#
# Collect information from lime QCDml
#
confQCDml  = readXML( limeFile.split('.')[0]+'.xml' )
LFN        = confQCDml['gaugeConfiguration']['dataLFN']
enslabel   = LFN.split('/')[-2]
ensQCDml   = readXML( enslabel+'.xml' )
Ns, Nt     = paramsFromEnsQCDml(ensQCDml)
prec       = confQCDml['gaugeConfiguration']['precision']
series     = confQCDml['gaugeConfiguration']['markovSequence']['series']
mstep      = confQCDml['gaugeConfiguration']['markovSequence']['markovStep']
algorithm  = confQCDml['gaugeConfiguration']['algorithm']['parameters']['parameter']
beta       = ensQCDml['markovChain']['physics']['action']['gluon']['treelevelSymanzikGluonAction']['beta']
quarks     = ensQCDml['markovChain']['physics']['action']['quark']['hisqQuarkAction']

ml = quarks[0]['mass']
ms = quarks[1]['mass']

algtable = {
    'always_acc' : -1, 
    'cgMax'      : -1, 
    'load_conf'  : -1, 
    'no_md'      : -1, 
    'no_pf'      : -1, 
    'no_step_sf' : -1, 
    'no_sw'      : -1, 
    'rand_flag'  : -1, 
    'seed'       : -1, 
    'step_size'  : -1 
}
for algp in algorithm:
    for name in algtable:
        if algp['name']==name:
            algtable[name]=algp['value'] 

for name in algtable:
    if algtable[name]==-1:
        logger.TBError(f'Unable to read paramter {name} from lime XML.') 


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
    logger.info(f'  {conf}')
    shell(f'cat {conf}.header {conf}.naked > {conf}')


#
# Reconstruct the rhmc parameter file
#
rhmcParam = open('rhmc.param','w')
rhmcParam.write(f'#\n')
rhmcParam.write(f'# rhmc.param\n')
rhmcParam.write(f'#\n')
rhmcParam.write(f'# Parameter file for RHMC runs with HISQ.\n')
rhmcParam.write(f'#\n')
rhmcParam.write(f'#      Lattice: Nx Ny Nz Nt\n')
rhmcParam.write(f'#         beta: Bare coupling constant 6/g^2\n')
rhmcParam.write(f'#        Nodes: Number of nodes per direction\n')
rhmcParam.write(f'#      mass_ud: Light quark mass\n')
rhmcParam.write(f'#       mass_s: Strange quark mass\n')
rhmcParam.write(f'#        no_pf: Number of pseudo-fermion fields\n')
rhmcParam.write(f'#\n')
rhmcParam.write(f'#    step_size: step size of trajectory\n')
rhmcParam.write(f'#        no_md: number of steps of trajectory\n')
rhmcParam.write(f'#   no_step_sf: number of steps of strange quark integration\n')
rhmcParam.write(f'#        no_sw: number of steps of gauge integration\n')
rhmcParam.write(f'#        cgMax: max cg steps for multi mass solver\n')
rhmcParam.write(f'#   always_acc: always accept configuration in Metropolis\n')
rhmcParam.write(f'#     rat_file: rational approximation input file\n')
rhmcParam.write(f'#\n')
rhmcParam.write(f'#    rand_flag: new random numbers(0)/read in random numbers(1)\n')
rhmcParam.write(f'#    rand_file: file name for random numbers and infos\n')
rhmcParam.write(f'#         seed: myseed\n')
rhmcParam.write(f'#    load_conf: flag_load (0=identity, 1=random, 2=getconf)\n')
rhmcParam.write(f'#   gauge_file: prefix for the gauge configuration file name\n')
rhmcParam.write(f'#      conf_nr: configuration number\n')
rhmcParam.write(f'#   no_updates: number of updates\n')
rhmcParam.write(f'#  write_every: write out configuration every\n')
rhmcParam.write(f'#\n')
rhmcParam.write(f'Lattice     = {Ns} {Ns} {Ns} {Nt} \n')
rhmcParam.write(f'Nodes       = 1 1 1 1\n')
rhmcParam.write(f'mass_ud     = {ml}\n')
rhmcParam.write(f'mass_s      = {ms}\n')
rhmcParam.write(f'beta        = {beta}\n')
rhmcParam.write(f'no_pf       = {algtable['no_pf']}\n')
rhmcParam.write(f'step_size   = {algtable['step_size']}\n')
rhmcParam.write(f'no_md       = {algtable['no_md']}\n')
rhmcParam.write(f'no_step_sf  = {algtable['no_step_sf']}\n')
rhmcParam.write(f'no_sw       = {algtable['no_sw']}\n')
rhmcParam.write(f'cgMax       = {algtable['cgMax']}\n')
rhmcParam.write(f'always_acc  = {algtable['always_acc']}\n')
rhmcParam.write(f'rat_file    = <RATFILE>\n')
rhmcParam.write(f'rand_flag   = {algtable['rand_flag']}\n')
rhmcParam.write(f'rand_file   = rand\n')
rhmcParam.write(f'seed        = {algtable['seed']}\n')
rhmcParam.write(f'load_conf   = {algtable['load_conf']}\n')
rhmcParam.write(f'gauge_file  = <GAUGEFILE> \n')
rhmcParam.write(f'conf_nr     = 0\n')
rhmcParam.write(f'no_updates  = 0\n')
rhmcParam.write(f'write_every = 0\n')
rhmcParam.close()


#
# Clean up after yourself
#
for naked_file in ls('*.naked'):
    rm(naked_file)
for header in ls('*.header'):
    rm(header)
rm(ILDGUNPACKER)

logger.info('Done!')
