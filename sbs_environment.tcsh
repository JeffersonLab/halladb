#!/bin/tcsh

set DB_HOME=/adaqfs/home/sbs-onl/rcdb
set RCDB_DIR=$DB_HOME/rcdb


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

setenv PYTHONPATH "$DB_HOME":"$RCDB_DIR":$PYTHONPATH

# Connection string
setenv RCDB_CONNECTION mysql://rcdb@chafs1.jlab.org/rcdb

# For test
#setenv RCDB_CONNECTION mysql://rcdb@chafs1.jlab.org/test
