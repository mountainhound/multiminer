#!/bin/bash

#WALLET=3C2686TfBdgJsLN3ibPQcpGysbnB4VdYgr.thinkpad
#WALLET=1FCLeN861h7SGSheTBDyBimQMQPNX8QUZX
#NICEHASH_WALLET=3C2686TfBdgJsLN3ibPQcpGysbnB4VdYgr
#EQUIHASH_WALLET=0x333b5748538B03362f70A1be261599eD963925dC

WALLET=33eyT1HqnAcZ6e4iFcqsUcozZuUdJnW3eb #Charles
NICEHASH_WALLET=33eyT1HqnAcZ6e4iFcqsUcozZuUdJnW3eb #Charles
ETHASH_WALLET=0x814a5e5a742c4377aac621419564242ae601f0c6 #Charles

export LD_LIBRARY_PATH=/usr/local/cuda-8.0/lib64:$LD_LIBRARY_PATH
export PATH=/usr/local/cuda-8.0/bin:$PATH

if [[ $1 = "-lyra2rev2" ]]; then
	./ccminer -a lyra2v2 -o stratum+tcp://lyra2v2.mine.zpool.ca:4533 -u $WALLET	-p [c=BTC] -b 4068
fi

if [[ $1 = "-nicehash-lyra2rev2" ]]; then
	./ccminer -a lyra2v2 -o stratum+tcp://lyra2rev2.usa.nicehash.com:3347 -u $NICEHASH_WALLET	-p [c=BTC] -b 4068
fi

if [[ $1 = "-equihash" ]]; then
	./ccminer -a equihash -o stratum+tcp://equihash.mine.zpool.ca:2142 -u $WALLET -p [c=BTC] -b 4068
fi

if [[ $1 = "-nicehash-equihash" ]]; then
	./ccminer -a equihash -o stratum+tcp://equihash.usa.nicehash.com:3357 -u $NICEHASH_WALLET -p [c=BTC] -b 4068
fi

if [[ $1 = "-ethash" ]]; then
	./ethminer -U -S eth-us-east1.nanopool.org:9999 -O $ETHASH_WALLET.dev-machine --farm-recheck 200 --api-port 4068
fi

if [[ $1 = "-ubiq" ]]; then
	./ethminer -U -SP 1 -S ubiq.hodlpool.com:8009 -O $ETHASH_WALLET.dev-machine --farm-recheck 200 --api-port 4068
fi

if [[ $1 = "-nicehash-ethash" ]]; then
	./ethminer -U -SP 2 -S daggerhashimoto.usa.nicehash.com:3353 -O $NICEHASH_WALLET --farm-recheck 200 --api-port 4068
fi

if [[ $1 = "-neoscrypt" ]]; then
	./ccminer -a neoscrypt -o stratum+tcp://neoscrypt.mine.zpool.ca:4233 -u $WALLET -p [c=BTC] -b 4068
fi

if [[ $1 = "-nicehash-neoscrypt" ]]; then
	./ccminer -a neoscrypt -o stratum+tcp://neoscrypt.usa.nicehash.com:3341 -u $NICEHASH_WALLET -p [c=BTC] -b 4068
fi

if [[ $1 = "-scrypt" ]]; then
	./ccminer -a scrypt -o stratum+tcp://scrypt.mine.zpool.ca:3433 -u $WALLET -p [c=BTC] -b 4068
fi

if [[ $1 = "-x11gost" ]]; then
	./ccminer -a x11 -o stratum+tcp://x11.mine.zpool.ca:3533 -u $WALLET -p [c=BTC] -b 4068
fi

if [[ $1 = "-nicehash-x11gost" ]]; then
	./ccminer -o stratum+tcp://x11gost.usa.nicehash.com:3359 -u $NICEHASH_WALLET -p [c=BTC] -b 4068
fi

if [[ $1 = "-x17" ]]; then
	./ccminer -a x17 -o stratum+tcp://x17.mine.zpool.ca:3737 -u $WALLET -p [c=BTC] -b 4068
fi

if [[ $1 = "-lyra2z" ]]; then
	./ccminer -a lyra2z -o stratum+tcp://lyra2z.mine.zpool.ca:4553 -u $WALLET -p [c=BTC] -b 4068
fi

if [[ $1 = "-decred" ]]; then
	./ccminer -a decred -o stratum+tcp://decred.mine.zpool.ca:5744 -u $WALLET -p [c=BTC] -b 4068
fi

if [[ $1 = "-nicehash-decred" ]]; then
	./ccminer -a decred -o stratum+tcp://decred.usa.nicehash.com:3354 -u $NICEHASH_WALLET -b 4068
fi

if [[ $1 = "-nicehash-blake14r" ]]; then
	./ccminer -a decred -o stratum+tcp://decred.usa.nicehash.com:3354 -u $NICEHASH_WALLET -b 4068
fi

if [[ $1 = "-blake2s" ]]; then
	./ccminer -a blake2s -o stratum+tcp://blake2s.mine.zpool.ca:5766 -u $WALLET -p [c=BTC] -b 4068
fi

if [[ $1 = "-blake14r" ]]; then
	./ccminer -a decred -o stratum+tcp://decred.mine.zpool.ca:5744 -u $WALLET -p [c=BTC] -b 4068
fi

if [[ $1 = "-nist5" ]]; then
	./ccminer -a nist5 -o stratum+tcp://nist5.mine.zpool.ca:3833 -u $WALLET -p [c=BTC] -b 4068
fi

if [[ $1 = "-nicehash-nist5" ]]; then
	./ccminer -a nist5 -o stratum+tcp://nist5.usa.nicehash.com:3340 -u $NICEHASH_WALLET -p [c=BTC] -b 4068
fi

if [[ $1 = "-lbry" ]]; then
	./ccminer -a lbry -o stratum+tcp://lbry.mine.zpool.ca:3334 -u $WALLET -p [c=BTC] -b 4068
fi

if [[ $1 = "-nicehash-lbry" ]]; then
	./ccminer -a lbry -o stratum+tcp://lbry.usa.nicehash.com:3356 -u $NICEHASH_WALLET -p [c=BTC] -b 4068
fi

if [[ $1 = "-xevan" ]]; then
	./ccminer-xevan -a xevan -o stratum+tcp://blake2s.mine.zpool.ca:3739 -u $WALLET -p [c=BTC] -b 4068
fi




