import os, sys
from datetime import datetime, timedelta
import argparse
import logging

import rcdb
from rcdb.log_format import BraceMessage as Lf
from sbs_rcdb import SBSConditions, parser
from sbs_rcdb.parser import CodaParseResult, EpicsParseResult

#########################
# MODIFY HERE
#########################

# full path to controlSessions.xml file
session_xml_file = "/adaqfs/home/sbs-onl/coda/coolDB/SBSDAQ/ddb/controlSessions.xml"

def get_epics_list():
    # Define epics variables to read
    epics_list = {
        "HALLA:p":SBSConditions.BEAM_ENERGY,
        "IBC1H04CRCUR2":SBSConditions.BEAM_CURRENT,
        #"":SBSConditions.BB_ANGLE,
        #"":SBSConditions.SBS_ANGLE,
        "MSUPERBIGBITE":SBSConditions.SBS_CURRENT,
        "MBIGBITE":SBSConditions.BB_CURRENT,
    }
    return epics_list

#########################
# END OF MODIFICATION
#########################

def main():
    # Get the start/end time
    time_now= datetime.now()

    # logger
    log = logging.getLogger("halla.rcdb") # create run configuration standard logger
    log.addHandler(logging.StreamHandler(sys.stdout)) # add console output for logger
    log.setLevel(logging.INFO) # INFO: for less output, change it to DEBUG for printing everything

    # parse args
    argparser = argparse.ArgumentParser(description=" Update Hall A RCDB", usage=get_usage())
    argparser.add_argument("--run", type=int, help="Run number to update", required=True)
    #argparser.add_argument("--daq",  help="DAQ session: HMS, SHMS, NPS, COIN", required=True)
    argparser.add_argument("--update", help="Comma separated, modules to update such as coda, epics", default="coda,epics")
    argparser.add_argument("--reason", help="Reason for the update: start, update, end", default="start")
    argparser.add_argument("--exp", help="Experiment name", default="SBS")
    argparser.add_argument("--test", help="Test mode flag", default=False)
    argparser.add_argument("-v","--verbose", help="increase output verbosity", action="store_true")
    argparser.add_argument("-c","--connection", help="connection string, e.g: mysql://rcdb@chafs1.jlab.org/rcdb")
    args = argparser.parse_args()

    # Set log output level
    log.setLevel(logging.DEBUG if args.verbose else logging.INFO)

    # Run number to update
    run_num = args.run

    # Connection string
    if args.connection:
        con_str = args.connection
    elif "RCDB_CONNECTION" in os.environ:
        con_str = os.environ["RCDB_CONNECTION"]
    else:
        print("ERROR: RCDB_CONNECTION is not set and is not given as a script parameter (-c)")
        argparser.print_help()
        sys.exit(2)

    # Connect to the DB
    db = rcdb.RCDBProvider(con_str)

    # Conditions to add
    conditions = []

    # What to update
    update_parts = []
    if args.update:
        update_parts = args.update.split(",")
    log.debug(Lf("update parts = '{}'", update_parts))

    # Why are we updating
    update_reason = args.reason
    log.debug(Lf("update reason = '{}'", update_reason))

    # parse epics info
    epics_list = get_epics_list()
    if "epics" in update_parts:
        log.debug(Lf("Adding epics info to DB", ))
        epics_result = parser.epics_parser(epics_list)

        # add conditions
        for key in epics_result:
            if epics_result[key] is not None:
                conditions.append((key, epics_result[key]))
                
    # parse coda info
    if "coda" in update_parts:
        log.debug(Lf("Adding coda conditions to DB", ))
        coda_parse_result = CodaParseResult()
        parser.coda_parser(session_xml_file, coda_parse_result)
        
        if int(coda_parse_result.runnumber) != run_num:
            log.warn("ERROR: Coda parser run number mismatch. Skip coda update\n")
        else:
            conditions.append((rcdb.DefaultConditions.SESSION, coda_parse_result.session_name))
            conditions.append((rcdb.DefaultConditions.RUN_CONFIG, coda_parse_result.config))

    ######  UPDATE  ######
    if args.test:
        print(conditions)
    else:
        run = db.get_run(run_num)
        if not run:
            run = db.create_run(run_num)

        run.start_time = time_now

        # Update the DB
        db.add_conditions(run, conditions, replace=True)    
        db.session.commit()

def get_usage():
    return """
    
    Usage:
    python3 run_start.py --run=<run number> -c <db_connection string> --update=[coda,epics] --reason=[start,update,end] --exp=SBS

    Examples:
    Update epics info only, at the start of run
    > python3 run_start.py --run=123 --update=epics --reason=start --exp=SBS

    Update both coda, epics info, at the end of the run
    > python3 run_start.py --run=123 --update=coda,epics --reason=end --exp=SBS

    Run the script in Test mode:
    > python3 run_start.py --test --run=123 --update=coda,epics --reason=end --exp=SBS
    """
    
if __name__=="__main__":
    main()
