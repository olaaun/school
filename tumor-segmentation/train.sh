#!/bin/sh
TIMESTAMP=`date +"%Y-%m-%d_%H-%M-%S"`
python solve.py 2>&1 | tee log/train_$TIMESTAMP.log
