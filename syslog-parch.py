#!/usr/bin/env python

# Author: James Simpson
# Version: 1.0

import smtplib

############################
#                          #
#        FUNCTIONS         #
#                          #
############################

#Function used for sending mail via an unauthenticated or open SMTP relay
def sendmail(FROM, TO, message):
	server = smtplib.SMTP('open.relay.address') 
	server.sendmail(FROM, TO, message)
	server.quit()

#Function used for sending mail via an SMTP relay requiring SSL
def sendmail_ssl(FROM, TO, message):
	server = smtplib.SMTP_SSL('ssl.smtp.server:465')
	server.login('username' 'password')
	server.sendmail(FROM, TO, message)
	server.quit()

def sort_devices(devices):
	sorted_devices = ""
	unique_devices = sorted(set(devices))
	for device in unique_devices:
		sorted_devices += device + "\n"

	return sorted_devices

############################
#                          #
#      GENERATE LIST       #
#                          #
############################
switches = []
bpdu = []
log = open("/logs/syslog")

for line in log:
	if "MACFLAP" in line:
		fields = line.strip().split()
		switches.append(fields[3])

	elif "BPDU" in line:
		fields = line.strip().split()
		bpdu.append(fields[3])

log.close

sorted_flaps = sort_devices(switches)
sorted_bpdus = sort_devices(bpdu)

############################
#                          #
#      MESSAGE PARAMS      #
#                          #
############################
FROM = 'gremlins@network'
TO = 'recipient@address.com'
SUBJECT = "Your subject line"
TEXT = sorted_flaps
TEXT2 = sorted_bpdus

message = """\
From: %s
To: %s
Subject: %s

The following devices have reported BPDUGUARD messages: \n
%s

The following devices have reported Mac Address Flapping: \n
%s
""" % (FROM, ", ".join(TO), SUBJECT, TEXT2, TEXT)

############################
#                          #
#        SEND EMAIL        #
#                          #
############################


sendmail(FROM, TO, message)
