import os
import sys
import subprocess
from datetime import datetime, timedelta

# rcdb stuff
import rcdb

TEST_MODE = False

def update(run_num):

    # Connection string
    con_str = os.environ["RCDB_CONNECTION"] \
        if "RCDB_CONNECTION" in os.environ.keys() \
        else "mysql://rcdb@localhost/rcdb"


    db = rcdb.RCDBProvider(con_str)
    
    # start, end time
    time_end = datetime.now()
    time_start = time_end - timedelta(minutes=3)
    
    run = db.get_run(run_num)
    if not run:
        run = db.create_run(run_num)
    
    # Add conditions
    run.start_time = time_start
    run.end_time = time_end
    
    conditions = []
    conditions.append((rcdb.DefaultConditions.USER_COMMENT, "test db entry"))
    conditions.append((rcdb.DefaultConditions.RUN_TYPE, "TEST"))
    conditions.append(("target", "Home"))
    
    if TEST_MODE:
        for condition in conditions:
            print('%s %s' % (str(condition[0]), str(condition[1])))
    else:
        db.add_conditions(run, conditions, replace=True)
        db.session.commit()

if __name__=="__main__":
    update(sys.argv[1])
