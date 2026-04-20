# 
# packILDGcommon.py                                                               
# 
# D. Clarke
# 
# Auxiliary functions used by packILDG.py. This is also where you, the archiver,
# should fill out information needed for archiving. The intention of all this code
# is to pack HotQCD configurations in NERSC format; it may work in other contexts
# but you use at your own risk.
# 
from collections import OrderedDict
import os

from latqcdtools.base.utilities import byteConvert, shell
from latqcdtools.base.check import checkType
from latqcdtools.math.math import rel_check
from latqcdtools.physics.lattice_params import latticeParams
import latqcdtools.base.logger as logger


#
# ! ---- MAKE SURE YOU ADJUST PARAMETERS IN THIS BLOCK TO SUIT YOUR NEEDS ---- ! 
#
ARCHIVER              = 'David Anthony Clarke'
ARCHIVER_INSTITUTION  = 'Bielefeld University'
ARCHIVER_ORCID        = '0000-0002-5570-0894'
TIME_NOW              = '/home/dclarke/HotQCDPacker/hubert-mtime.pl'  # Gets current time
ILDGBINARY            = '/home/dclarke/try-binary/ildg-binary'        # LIME packer
ILDGMDC               = '/home/dclarke/try-client/try-mdc'            # metadata catalogue
ILDGFC                = '/home/dclarke/try-client/try-fc'             # file catalogue
ILDGSE                = '/home/dclarke/try-client/try-se'             # download files from storage element
GENERATOR             = 'Luis Altenkort'
GENERATOR_INSTITUTION = 'Bielefeld University'
GENERATOR_ORCID       = '0000-0001-9382-0208'
GENERATOR_TIMEZONE    = 'America/Detroit'                        # For conf date. List of zones here: https://en.wikipedia.org/wiki/List_of_tz_database_time_zones
CONF_REFERENCE        = '10.1103/PhysRevLett.132.051902'         # Reference to paper where conf were first used
CODE                  = 'SIMULATeQCD'                            # Code used to generate configurations
CODE_COMMENT          = 'WARNING: Code compile date is a guess'
CODE_VERSION          = 'UNKNOWN'
CODE_COMPILEDATE      = '2022-01-01T00:00:00+00:00'              # Unfortunately this is mandatory...
MACHINE               = 'Perlmutter'                             # Machine where confs were generated
MACHINE_TYPE          = 'NVIDIA A100'
MACHINE_INSTITUTE     = 'NERSC'
MACHINE_COMMENT       = None
SEQUENCE_COMMENT      = 'crcChecksum fields here are the NERSC checksums.'
PROJECT_NAME          = 'f21_highTspf'
NF                    = '21'
RHMC_PARAMFILE        = 'in.run_scratch'                         # Name of the SIMULATeQCD RHMC parameter file
REVISION_COMMENT      = None
FUNDING_INSTITUTES    = [                                        # Make sure element i of each list corresponds to the same award! 
                        'U.S. Department of Energy, Office of Science, Office of Nuclear Physics',
                        'U.S. Department of Energy, Office of Science, Office of Nuclear Physics',
                        'Deutsche Forschungsgemeinschaft', 
                        'U.S. Department of Energy, Office of Science, National Energy Research Scientific Computing Center',
                        'U.S. Department of Energy, Office of Science', 
                        ]
FUNDING_AWARDS        = [
                        None,
                        'SciDAC Fundamental Nuclear Physics at the Exascale and Beyond and the Topical Collaboration in Nuclear Theory Heavy-Flavor Theory (HEFTY) for QCD Matter',
                        'CRC-TR 211 Strong-interaction matter under extreme conditions',
                        None,
                        'USQCD Collaboration',
                        ]
FUNDING_AWARDNOS      = [
                        'Contract No. DE-SC0012704',
                        None, 
                        'Project No. 315477589-TRR 211',
                        'Contract No. DE-AC02-05CH11231',
                        None,
                        ]

#
# ! ---- The following parameters should not (need to) be adjusted ---- !
#
ILDGPACKER       = 'ILDG_pack.bash'
ILDGUNPACKER     = 'ILDG_unpack.bash'
XMLVALIDATOR     = '/home/dclarke/HotQCDPacker/xml/doValidate.bash'
SCHEMA_ENS       = '/home/dclarke/HotQCDPacker/xml/QCDmlEnsemble2.0.0.xsd'
SCHEMA_CONF      = '/home/dclarke/HotQCDPacker/xml/QCDmlConfig2.0.0.xsd'
COLLABORATION    = "hotqcd"
MAXLIMESIZEBYTES = byteConvert(200,'GB','B')                        # Hubert says lime files should not exceed 200 GB
GAUGEFIELD       = 'su3gauge'
NROWS            = 2
HEADER_LENGTH    = 11                                               # NERSC header length in lines
LICENSE          = "https://creativecommons.org/licenses/by/4.0/"


if NROWS==2:
    su3rep = 'su3r'
elif NROWS==1:
    su3rep = 'su3'
else:
    logger.TBError('NROWS must be 2 or 3')


def checkFileExists(f):
    if not os.path.isfile(f):
        logger.TBError(f'Missing file {f}')


def readHeader(hfile,Ns,Nt) -> dict:
    """
    Auxiliary function for getting information from NERSC headers. This also checks
    that the NERSC header is well formed and makes sense given Ns, Nt.
    
    Args:
        hfile (str): *.header file

    Returns:
        dict: Dictionary with info like precision, tr U, and so on. 
    """

    checkType(str,hfile=hfile)
    checkType('int',Ns=Ns)
    checkType('int',Nt=Nt)

    FOUNDBEGIN = False
    FOUNDEND   = False
    
    res = {
        'DATATYPE'   : None,
        'DIMENSION'  : [None,None,None,None],
        'CHECKSUM'   : None,
        'LINK_TRACE' : None,
        'PLAQUETTE'  : None,
        'PREC'       : None,
    }
    
    header = open(hfile,'r')
    for line in header:
        col = line.split()
        if line.startswith('BEGIN_HEADER'):
            FOUNDBEGIN = True
        if line.startswith('END_HEADER'):
            FOUNDEND = True
        if line.startswith('DATATYPE'):
            res['DATATYPE'] = col[2].strip()
        if line.startswith('DIMENSION'):
            dir = int(col[0].split('_')[1])
            extension = int(col[2].strip())
            res['DIMENSION'][dir-1] = extension
        if line.startswith('CHECKSUM'):
            res['CHECKSUM'] = col[2].strip()
        if line.startswith('LINK_TRACE'):
            res['LINK_TRACE'] = col[2].strip()
        if line.startswith('PLAQUETTE'):
            res['PLAQUETTE'] = col[2].strip()
        if line.startswith('FLOATING_POINT'):
            FP = col[2].strip()
            if FP == 'IEEE32BIG':
                res['PREC'] = 'single'
            elif FP == 'IEEE64BIG':
                res['PREC'] = 'double'
            else:
                logger.TBRaise(f'Got unexpected precision {FP}. Should be big endian right?')
    
    for key in res:
        if key=='DIMENSION':
            continue
        if res[key] is None:
            logger.TBRaise(f'{key} was not found in header')
    
    if not FOUNDBEGIN:
        logger.TBRaise('No BEGIN_HEADER')
    if not FOUNDEND:
        logger.TBRaise('No END_HEADER')
    if res['DATATYPE'] != '4D_SU3_GAUGE':
        logger.TBRaise(f"Expected 4D SU(3) gauge configuration. Got {res['DATATYPE']}")
    for dir in [0,1,2]:
        if res['DIMENSION'][dir] != Ns:
            logger.TBRaise(f'DIMENSION_{dir+1} != {Ns}')
    if res['DIMENSION'][3] != Nt:
        logger.TBRaise(f'DIMENSION_4 != {Nt}')
    
    header.close()

    return res



def readRHMCParamFile(pfile,lp) -> OrderedDict:
    """
    Auxiliary function for reading a SIMULATeQCD RHMC parameter file.

    Args:
        pfile (str)): name of parameter file
        lp (latticeParams): latticeParams object containing properties of ensemble

    Returns:
        OrderedDict: some algorithm-related parameters for later use in LIME QCDml file 
    """

    # Want ordered dictionary so elements always put in same order in QCDml file
    res = OrderedDict()
    res['always_acc'] = None
    res['cgMax'     ] = None
    res['load_conf' ] = None
    res['no_md'     ] = None
    res['no_pf'     ] = None
    res['no_step_sf'] = None
    res['no_sw'     ] = None
    res['rand_flag' ] = None
    res['seed'      ] = None
    res['step_size' ] = None
    
    params = open(pfile,'r')
    for line in params:
    
        if line.startswith('#'):
            continue
        col = line.split('=')
        if len(col)<2:
            continue
    
        param = col[0].strip()
    
        # Check lattice parameters match the ensemble string 
        if param=='Lattice':
            lat = col[1].strip().split()
            for i in [0,1,2]:
                if int(lat[i]) != lp.Ns:
                    logger.TBRaise(f'Lattice[{i+1}] != {lp.Ns}')
            if int(lat[3]) != lp.Nt:
                logger.TBRaise(f'Lattice[4] != {lp.Nt}')
        elif param=='mass_ud':
            mass = float(col[1].strip())
            if not rel_check(mass,lp.ml):
                logger.TBRaise(f'mass_ud != {lp.ml}')    
        elif param=='mass_s':
            mass = float(col[1].strip())
            if not rel_check(mass,lp.ms):
                logger.TBRaise(f'mass_ud != {lp.ms}')    
        elif param=='beta':
            beta = float(col[1].strip())
            if not rel_check(beta,lp.beta):
                logger.TBRaise(f'beta != {lp.beta}')    
    
        # Pick up the other run parameters
        else:
            if param in res:
                res[param] = col[1].strip()
        
    params.close()

    # Only take over the parameters you could find
    for key in res:
        if res[key] is None:
            del res[key]

    return res



class ensQCDmlSkeleton():

    def __init__(self,ens,lp,URI):
        """
        This is the skeleton for creating the ensemble QCDml file.

        Args:
            ens (str): HotQCD ensemble string of form l{Ns}{Nt}f21b{beta}m{ml}m{ms} 
            lp (latticeParams): latticeParams object containing properties of ensemble
        """
        checkType(str,ens=ens)
        checkType(latticeParams,lp=lp)

        self.QCDmlEnsembleFileName = f"{ens}.xml"
    
        self.size = {"x": lp.Ns, "y": lp.Ns, "z": lp.Ns, "t": lp.Nt  }
        if NF=='21':
            self.quarks    = {"l", "s"}
            self.Nf        = {"l": lp.Nf[0], "s": lp.Nf[1]}
            self.couplings = { "beta": lp.beta, "ml": lp.ml, "ms": lp.ms }
        else:
            logger.TBError(f'Nf = {NF} not yet supported.')

        self.license           = LICENSE 
        self.projectName       = PROJECT_NAME 
        self.collaboration     = COLLABORATION 
        self.ensembleName      = ens 
        self.markovChainURI    = URI 
        self.name              = ARCHIVER 
        self.orcid             = ARCHIVER_ORCID 
        self.institution       = ARCHIVER_INSTITUTION
        self.fundingInstitutes = FUNDING_INSTITUTES 
        self.fundingAwards     = FUNDING_AWARDS
        self.fundingAwardNos   = FUNDING_AWARDNOS
        self.date              = shell(TIME_NOW)



class limeQCDmlSkeleton():

    def __init__(self,limeName,series,prec,rhmc,generateDate):
        """
        This is the skeleton for creating the LIME QCDml file.

        Args:
            limeName (str): lime file containing packed configurations 
            series (str): series/stream label
            prec (str): single, double, or mixed 
            rhmc (OrderedDict): output from readRHMC 
            generateDate (str): date on which configurations were generated
        """

        checkType(str,limeName=limeName)
        checkType(str,series=series)
        checkType(str,prec=prec)
        checkType(OrderedDict,rhmc=rhmc)
        checkType(str,generateDate=generateDate)

        self.QCDmlConfigFileName = f'{limeName}.xml'
        self.reference           = CONF_REFERENCE 
        self.revisionNumber      = [0,1]
        self.revisionAction      = ["generate","add"]
        self.reviser             = [GENERATOR,ARCHIVER]
        self.reviserInstitute    = [GENERATOR_INSTITUTION,ARCHIVER_INSTITUTION]
        self.revisionDate        = [generateDate,shell(TIME_NOW)]
        self.revisions           = len(self.revisionNumber)
        self.code                = CODE 
        self.codeVersion         = CODE_VERSION 
        self.codeCompileDate     = CODE_COMPILEDATE 
        self.machineName         = MACHINE 
        self.machineType         = MACHINE_TYPE
        self.machineInstitute    = MACHINE_INSTITUTE
        self.parameterName       = []
        self.parameterValue      = []
        self.confComment         = [] # Going to use comment to hold trU
        self.series              = series
        self.update              = []
        self.plaquette           = []
        self.checksum            = []
        self.precision           = prec
        self.field               = GAUGEFIELD

        # Fill out algorithm details, grabbed from readRHMC
        for key in rhmc:
            self.parameterName.append(key)
            self.parameterValue.append(rhmc[key])

        # Optional information
        if CODE_COMMENT is not None:
            self.codeComment = CODE_COMMENT 
        if MACHINE_COMMENT is not None:
            self.machineComment = MACHINE_COMMENT 
        if REVISION_COMMENT is not None:
            self.revisionComment = REVISION_COMMENT 

    def appendToSequence(self,update,plaq,cksum,trU):
        """
        QCDml2.0 supports LIME files with multiple configurations saved in them, collected in a
        so-called sequence. This function allows you to append information about each packed
        configuration into the sequence.

        Args:
            update (int): trajectory number
            plaq (str): average plaquette 
            cksum (str): NERSC checksum
            trU (str): average link trace 
        """
        checkType(int,update=update)
        self.update.append(update)
        self.plaquette.append(plaq)
        self.checksum.append(cksum)
        self.confComment.append(f'LINK_TRACE = {trU}')
    

def paramsFromEnsQCDml(eQCDml):
    lat = eQCDml['markovChain']['physics']['size']
    Nx = int(lat['x'])
    Ny = int(lat['y'])
    Nz = int(lat['z'])
    Nt = int(lat['t'])
    if Nx!=Ny or Nx!=Nz or Ny!=Nz:
        logger.TBRaise('Expected Nx==Ny==Nz')
    return Nx, Nt


def writeHeader(ens,Ns,Nt,series,traj,cksum,trU,plaq,prec):
    header = open(f'{ens}_{series}.{traj}.header','w')
    header.write('BEGIN_HEADER\n')
    header.write('DATATYPE = 4D_SU3_GAUGE\n')
    for i in range(3):
        header.write(f'DIMENSION_{i+1} = {Ns}\n')
    header.write(f'DIMENSION_4 = {Nt}\n')
    header.write(f'CHECKSUM = {cksum}\n')
    header.write(f'LINK_TRACE = {trU}\n')
    header.write(f'PLAQUETTE = {plaq}\n')
    if prec=='single':
        header.write(f'FLOATING_POINT = IEEE32BIG\n')
    elif prec=='double':
        header.write(f'FLOATING_POINT = IEEE64BIG\n')
    header.write('END_HEADER\n')
    header.close()    

