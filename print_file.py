#!/usr/bin/env python3

import smtplib
from email.mime.multipart import MIMEMultipart 
from email.mime.text import MIMEText 
from email.mime.base import MIMEBase 
from email import encoders
from tkinter import Tk 
from tkinter.filedialog import askopenfilename
from getpass import getpass

PWD = getpass("Please enter your email password: ")

FROM = "trin3399@OX.AC.UK"
TO = "followmeprint@materials.ox.ac.uk"

# creates SMTP session 
s = smtplib.SMTP('outlook.office365.com', 587)
  
# start TLS for security 
s.ehlo()
s.starttls() 
  
# Authentication 

while True : 
    try : 
        s.login(FROM, PWD)
        break
    except : 
        print("Problem logging in. Try again.")
        PWD = input("Please enter your email password: ")

'''
try : 
    s.login(FROM, PWD) 
except : 
    print("Problem logging in. Try again. ")
'''   

# Graphically select file  
Tk().withdraw()

filename = askopenfilename(title = "Select files to send", filetypes = [(".docx", ".pdf")], initialdir = '~/')

checker = input("Sending {} to print. Press enter to send to print, anything else to exit.".format(filename))

if checker == '' : 
    pass
else : 
    print("Exiting")
    exit()

# instance of MIMEMultipart 
msg = MIMEMultipart() 
  
# set addresses etc
msg['From'] = FROM
msg['To'] = TO 
msg['Subject'] = "Attachment for printing"
  
# open the file to be sent  
attachment = open(filename, "rb") 
  
# instance of MIMEBase and named as p 
p = MIMEBase('application', 'octet-stream') 
  
# To change the payload into encoded form 
p.set_payload((attachment).read()) 
  
# encode into base64 
encoders.encode_base64(p) 
   
p.add_header('Content-Disposition', "attachment; filename = {}".format(filename)) 
  
# attach the instance 'p' to instance 'msg' 
msg.attach(p) 
  

# Converts the Multipart msg into a string 
text = msg.as_string() 
  
# sending the mail 
try : 
    s.sendmail(FROM, TO, text)
    print('Email sent.')
except : 
    print('Error sending mail.')  

# terminating the session 
s.quit() 





