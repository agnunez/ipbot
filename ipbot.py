#!/usr/bin/env python
 
import smtplib
import datetime
import os
import sys
import time
import ConfigParser

# configuration file path
confile  = "/home/pi/ipbot.conf" # insert full path to a configuration file in a protected directory
logfile  = "/home/pi/ipbot.log"  # full path to a log file

# functions

def log(msg):
  file=open(logfile,"a")
  logmsg = "%s %s\n" % (time.strftime("%d/%m/%Y %H:%M:%S"),msg)
  file.write(logmsg)
  file.close()

def sendemail(result):
    if debug:
        print "Sendmail simulated in debug mode. Turn debug to False to send real mails"
        return
    notifier = 'Bot'
    sender = 'home@gmail.com' # this is fake email from field
    receivers = ['anunez@gmail.com'] #Use one or a list of email addresses separated by comma
    date = datetime.datetime.now().strftime( '%m/%d/%Y %H:%M:%S' )
    header = 'To:' + notifier + '\n' + 'From: ' + sender + '\n' + 'Subject: Bot ' + result +'\n'
    message = header + '\n' + 'date:' + '\n' + date + '\n' + 'Change: ' + result
    log(result)
    try:
        server_ssl = smtplib.SMTP_SSL("smtp.gmail.com", 465)
        server_ssl.ehlo() # optional, called by login()
        server_ssl.login(username, password)
        # ssl server doesn't support or need tls, so don't call server_ssl.starttls()
        server_ssl.sendmail(sender, receivers, message)
        #server_ssl.quit()
        server_ssl.close()
        if debug: print 'Email Sent'
    except smtplib.SMTPException:
        print 'Something broke. Remove Try/Except to debug.'
        sys.exit()

def ping():
    log("start")
    iplen = len(iplist)
    for ip in iplist:
      statusnet[ip] = True
    while True:
      for ip,name in zip(iplist,ipname):
        if debug: print 'ping -c %s -W %s -w %s %s' % (retry,deadline,timeout,ip)
        net = os.system('ping -c %s -W %s -w %s %s' % (retry,deadline,timeout,ip
))
        result=''
        if net == 0 and statusnet[ip] == True:
            if debug:
                print "ok!"
        if net != 0 and statusnet[ip] == True:
            result += '%s (%s) went Off home! ' % (name,ip)
            if debug: print '%s (%s) went Off home! ' % (name,ip)
            statusnet[ip] = False
        if net == 0 and statusnet[ip] == False:
            result += '%s (%s) arrived at home! ' % (name,ip)
            if debug: print '%s (%s) arrived at home! ' % (name,ip)
            statusnet[ip] = True
        if  result != '':
            sendemail(result)
            if debug: print "mail sent! %s" % result
      time.sleep(period)
      continue

#  Read configuration file 

try:
  Config = ConfigParser.ConfigParser()
  Config.read(confile)
except:
  print "Configuration file '%s' not found" % confile
  raise

try:
  debug    = (Config.get("params","debug")=="True")
  period   = int(Config.get("params","period"))
  retry    = int(Config.get("params","retry"))
  deadline = int(Config.get("params","deadline"))
  timeout  = int(Config.get("params","timeout"))
except:
  print "format error in [params] section"
  raise
if debug: print "period: %s, retry: %s, deadline: %s, timeout: %s" % (period,retry,deadline,timeout)

try:
  ssid = Config.get("wifi","ssid")
  pswd = Config.get("wifi","pswd")
except:
  print "format error in  [wifi] section of '%s' configuration file" % confile
  raise
if debug: print "ssid: %s, pass: '%s" % (ssid, pswd)

iplist = []  # init list of ip's
ipname = []  # init list of nicknames of ip's
try:
  for name in Config.options("iplist"):
    ip=Config.get("iplist",name)
    iplist.extend([ip])
    ipname.extend([name])
    if debug: print "ip: %s, name: %s" % (ip,name)
except:
  print "format error in [iplist] section"
  raise
if debug: print iplist,ipname

statusnet = dict()
 
#Define Username and Password of sender email account and receiver one(mailto)
try:
  username = Config.get("mail","username") # read user and password of smtp sender email account
  password = Config.get("mail","password")
  mailto   = Config.get("mail","mailto")   # read destination mail for sending messages
  if debug: print "username: '%s' password '%s' mailto '%s'" % (username,password,mailto)
except:
  print "format error in [mail] section of '%s' configuration file" % confile
  raise
 
# Start
ping()
