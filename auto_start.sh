#!/bin/bash

tmux new-session -d -s MINER
tmux send-keys -t MINER "sudo -i -u micci-dev" C-m
tmux send-keys -t MINER "export PATH=/usr/local/cuda-8.0/bin${PATH:+:${PATH}}" C-m
tmux send-key -t MINER "export LD_LIBRARY_PATH=/usr/local/cuda-8.0/lib64" C-m
tmux send-keys -t MINER "export PATH=/usr/local/cuda-9.0/bin${PATH:+:${PATH}}" C-m
tmux send-key -t MINER "export LD_LIBRARY_PATH=/usr/local/cuda-9.0/lib64" C-m
tmux send-key -t MINER "export CUDA_HOME=/usr/local/cuda" C-m
tmux send-keys -t MINER "vncserver :1" C-m
tmux send-keys -t MINER "cd /home/micci-dev/multiminer/" C-m
tmux send-keys -t MINER "miner-env/bin/python profit_switcher.py" C-m

#tmux send-keys -t MINER "send 'Mi((i'" C-m
