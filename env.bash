# 
# env.bash                                                               
# 
# D. Clarke
# 
# HotQCDPacker environment 
# 

#
# Adjust as needed
#
export CREATEQCDMLFOLDER=/home/${USER}/GitHub/createQCDml # Folder where you want to put createQCDml
export ILDGBINARYFOLDER=/home/${USER}/GitHub/try-binary   # Folder where you want to put try-binary 
export ILDGSERVICEFOLDER=/home/${USER}/GitHub/try-client  # Folder where you want to put try-client 

#
# Do not adjust
#
export ILDGMDC="${ILDGSERVICEFOLDER}/try-mdc"
export ILDGFC="${ILDGSERVICEFOLDER}/try-fc"
export ILDGSE="${ILDGSERVICEFOLDER}/try-se"
export SE='https://dcache.fz-juelich.de:2880/pnfs/fz-juelich.de/data/ildg' # SE location
export HOTQCDALLOC='j-hotqcd'
