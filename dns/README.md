# DNS zones

The script **create-bind-zones.py** is used to create/udpate bind zones.

## Requirements

The following requirements are needed:

* python 3
* pandas 
* The user executing the script must have write access to the directories where zones and bind configuration are placed.

## Zone configuration data

To use you need an ini file with zone data:

```ini
[melmac.univ]

network = 192.168.1
csv = ~/src/mygithub/IaC/melmac.univ.csv
primaryns = beast.melmac.univ.
masteremail = root.beast.melmac.univ.
refresh = 21600
retry = 3600
expire = 604800
minttl = 86400
```

Where:

* **[melmac.univ]** is the dns zone name.
* **network** is the network address without the mask.
* **csv** csv file containing the dns entries.
* **primaryns** zone primary dns.
* **masteremail** zone master email.
* **refresh** refresh for the zone.
* **retry** retry for the zone.
* **expire** expire for the zone.
* **minttl** minimum TTL for the zone.

You can have one ini file per dns zone but you can also include several zones in the same ini file.

The csv file will have 5 fields using **;** as field separator:

1. The ip for the host.
2. Type of register, currently only **A** registers are supported.
3. Destination, this is the hostname without the domain for the **A** registries.
4. PTR data for the reverse zone.
5. Comments to add.

```
ip;register;destination;ptr;comments
192.168.1.110;A;lab-master;110;vm k8s master
192.168.1.111;A;lab-worker01;111;vm k8s node1
192.168.1.112;A;lab-worker02;112;vm k8s node2
```

In __vars.py__ configure:

* **zone_dir** with the directory where zones are stored.
* **zone_conf_dir** with the directory where bind configuration is stored.

## Using the script

To create the zones:

```bash
# python create-bind-zones.py -f zones.ini -s 01
```

* **-f zones.ini** zones to create/update.
* **-s 01** will be used as serial. In this case serial will be **YYYYMMDD01**.