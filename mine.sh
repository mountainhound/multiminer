#!/bin/bash


#WALLET=1FCLeN861h7SGSheTBDyBimQMQPNX8QUZX #Parker-Coinbase
#NICEHASH_WALLET=1FCLeN861h7SGSheTBDyBimQMQPNX8QUZX #Parker-Coinbase
WALLET=395WprTpQkg4EU9e92gcBM4QDq4ataosAZ #Kraken BTC
ETHASH_WALLET=0xA13C320155F9A301F166C6FdE8189D974E9C1716 #Kraken-Eth
NICEHASH_WALLET=395WprTpQkg4EU9e92gcBM4QDq4ataosAZ #Kraken BTC
EQUIHASH_WALLET=t1NKe7ayhDZijC1TzNLfd5gPTBfbbU1Ktyg #Kraken ZCash

#WALLET=3C2686TfBdgJsLN3ibPQcpGysbnB4VdYgr #Grant
#NICEHASH_WALLET=3C2686TfBdgJsLN3ibPQcpGysbnB4VdYgr #Grant-Nicehash
#ETHASH_WALLET=0x333b5748538B03362f70A1be261599eD963925dC #Parker-Eth

WORKER_NAME=default_changeme

export LD_LIBRARY_PATH=/usr/local/cuda-8.0/lib64:$LD_LIBRARY_PATH
export PATH=/usr/local/cuda-8.0/bin:$PATH
export LD_LIBRARY_PATH=/usr/local/cuda-9.0/lib64:$LD_LIBRARY_PATH
export PATH=/usr/local/cuda-9.0/bin:$PATH
export LD_LIBRARY_PATH=/usr/local/cuda/lib64:$LD_LIBRARY_PATH
export PATH=/usr/local/cuda/bin:$PATH


if [[ $1 = "-lyra2rev2" ]]; then
	./ccminer-xevan -a lyra2v2 -o stratum+tcp://lyra2v2.mine.zergpool.com:4533 -u $WALLET -p [c=BTC] -b 4068
fi

if [[ $1 = "-nicehash-lyra2rev2" ]]; then
	./ccminer-xevan -a lyra2v2 -o stratum+tcp://lyra2rev2.usa.nicehash.com:3347 -u $NICEHASH_WALLET	-p [c=BTC] -b 4068
fi

if [[ $1 = "-equihash-ccminer" ]]; then
	./ccminer -a equihash -o stratum+tcp://zec.2miners.com:1010 -u $EQUIHASH_WALLET -p [c=BTC] -b 4068
fi

if [[ $1 = "-equihash" ]]; then
	./ewbf_miner --server zec.2miners.com --user $EQUIHASH_WALLET.$WORKER_NAME --pass x --port 1010 --api 0.0.0.0:4068
fi

if [[ $1 = "-nicehash-equihash" ]]; then
	./ccminer -a equihash -o stratum+tcp://equihash.usa.nicehash.com:3357 -u $NICEHASH_WALLET -p [c=BTC] -b 4068
fi

if [[ $1 = "-ethash" ]]; then
	./ethminer -U -S eth-us-east1.nanopool.org:9999 -O $ETHASH_WALLET.$WORKER_NAME --farm-recheck 200 --api-port 4068
fi

if [[ $1 = "-ubiq" ]]; then
	./ethminer -P stratum1+tcp://$UBIQ_WALLET.$WORKER_NAME@ubiq.hodlpool.com:8009 --farm-recheck 200 --api-port 4068
fi

if [[ $1 = "-nicehash-ethash" ]]; then
	./ethminer -SP 2 -U -S daggerhashimoto.usa.nicehash.com:3353 -O $NICEHASH_WALLET --farm-recheck 200 --api-port 4068
fi

if [[ $1 = "-neoscrypt" ]]; then
	./ccminer -a neoscrypt -o stratum+tcp://neoscrypt.mine.zergpool.com:4233 -u $WALLET -p [c=BTC] -b 4068
fi

if [[ $1 = "-nicehash-neoscrypt" ]]; then
	./ccminer -a neoscrypt -o stratum+tcp://neoscrypt.usa.nicehash.com:3341 -u $NICEHASH_WALLET -p [c=BTC] -b 4068
fi

if [[ $1 = "-scrypt" ]]; then
	./ccminer -a scrypt -o stratum+tcp://scrypt.mine.zergpool.com:3433 -u $WALLET -p [c=BTC] -b 4068
fi

if [[ $1 = "-x11gost" ]]; then
	./ccminer -a x11 -o stratum+tcp://x11.mine.zpool.ca:3533 -u $WALLET -p [c=BTC] -b 4068
fi

if [[ $1 = "-nicehash-x11gost" ]]; then
	./ccminer -o stratum+tcp://x11gost.usa.nicehash.com:3359 -u $NICEHASH_WALLET -p [c=BTC] -b 4068
fi

if [[ $1 = "-x17" ]]; then
	./ccminer -a x17 -o stratum+tcp://x17.mine.zergpool.com:3737 -u $WALLET -p [c=BTC] -b 4068
fi

if [[ $1 = "-lyra2z" ]]; then
	./ccminer -a lyra2z -o stratum+tcp://lyra2z.mine.zergpool.com:4553 -u $WALLET -p [c=BTC] -b 4068
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
	./ccminer -a blake2s -o stratum+tcp://blake2s.mine.zergpool.com:5766 -u $WALLET -p [c=BTC] -b 4068
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
	./ccminer-xevan -a xevan -o stratum+tcp://blake2s.mine.zergpool.com:3739 -u $WALLET -p [c=BTC] -b 4068
fi

if [[ $1 = "-phi1612" ]]; then
	./ccminer-phi -a phi -o stratum+tcp://phi.mine.zergpool.com:8333 -u $WALLET -p [c=BTC] -b 4068
fi

if [[ $1 = "-timetravel10" ]]; then
	./ccminer -a timetravel -o stratum+tcp://timetravel.mine.zergpool.com:3555 -u $WALLET -p [c=BTC] -b 4068
fi






