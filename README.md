# pack/unpack ILDG

This is a bunch of Python scripts to pack HotQCD configurations
into LIME files. It generates QCDml files for the ensemble and
for each LIME file automatically.

To use this software, you need
1. [createQCDml](https://github.com/clarkedavida/createQCDml)
2. [AnalysisToolbox](https://github.com/LatticeQCD/AnalysisToolbox)
3. [try-binary](https://gitlab.desy.de/ildg/hands-on/try-binary)

To pack, call
```
python packILDG.py --ens <ensembleLabel> --series <stream> --dir <directory with to-be-packed configurations>
```
This will create the ensemble QCDml file on the current directory level, along with a lime file that contains 
all configurations inside the directory and a corresponding QCDml file for the lime. To unpack the lime file
and recover the configurations, call
```
python unpackILDG.py --lime <limeFile>
```
It will extract all configurations on the current directory level. 

