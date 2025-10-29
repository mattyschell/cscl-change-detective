import sys
import datetime
import glob
import os
import smtplib
import socket
from email.message import EmailMessage


def getlogfile(logdir
              ,logtype):

    # ex get most recent logtype* log from a log directory

    list_of_logs = glob.glob(os.path.join(logdir
                                         ,'*{0}*.log'.format(logtype)))

    latest_log = max(list_of_logs, key=os.path.getctime)

    with open(os.path.join(logdir, latest_log), 'r') as file:
        loglines = file.read()

    return loglines

def main():

    pnotification   = sys.argv[1]
    pemails         = sys.argv[2]
    plogtype        = sys.argv[3] # ex 'HistoricDistrict' 'NOLOG'
    plogdir         = sys.argv[4]
    pemailfrom      = sys.argv[5]
    psmtpfrom       = sys.argv[6]
    
    msg = EmailMessage()

    # notification is like "a very important thing"

    content  = 'Completed {0} '.format(pnotification)
    msg['Subject'] = content
    content += 'at {0} {1}'.format(datetime.datetime.now()
                                  ,os.linesep)

    # NOLOG input on failures 
    if plogtype != 'NOLOG':
        content += '\n' + getlogfile(plogdir
                                    ,plogtype)   
    
    smtp = smtplib.SMTP(psmtpfrom)  
    msg['From'] = pemailfrom
    # this is headers only 
    # if a string is passed to sendmail it is treated as a list with one element!
    msg['To'] = pemails

    if 'WARNING' in content:
        msg.set_content(content) 
    else:
        msg.set_content('No evidence to report') 
        
    try:
        smtp.sendmail(msg['From']
                        ,msg['To'].split(",")
                        ,msg.as_string())
    except smtplib.SMTPRecipientsRefused as e:
        print("\n notify.py - Email not sent: relaying denied.")
        print(" notify.py - This is expected from desktop environments.\n")

    smtp.quit()


if __name__ == "__main__":
    main()

