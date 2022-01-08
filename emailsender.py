import requests # http requests
from bs4 import BeautifulSoup # web scraping
import smtplib # send the mail
from email.mime.multipart import MIMEMultipart # email body
from email.mime.text import  MIMEText # email body
import datetime # system date and time manipulation

now = datetime.datetime.now()

#email content placeholder
content = ""

def extract_news(url):
    print("Extracting Hacker News Stories")
    cnt = ""
    cnt += ("<b> HN Top Stories: </b>\n" + "<br>" + "-"*50 + "<br>" )
    response = requests.get(url)
    content = response.content
    soup = BeautifulSoup(content, "html.parser")
    for i, tag in enumerate(soup.find_all("td", attrs={"class": "title", "valign":""})):
        cnt += ((str(i+1) + " :: " + tag.text + "\n" +  "<br>") if tag.text != "More" else "")
    return(cnt)

cnt = extract_news("https://news.ycombinator.com/")
content += cnt
content += ("<br> ----------- <br>")
content += ("<br><br> End of Message")

print("Composing mail...")

# E-mail Authentication
# Update e-mail details

SERVER = "smtp.gmail.com" # standard gmail smtp server
PORT = 587 # standard gmail port number
FROM = "[sender]@gmail.com"
TO = "[recipient]@domain.de"
PASS = "********"


# Create a text/plain message

msg = MIMEMultipart()

# Creating a dynamic Subject line:
msg["Subject"] = "Top Hacker News [Automated E-Mail]" + " " + str(now.day) + " " + str(now.month) + " " + str(now.year)

msg["From"] = FROM
msg["To"] = TO

msg.attach(MIMEText(content, "html"))

print("Initiating Server")

server = smtplib.SMTP(SERVER, PORT) # telling the program where the mail is going to be sent from
server.set_debuglevel(1) # if there is an error, setting the debug level to 1 will show the error message
server.ehlo() # initiates the transaction with the Gmail server
server.starttls() # starts TLS connection which is a secured connection
server.login(FROM, PASS) # enters login details
server.sendmail(FROM, TO, msg.as_string()) # specifies that the content of msg is sent as a string

print("EMail sent")

server.quit()
