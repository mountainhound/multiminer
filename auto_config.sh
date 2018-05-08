#!/bin/bash

tmux new-session -d -s CONFIG
tmux send-keys -t CONFIG "/home/micci-dev/multiminer/nvidia-settings.sh" C-m
tmux send-keys -t CONFIG "/home/micci-dev/OhGodAnETHlargementPill/OhGodAnETHlargementPill-r2" C-m
