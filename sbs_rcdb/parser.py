import logging
import os, sys
import xml.etree.ElementTree as Et
from subprocess import check_output
import subprocess
from datetime import datetime

from rcdb.log_format import BraceMessage as Lf

log = logging.getLogger("HallA_RCDB_parser")
log.addHandler(logging.NullHandler())

class EpicsParseResult(object):
    def __init__(self):
        self.beam_energy = None      # Beam energy
        self.beam_current = None     # Beam current
        self.target = None           # Target 
        self.bb_angle = None         # BB angle 
        self.sbs_angle = None        # SBS angle

class CodaParseResult(object):
    def __init__(self):
        self.session_name = None     # Coda session name
        self.config = None
        self.runnumber = None
        self.run_type = None

def epics_parser(epics_list):
    parse_result = {}
    for epics_name, cond_name in epics_list.items():
        parse_result[cond_name] = None
        try:
            cmds = ['caget', '-t', epics_name]
            out_str = subprocess.Popen(cmds, stdout=subprocess.PIPE).stdout.read().strip()
            value = out_str.decode('ascii')
            parse_result[cond_name] = float(value)
        except Exception as ex:
            log.warning("Error: " + str(ex))
            continue
    return parse_result

def coda_parser(session_file, parse_result):
    
    """
    <control>
      <session>
        <name>SBSGEM</name>
        <config>SBSGEMs</config>
        <runnumber>2021</runnumber>
      </session>
      <session>
        <name>sbsts</name>
        <config>GEnII-HCal-only</config>
        <runnumber>4691</runnumber>
      </session>
      <session>
        <name>undefined</name>
        <config>undefined</config>
        <runnumber>1</runnumber>
      </session>
    </control>
    """    

    xml_root = Et.parse(session_file).getroot()
    xml_result = xml_root.find("session").text

    if xml_result is None:
        log.warning("No <session> section found in controlSessions.xml")
        return parse_result

    for session in xml_root.findall("session"):
        name = session.find("name").text
        config = session.find("config").text
        runnum = session.find("runnumber").text
        if "sbsts" in name:
            parse_result.session_name = name
            parse_result.config = config
            parse_result.runnumber = int(runnum)
    
    return parse_result
