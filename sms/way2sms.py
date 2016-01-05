#!/usr/bin/python
import cookielib
import urllib2
from getpass import getpass
import sys
from urllib import urlencode
from getopt import getopt
username = None
passwd = None
message = None
number = None
def Usage():
	print '\t-h, --help:  View help'
	print '\t-u, --username: Username'
	print '\t-p, --password: Password'
	print '\t-n, --number: numbber to send the sms'
	print '\t-m, --message: Message to send'
	sys.exit(1)
opts, args = getopt(sys.argv[1:], 'u:p:m:n:h',["username=","password=","message=","number=","help"])
for o,v in opts:
	if o in ("-h", "--help"):
		Usage()
	elif o in ("-u", "--username"):
		username = v
		ask_username = False
	elif o in ("-p", "--password"):
		passwd = v
		ask_password = False
	elif o in ("-m", "--message"):
		message = v
		ask_message = False
	elif o in ("-n", "--number"):
		number = v
		ask_number = False
#Credentials taken here
if username is None: username = raw_input("Enter USERNAME: ")
if passwd is None: passwd = getpass()
if message is None: message = raw_input("Enter Message: ")
if number is None: number = raw_input("Enter Mobile number: ")
#Logging into the SMS Site
url = 'http://site24.way2sms.com/Login1.action?' 
data = 'username='+username+'&password='+passwd+'&Submit=Sign+in'
#Remember, Cookies are to be handled
cj = cookielib.CookieJar()
opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))
# To fool way2sms as if a Web browser is visiting the site
opener.addheaders = [('User-Agent','Mozilla/5.0 (X11; U; Linux x86_64; en-US; rv:1.9.1.3) Gecko/20091020 Ubuntu/9.10 (karmic) Firefox/3.5.3 GTB7.0')]
try:
	usock = opener.open(url, data)
except IOError:
	print "Check your internet connection11"
	sys.exit(1)
#urlencode performed.. Because it was done by the site as i checked through HTTP headers
message = urlencode({'message':message})
message = message[message.find("=")+1:]
jession_id = str(cj).split('~')[1].split(' ')[0]
#SMS sending
send_sms_url = 'http://site24.way2sms.com/smstoss.action?'
send_sms_data = 'ssaction=ss&Token='+jession_id+'&mobile='+number+'&message='+message+'&msgLen=136'
opener.addheaders = [('Referer', 'http://site25.way2sms.com/sendSMS?Token='+jession_id)]
try:
	sms_sent_page = opener.open(send_sms_url,send_sms_data)
except IOError:
	print "Check your internet connection( while sending sms)"
	sys.exit(1)
print "SMS sent!!!"
