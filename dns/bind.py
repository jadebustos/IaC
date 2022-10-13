# Copyright (c) 2022 Jose Angel de Bustos Perez
# May be copied or modified under the terms of 
# the GNU General Public License v3.0. 
# See https://www.gnu.org/licenses/gpl-3.0.html

import datetime
import pandas as pd
import os

from vars import *

class Zone:
    def __init__(self, zone_data):
        self.data = zone_data
        self.inv_name = self.data['network'].split('.')
        self.inv_name.reverse()
        self.inv_name = '.'.join(self.inv_name) + '.in-addr.arpa'
    
    def read_data(self):
        zone_file = [] # zone file
        inv_zone_file = [] # reverse zone file
        zone_conf_file = [] # zone configuration file

        serial = datetime.datetime.now().strftime('%Y%m%d')
        data = pd.read_csv(self.data['csv'], header=0, sep=';', 
                    names=['IP', 'Register', 'Destination', 'PTR', 'Comments'])
        
        # header for zone file
        zone_file.append('$TTL 4H')
        zone_file.append('@\tIN\tSOA\t' + self.data['primaryns'] + '\t' + self.data['masteremail'] + '\t(')
        zone_file.append('\t\t\t\t' + serial + self.data['serial'] + '\t; serial')
        zone_file.append('\t\t\t\t' + self.data['refresh'] + '\t\t; refresh')
        zone_file.append('\t\t\t\t' + self.data['retry'] + '\t\t; retry')
        zone_file.append('\t\t\t\t' + self.data['expire'] + '\t\t; expire')
        zone_file.append('\t\t\t\t' + self.data['minttl'] + '\t\t; minimum TTL')
        zone_file.append('\t\t\t\t)')
        zone_file.append('\tIN\tNS\t' + self.data['primaryns'])
        zone_file.append('\n')

        # header for the inverse zone file
        inv_zone_file = zone_file.copy()

        for item in data.to_numpy().tolist():
            # create zone file
            zone_file.append(item[2] + '\tIN\t' + item[1] + '\t' + item[0] + '\t; ' + item[4]) 
            # create inverse zone file
            inv_zone_file.append(str(item[3]) + '\tIN\tPTR\t' + item[2] + '.' + self.data['fqdn'] + '.\t; ' + item[4])

        zone_file.append('\n')
        inv_zone_file.append('\n')

        # zone configuration file
        zone_conf_file.append('zone \"' + self.data['fqdn'] + '\" IN {')
        zone_conf_file.append('\ttype master;')
        zone_conf_file.append('\tfile \"' + os.path.join(zone_dir, 'named.' + self.data['fqdn']) +'\";')
        zone_conf_file.append('\tallow-update { none; };')
        zone_conf_file.append('};\n')
        zone_conf_file.append('zone \"' + self.inv_name + '\" IN {')
        zone_conf_file.append('\ttype master;')
        zone_conf_file.append('\tfile \"' + os.path.join(zone_dir, self.inv_name + '.' + self.data['fqdn']) +'\";')
        zone_conf_file.append('\tallow-update { none; };')
        zone_conf_file.append('};\n')

        # return zones
        return zone_file, inv_zone_file, zone_conf_file

    def create_zone(self):
        zone, inv_zone, zone_conf = self.read_data()
        # zone file
        zone_file = os.path.join(zone_dir, "named." + self.data['fqdn'])
        # reverse zone file
        inv_filename = self.inv_name + '.' + self.data['fqdn']
        inv_zone_file = os.path.join(zone_dir, inv_filename)
        # configuration zone file
        zone_conf_file = os.path.join(zone_conf_dir, self.data['fqdn'] + '.conf')


        # write zone file
        with open(zone_file, "w") as zonefile:
            zonefile.write('\n'.join(str(item) for item in zone))
        zonefile.close()
        os.chmod(zone_file, 0o644)

        # write reverse zone file
        with open(inv_zone_file, "w") as zonefile:
            zonefile.write('\n'.join(str(item) for item in inv_zone))
        zonefile.close()
        os.chmod(inv_zone_file, 0o644)

        # write configuration zone file
        with open(zone_conf_file, "w") as zonefile:
            zonefile.write('\n'.join(str(item) for item in zone_conf))
        zonefile.close()
        os.chmod(zone_conf_file, 0o644)

        # add zone to bind configuration file
        zoneconf = 'include \"/etc/named/' + self.data['fqdn'] + '.conf\";'
        with open(bind_conf_file, "r") as bindfile:
            if not any(zoneconf == x.rstrip('\r\n') for x in bindfile):
                bindfile.close()
                with open(bind_conf_file, "a+") as bindfile:
                    bindfile.write(zoneconf + '\n')
        bindfile.close()