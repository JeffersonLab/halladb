#!/bin/bash

RCDB_DIR=/adaqfs/home/sbs-onl/rcdb/rcdb
SBS_DIR=/adaqfs/home/sbs-onl/rcdb

# RCDB environment
if [[ -z $RCDB_HOME ]]; then
    export RCDB_HOME=$RCDB_DIR
fi

if [[ -z $LD_LIBRARY_PATH ]]; then
    export LD_LIBRARY_PATH=$RCDB_HOME/cpp/lib
else
    export LD_LIBRARY_PATH="$RCDB_HOME/cpp/lib":$LD_LIBRARY_PATH
fi

if [[ -z $PYTHONPATH ]]; then
    export PYTHONPATH="$RCDB_HOME/python"
else
    export PYTHONPATH="$RCDB_HOME/python":$PYTHONPATH
fi

export PATH="$RCDB_HOME":"$RCDB_HOME/bin":"$RCDB_HOME/cpp/bin":$PATH

export PYTHONPATH="$SBS_DIR":"$RCDB_DIR":$PYTHONPATH

# Connection string
export RCDB_CONNECTION=mysql://rcdb@chafs1.jlab.org/test

# For test
#export RCDB_CONNECTION=mysql://rcdb@chafs1.jlab.org/test
