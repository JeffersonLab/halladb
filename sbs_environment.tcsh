#!/bin/tcsh

# sqlalchemy installd for python 3.11
# need to load this version (or set it as default? -- check with Ole)
# > module use /group/halla/modulefiles
# > module load python

set CURR_DIR=`pwd`
set RCDB_DIR=${CURR_DIR}/rcdb
set SBS_DIR=${CURR_DIR}/sbs_rcdb

# RCDB environment
if ( ! $?RCDB_HOME ) then
    setenv RCDB_HOME $RCDB_DIR
endif

if (! $?LD_LIBRARY_PATH) then
    setenv LD_LIBRARY_PATH $RCDB_HOME/cpp/lib
else
    setenv LD_LIBRARY_PATH "$RCDB_HOME/cpp/lib":$LD_LIBRARY_PATH
endif

if ( ! $?PYTHONPATH ) then
    setenv PYTHONPATH "$RCDB_HOME/python"
else
    setenv PYTHONPATH "$RCDB_HOME/python":$PYTHONPATH
endif

setenv PATH "$RCDB_HOME":"$RCDB_HOME/bin":"$RCDB_HOME/cpp/bin":$PATH

setenv PYTHONPATH "$CURR_DIR":"$RCDB_DIR":$PYTHONPATH

# Connection string
setenv RCDB_CONNECTION mysql://rcdb@chafs1.jlab.org/rcdb

# For test
#setenv RCDB_CONNECTION mysql://rcdb@chafs1.jlab.org/test
