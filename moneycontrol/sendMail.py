#!/usr/bin/env python

import smtplib

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

# me == my email address
# you == recipient's email address
me = "ckreddybh@gmail.com"
to = "chaitu949@gmail.com"
def sendMail(me,to,subject,message):

# Create message container - the correct MIME type is multipart/alternative.
	msg = MIMEMultipart('alternative')
	msg['Subject'] = subject
	msg['From'] = me
	msg['To'] = to
	'''
# Create the body of the message (a plain-text and an HTML version).
	text = "Hi!\nHow are you?\nHere is the link you wanted:\nhttps://www.python.org"
	html = """\
		<html>
		<head></head>
		<body>
		<p>Hi!<br>
		How are you?<br>
		Here is the <a href="https://www.python.org">link</a> you wanted.
		</p>
		</body>
		</html>
		"""
		'''
# Record the MIME types of both parts - text/plain and text/html.
#	part1 = MIMEText(message, 'plain')
	part2 = MIMEText(message, 'html')

# Attach parts into message container.
# According to RFC 2046, the last part of a multipart message, in this case
# the HTML message, is best and preferred.
#	msg.attach(part1)
	msg.attach(part2)

# Send the message via local SMTP server.
	s = smtplib.SMTP('localhost')
# sendmail function takes 3 arguments: sender's address, recipient's address
# and message to send - here it is sent as one string.
	s.sendmail(me, to, msg.as_string())
	s.quit()
if __name__ == "__main__":
	sendMail(me,to,"TEST",'<table border="2"><body><tr><th><b>Company Name</th><th>Days Left</th><th>Result Date</th></b></tr><tr><td>tata steel</td><td><b>33 days to go</b></td><td>04-Feb-2016</td></tr><tr><td>rane holdings</td><td><b>38 days to go</b></td><td>09-Feb-2016</td></tr></body></table>')
