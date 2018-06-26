#!/usr/bin/env python
 
import smtplib
import datetime
import os
import sys
import time

debug    = True # Turn into True to print debug info on terminal
period   = 10 # cycle period in seconds
iplist = ('192.168.1.53','192.168.1.20') # Mobile phone permanent lan ip list, can be any number of ip's
statusnet = dict()

 
#Define Username and Password of sender. I used a new gmail account
username = 'myemail@gmail.com'
password = 'pass'
 
def sendemail(result):
    if debug: return
    notifier = 'Bot'
    sender = 'home@gmail.com' # this is fake email from field
    receivers = ['mynormalemail@gmail.com'] #Use one or many email addresses by comma
    date = datetime.datetime.now().strftime( '%m/%d/%Y %H:%M:%S' )
    header = 'To:' + notifier + '\n' + 'From: ' + sender + '\n' + 'Subject: Bot ' + result +'\n'
    message = header + '\n' + 'date:' + '\n' + date + '\n' + 'Change: ' + result
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
    iplen = len(iplist)
    for ip in iplist: 
      statusnet[ip] = True
    while True:
      for ip in iplist:  
        if debug: print 'ping -c 3 -W 3 ' + ip
        net = os.system('ping -c 3 -W 3 ' + ip) 
        result=''
        if net == 0 and statusnet[ip] == True: 
            if debug: 
                print "ok!"
        if net != 0 and statusnet[ip] == True: 
            result += '%s Off home! ' % ip
            if debug: print "Offline"
            statusnet[ip] = False
        if net == 0 and statusnet[ip] == False: 
            result += '%s On home! ' % ip
            if debug: print "Online again! "
            statusnet[ip] = True 
        if  result != '':
            sendemail(result)
            if debug: print "mail sent! %s" % result
      time.sleep(period)
      continue
 
#Start
ping()
