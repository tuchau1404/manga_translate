#!/bin/sh
export TORCH_HOME=$(pwd) && export PYTHONPATH=$(pwd)
./lama/bin/predict.py model.path=$(pwd)/lama/big-lama indir=$(pwd)/input outdir=$(pwd)/output