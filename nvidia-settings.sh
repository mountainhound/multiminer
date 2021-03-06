#!/bin/bash
 
OPTS=`getopt -o m:g:p:n:i: --long mem-offset:,graphic-offset:,power-limit:,gpu-num:,init:, -n 'parse-options' -- "$@"`

if [ $? != 0 ] ; then echo "Failed parsing options." >&2 ; exit 1 ; fi

echo "$OPTS"
eval set -- "$OPTS"

MEM_OFFSET=-1
GRAPHIC_OFFSET=-1
POWER_LIMIT=-1
GPU_NUM=13
INIT_FLAG=0


while true; do
  case "$1" in
    -m | --mem-offset ) MEM_OFFSET="$2"; shift;shift ;;
    -g | --graphic-offset ) GRAPHIC_OFFSET="$2"; shift;shift ;;
    -p | --power-limit ) POWER_LIMIT="$2"; shift;shift ;;
    -n | --gpu-num ) GPU_NUM="$2"; shift;shift ;;
    -i | --init ) INIT_FLAG="$2"; shift;shift ;;
    -- ) shift; break ;;
    * ) break ;;
  esac
done

echo MEM_OFFSET=$MEM_OFFSET
echo GRAPHIC_OFFSET=$GRAPHIC_OFFSET
echo POWER_LIMIT=$POWER_LIMIT
echo GPU_NUM=$GPU_NUM
 
# Enable nvidia-smi settings so they are persistent the whole time the system is on.
if [ $INIT_FLAG == 1 ];
then
nvidia-xconfig -a --enable-all-gpus --cool-bits=28
fi

nvidia-smi -pm 1
## Apply settings to each GPU
COUNTER=0
while [  $COUNTER -lt $GPU_NUM ]; do
    
    if [ $POWER_LIMIT -gt -1 ];
    then
    nvidia-smi -i $COUNTER -pl $POWER_LIMIT
    fi

    DISPLAY=:0 XAUTHORITY=/var/run/lightdm/root/:0 nvidia-settings -a [gpu:$COUNTER]/GpuPowerMizerMode=0
    
    if [ $MEM_OFFSET -gt -1 ];
    then
    	DISPLAY=:0 XAUTHORITY=/var/run/lightdm/root/:0 nvidia-settings -a [gpu:$COUNTER]/GPUMemoryTransferRateOffset[3]=$MEM_OFFSET
    fi
    
    if [ $GRAPHIC_OFFSET -gt -1 ];
    then
    	DISPLAY=:0 XAUTHORITY=/var/run/lightdm/root/:0 nvidia-settings -a [gpu:$COUNTER]/GPUGraphicsClockOffset[3]=$GRAPHIC_OFFSET
    fi
    
    let COUNTER=COUNTER+1 
done
