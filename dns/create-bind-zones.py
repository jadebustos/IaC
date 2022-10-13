#!/usr/bin/python

# Copyright (c) 2022 Jose Angel de Bustos Perez
# May be copied or modified under the terms of 
# the GNU General Public License v3.0. 
# See https://www.gnu.org/licenses/gpl-3.0.html

import configparser
import argparse
import sys

from bind import *

# args: dictionary with command line arguments
def main(args):
    config = configparser.ConfigParser()
    # read configuration
    try:
        config.read(args['file'])
    except Exception as e:
        print(e)
        sys.exit(255)
    
    # process sections
    for sec in config.sections():
        zone_data = {}
        zone_data['fqdn'] = sec
        zone_data['network'] = config.get(sec, 'network')
        zone_data['csv'] = config.get(sec, 'csv')
        zone_data['primaryns'] = config.get(sec, 'primaryns')
        zone_data['masteremail'] = config.get(sec, 'masteremail')
        zone_data['refresh'] = config.get(sec, 'refresh')
        zone_data['retry'] = config.get(sec, 'retry')
        zone_data['expire'] = config.get(sec, 'expire')
        zone_data['minttl'] = config.get(sec, 'minttl')
        zone_data['serial'] = args['serial']
        
        myzone = Zone(zone_data)
        myzone.create_zone()

if __name__ == "__main__":

    # parser initialization
    msg = "Create bind zones script"
    parser = argparse.ArgumentParser(description=msg)

    # defining arguments
    parser.add_argument("-f", "--file", type=str, required=True, 
                            help = "Ini file to process.")

    parser.add_argument("-s", "--serial", type=str, required=True, 
                            help = "Serial for the day. Starts with 01, 02, ...")

    # parsing arguments
    args = parser.parse_args()

    main(vars(args))