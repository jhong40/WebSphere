import re, datetime
import smtplib
import sys

logfile="atlassian-jira.log"
print(logfile)

f = open(logfile, "r")
lines = f.readlines()
pre = ""  #pre line

count=0
eflag=0
terr=0

todaylines=[]
tc=0
msg=""

d0=datetime.date.today()
yy=d0.strftime("%Y")
dd=d0.strftime("%Y")+"-"+d0.strftime("%m")+"-"+d0.strftime("%d")
#print(dd)
#dstr="2020-10-06"
dstr=dd
for txt in lines:  #Extract lines for today
  pattern = '^(\d{4}-\d{2}-\d{2}) (\d{2}:\d{2}:\d{2},\d{3} .*)' 
  matchObj = re.match(pattern, txt)  
  if matchObj:
    mystr=matchObj.group(1)
    if mystr==dstr:
      tc=tc+1
  if tc>0:
    todaylines.append(txt)	
  
for txt in todaylines:
    pattern = '^(\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2},\d{3} .*)'
    #pattern = '^(2020-10-06 \d{2}:\d{2}:\d{2},\d{3} .*)'	
    match = re.search(pattern, txt)

    if match:  #regular line
      pre=txt
      eflag=0		
      count=0   
    else:  # err line
      #print(txt)
      if count<5:
        count=count+1	  
        if eflag==0:
          msg=msg+"\n\n"+pre+txt		
          eflag=1	
          terr=terr+1		  
        else:		  
          msg=msg+txt


msg=str(terr)+" Errs today\n"+msg	  
sender = 'me@blah.com'
receivers = ['George.Blah@blah.com','P@blah.com']

message = f"""From: George Tesla <george.tesla@blah.com>
To: george.tesla@blah.com
Subject: jira err {dstr}

    {msg}

"""

smtpObj = smtplib.SMTP('mailservert.com')
smtpObj.sendmail(sender, receivers, message)             
