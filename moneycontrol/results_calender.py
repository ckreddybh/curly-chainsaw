from bs4 import BeautifulSoup
import urllib
import warnings
import datetime as dt
from datetime import datetime
from sendMail import sendMail
date_format = "%d-%b-%Y"
company_results_hash = {}
nextPage = None
url = "http://www.moneycontrol.com/earnings/"
while True:
	try:
		if nextPage :
			url1 = url+nextPage
		else:
			url1 = url+"results-calender.html"
		print url1
		fh = urllib.urlopen(url1)
	except Exception as e:
		warnings.warn(e)
	data=fh.read()
	soup = BeautifulSoup(data)
	try:
		nextPage = soup.find('a',class_='nxt').get("href")
	except Exception :
		nextPage = None
	for tr in soup.find_all('tr'):
		try:
			companyName = tr.find('a',class_='bl_12').get_text(strip=True)
			resultDate = tr.find('p',class_='PL30').get_text(strip=True)
		except AttributeError:
			pass
		else:
			company_results_hash[companyName.lower()] = resultDate


	if not nextPage:
		break

today = dt.date.today()
msg = ""
subject = "Daily Results Report ["+today.strftime("%d-%b-%Y")+"]"
print "subject :", subject
final_company = {}
with open("companies_to_process.txt","r") as com:
	for company in com:
		company = company.lower().strip()
		print company
		date = company_results_hash.get(company)
		print date
		if date:
			resultDate = datetime.strptime(date,date_format).date()
			print resultDate
			diff = (resultDate - today).days
			if diff >= 0:
				final_company[company+"|"+date] = diff


for key,days in sorted(final_company.items(), key=lambda x: x[1]):
	value = key.split("|")
	company = value[0]
	date = value[1]
	msg = msg+"<tr><td>"+company+"</td><td><b>"+str(days)+" days to go</b></td><td>"+date+"</td></tr>"

if msg :
	msg = "<table border=\"2\"><body><tr><th><b>Company Name</th><th>Days Left</th><th>Result Date</th></b></tr>"+msg+"</body></table>"
else :
	msg = "<body><b><i>No results with in a week</i></b></body>\n"


print "msg ", msg

sendMail("ckreddybh@gmail.com","chaitu949@gmail.com, setmodevamsi1117@gmail.com, ayyappa.konala@gmail.com",subject,msg)

print "mail set ";
