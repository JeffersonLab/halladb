import xml.etree.ElementTree as Et
import os, sys

def xml_parser(fin):
    
    xml_root = Et.parse(fin).getroot()
    #xml_result = xml_root.fin(".//{*}session").text

    for session in xml_root.findall("session"):
        name = session.find("name").text
        config = session.find("config").text
        runnum = session.find("runnumber").text

        if "sbsts" in name:
            print(name, config, runnum)

    #print(xml_root[0][1].text)

if __name__== '__main__':
    xml_parser(sys.argv[1])
