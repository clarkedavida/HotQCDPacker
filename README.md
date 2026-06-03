
Here are a bunch of ILDG and Bash scripts to help streamline the upload of
HotQCD configurations to ILDG.

To use this software, you need
1. Python 3.9+ (For the AnalysisToolbox)
2. [createQCDml](https://github.com/clarkedavida/createQCDml)
3. [AnalysisToolbox](https://github.com/LatticeQCD/AnalysisToolbox)
4. [try-binary](https://gitlab.desy.de/ildg/hands-on/try-binary)
5. [try-client](https://gitlab.desy.de/ildg/hands-on/try-client.git)

The main scripts you will use are 
1. `packILDG.py` and `unpackILDG.py`
2. `convenience/get_token.bash`
3. `uploadILDG.bash`

In the `convenience` folder there are other Bash wrappers for
some of the `try-client` commands. These are just to make things easier
for me. You don't need to use them.

## Getting started

1. Have a look at `env.bash`. Those are the locations where you want to keep
the auxiliary software above. Adjust as needed.
2. Have a look at `setUp.bash`. Adjust as needed to install whichever auxiliary
software you are missing. Note that the `try-binary` software will need to be compiled.
3. Call `./setUp.bash`. Besides installation, this is necessary to make sure
scripts know where to look for auxiliary software. You may need to close and reopen
your terminal

## Packing configurations
To pack, call
```
python packILDG.py --ens <ensembleLabel> --series <stream> --dir <directory with to-be-packed configurations>
```
This will create the ensemble QCDml file on the current directory level, along with a lime file that contains 
all configurations inside the directory and a corresponding QCDml file for the lime. 

## Unpacking a lime file
To unpack the lime file and recover the configurations, call
```
python unpackILDG.py --lime <limeFile>
```
It will extract all configurations on the current directory level.

## Uploading XML and lime files to ILDG
To upload to ILDG, you need a HotQCD bearer token. (I assume you already have the necessary permissions
to get this token. If not, contact one of the HotQCD scientists.) You get this token with
```
bash getToken.bash
```
following the instructions it gives you. Once `getToken.bash` gives you the token, export the token.
Then call
```
bash uploadILDG.bash <limeXML>
```
where `limeXML` is the QCDml for the lime file you wish to upload.

## Why is this code part Bash part Python?
I tried to do everything in Python, I really did. But I couldn't get the upload to work
in Python so I gave up and resorted to Bash. My Bash skills are not that great, so
I needed help from [Claude](https://claude.ai/login) in a couple places. I marked where 
I used Claude.

## More information
You can learn more about how to use some of the metadata catalogue, file catalogue,
and storage element commands at https://slides.koutsou.net/ILDG-hands-on-2025-07-08/#1
