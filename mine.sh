#!/bin/bash

#WALLET=3C2686TfBdgJsLN3ibPQcpGysbnB4VdYgr.thinkpad
WALLET=1FCLeN861h7SGSheTBDyBimQMQPNX8QUZX
NICEHASH_WALLET=3C2686TfBdgJsLN3ibPQcpGysbnB4VdYgr


if [[ $1 = "-lyra2rev2" ]]; then
	./ccminer -a lyra2v2 -o stratum+tcp://lyra2v2.mine.zpool.ca:4533 -u $WALLET	-p [c=BTC] -b 4068
fi

if [[ $1 = "-equihash" ]]; then
	./ccminer -a equihash -o stratum+tcp://equihash.mine.zpool.ca:2142 -u $WALLET -p [c=BTC] -b 4068
fi

if [[ $1 = "-neoscrypt" ]]; then
	./ccminer -a neoscrypt -o stratum+tcp://neoscrypt.mine.zpool.ca:4233 -u $WALLET -p [c=BTC] -b 4068
fi

if [[ $1 = "-scrypt" ]]; then
	./ccminer -a scrypt -o stratum+tcp://scrypt.mine.zpool.ca:3433 -u $WALLET -p [c=BTC] -b 4068
fi

if [[ $1 = "-x11" ]]; then
	./ccminer -a x11 -o stratum+tcp://x11.mine.zpool.ca:3533 -u $WALLET -p [c=BTC] -b 4068
fi

if [[ $1 = "-x11gost" ]]; then
	./ccminer -o stratum+tcp://x11gost.usa.nicehash.com:3359 -u $NICEHASH_WALLET -p [c=BTC] -b 4068
fi

if [[ $1 = "-lyra2z" ]]; then
	./ccminer -a lyra2z -o stratum+tcp://lyra2z.mine.zpool.ca:4553 -u $WALLET -p [c=BTC] -b 4068
fi

if [[ $1 = "-decred" ]]; then
	./ccminer -a decred -o stratum+tcp://decred.usa.nicehash.com:3354 -u $WALLET -b 4068
fi

if [[ $1 = "-blake2s" ]]; then
	./ccminer -a blake2s -o stratum+tcp://blake2s.mine.zpool.ca:5766 -u $WALLET -p [c=BTC] -b 4068
fi



