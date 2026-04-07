#!/usr/bin/env python3
#
# packILDG.py
#
# D. Clarke
#
# Port of packILDG.bash to Python. Packs HOTQCD gauge configurations into
# ILDG-format lime files and creates accompanying QCDml metadata. This expects
# 4d SU(3) gauge configurations. Given the parameters at the top of this script:
# 
# 1. Creates ensemble QCDml file
# 2. Looks in target folder and packs configurations together into lime files
#    not exceeding 200 GB.
# 3. Creates QCDml file for each lime 
#
# TODO: Annotation that checksum is not the CRC checksum but the NERSC one

import os, argparse

from latqcdtools.base.utilities import shell, getArgs
from latqcdtools.base.fileSystem import ls, rm, cd, getFileSize, getFileTimeStamp
from latqcdtools.interfaces.collaborations import HotQCDParams, paramFromEnsLabel
import latqcdtools.base.logger as logger

from createQCDml.QCDmlUtils import checkEnsembleProfile, checkConfigProfile, makeURI, makeLFN
from createQCDml.QCDmlWrite import writeQCDmlEnsembleFile, writeQCDmlConfigFile
import createQCDml.profiles.treeLevelSymanzikInfo as gActInfo
import createQCDml.profiles.HISQInfo as qActInfo

from packILDGcommon import *

for file in [ILDGBINARY, XMLVALIDATOR, SCHEMA_ENS, SCHEMA_CONF]:
    checkFileExists(file)

#
# Parse command-line arguments to get ens label and series. Deduce ensemble parameters from ens label. This
# only works if one follows the typical convention ens = l{Ns}{Nt}f21b{beta}m{ml}m{ms}
#
parser = argparse.ArgumentParser(description='Pack HOTQCD gauge configurations into ILDG lime files')
parser.add_argument('--ens'   , dest='ens'   , required=True, type=str, help='HotQCD ensemble label (enslabel)')
parser.add_argument('--series', dest='series', required=True, type=str, help='Series/stream label')
parser.add_argument('--dir'   , dest='dir'   , required=True, type=str, help='Pack confs in this directory')
args     = getArgs(parser)
enslabel = args.ens
series   = args.series
d        = args.dir
ensparam = paramFromEnsLabel(enslabel)
lp       = HotQCDParams(ensparam['Ns'],ensparam['Nt'],ensparam['cbeta'],ensparam['cm1'],ensparam['cm2'],Nf=NF)
Ns       = lp.Ns
Nt       = lp.Nt
cbeta    = lp.cbeta
cml      = lp.cml
cms      = lp.cms

#
# Create QCDml ensemble file at top level; check that it validates
#
URI = makeURI(COLLABORATION,PROJECT_NAME,enslabel)
ensmInfo = ensQCDmlSkeleton(enslabel,lp,URI)
checkEnsembleProfile( ensmInfo )
writeQCDmlEnsembleFile( ensmInfo, gActInfo, qActInfo )
shell(f'bash {XMLVALIDATOR} {SCHEMA_ENS} {enslabel}.xml')

#
# Go to folder with to-be-packed configurations
#
if not os.path.isdir(d):
    logger.TBError(f'Directory {d} does not exist?')
cd(d)
if not os.path.isfile(RHMC_PARAMFILE):
    logger.TBError(f'Missing RHMC parameter file {RHMC_PARAMFILE}')


#
# Generate list of to-be-packed confs, strip headers, and
# accumulate lines for the ILDGPACKER script
#
confs, trajs = [],[]
lime_size    = 0
logger.info('Remove headers...')
for conf in ls(f'{enslabel}_{series}*'):
    if conf.endswith('.naked') or conf.endswith('.lime') or conf.endswith('.header') or conf.endswith('.xml'):
        continue
    logger.info(f'  {conf}')
    shell(f'head -n {HEADER_LENGTH} {conf} > {conf}.header')
    shell(f'tail -n +{HEADER_LENGTH+1} {conf} > {conf}.naked') 
    confs.append(conf)
    trajs.append(int(conf.split('.')[1]))
    lime_size += getFileSize(conf)

if lime_size > MAXLIMESIZEBYTES:
    logger.TBError('Lime file should not exceed 200 GB.')

lime_filename = f'{enslabel}_{series}_{min(trajs)}to{max(trajs)}'

#
# Construct the packing command
#
packer_lines = ['#!/bin/bash\n']
LFN = makeLFN(COLLABORATION,PROJECT_NAME,enslabel,f'{lime_filename}.lime')
for i, conf in enumerate(confs):
    packer_lines.append(f'in{i}={conf}.naked\n')
packer_lines.append(f'limeout={lime_filename}.lime\n')
pack_cmd = (f'{ILDGBINARY} -crc -c -T {Nt} -L {Ns} -LFN {LFN} $limeout')
for i, conf in enumerate(confs):
    traj = conf.split('.',1)[1]
    pack_cmd += f' -{su3rep} +{traj} $in{i}'
packer_lines.append(pack_cmd + '\n')
with open(ILDGPACKER, 'w') as fh:
    fh.writelines(packer_lines)

#
# Pack configurations into lime file 
#
logger.info(f'Packing configurations {min(trajs)} to {max(trajs)} in {lime_filename}.lime...')
shell(f'bash {ILDGPACKER}')

#
# Create QCDml file for the lime
#
ensprec = None
rhmcParams = readRHMCParamFile(RHMC_PARAMFILE,lp)
for header in ls(f'{enslabel}_{series}*.header'):
    confProperties = readHeader(header,Ns,Nt)
    cksum = confProperties['CHECKSUM']
    prec  = confProperties['PREC']
    plaq  = confProperties['PLAQUETTE'] 
    trU   = confProperties['LINK_TRACE']
    traj  = int(header.split('.')[1])
    conf  = header[:-7]
    date  = getFileTimeStamp(conf,'hubert',GENERATOR_TIMEZONE)
    if ensprec is None:
        confInfo = limeQCDmlSkeleton(lime_filename,series,prec,rhmcParams,date)
        ensprec = prec
    else:
        if prec != ensprec:
            logger.TBError('Detected that not all precisions match!')
    confInfo.appendToSequence(traj,plaq,cksum,trU)
checkConfigProfile( confInfo )
writeQCDmlConfigFile( confInfo, dataLFN=LFN, markovChainURI=URI )
shell(f'bash {XMLVALIDATOR} {SCHEMA_CONF} {lime_filename}.xml')


#
# Clean up after yourself
#
for naked_file in ls('*.naked'):
    rm(naked_file)
for header in ls('*.header'):
    rm(header)
rm(ILDGPACKER)

cd('..')

logger.info('Done!')

