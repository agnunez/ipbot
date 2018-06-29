#!/usr/bin/env python
 
import smtplib
import datetime
import os
import sys
import time

debug    = True # Turn into True to print debug info on terminal
period   = 10  # cycle period in seconds
retry    = 3
deadline = 10
timeout  = 10

# list of ip, and is id names. List should be identical number of elements or only shorter is considered
iplist = ['192.168.1.12','192.168.1.13'] # Mobile phone permanent lan ip list, can be any number of ip's
ipname = ['Mobile1','Mobile2'] # Mobile phone permanent lan ip list, can be any number of ip's
statusnet = dict()

 
#Define Username and Password of sender. I used a new gmail account
username = 'senderemail@gmail.com'
password = 'pass'
 
def sendemail(result):
    if debug: 
        print "Sendmail simulated in debug mode. Turn debug to False to send real mails"
        return
    notifier = 'Bot'
    sender = 'fake@gmail.com' # this is fake email from field
    receivers = ['receiver@gmail.com'] #Use one or a list of email addresses separated by comma
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
 
#Start
ping()
