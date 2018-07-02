#!/usr/bin/env python
import ConfigParser

debug=True
Config = ConfigParser.ConfigParser()
Config.read("ipbot.conf")
if debug: print "Config sections: ",Config.sections()
iplist = []
ipname = []

try:
  ssid = Config.get("wifi","ssid")
  pswd = Config.get("wifi","pswd")
except:
  print "format eror in  [wifi] configuration" 
if debug: print "ssid: %s, pass: '%s" % (ssid, pswd)

try:
  for name in Config.options("iplist"):
    ip=Config.get("iplist",name)
    iplist.extend([ip])
    ipname.extend([name])

    if debug: print "ip: %s, name: %s" % (ip,name)
except:
  print "format error in [iplist] section"

print "all ok"
print ipname
print iplist


