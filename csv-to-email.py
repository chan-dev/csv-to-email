# To add a new cell, type '# %%'
# To add a new markdown cell, type '# %% [markdown]'
# %%
import sys
import pandas as pd
import smtplib, ssl
import mimetypes
from getpass import getpass
from email.mime.multipart import MIMEMultipart
from email import encoders
from email.message import Message
from email.mime.audio import MIMEAudio
from email.mime.base import MIMEBase
from email.mime.image import MIMEImage
from email.mime.text import MIMEText


# %%
drinks = pd.read_csv('http://bit.ly/drinksbycountry')
drinks.head()


# %%
# Approach #1 on deleting column:
del drinks['continent']


# %%
# Approach #2 on deleting column:
drinks.drop(columns=['total_litres_of_pure_alcohol'], inplace=True)


# %%
# save the transformed dataframe to a new csv file
fileToSend = "attachment.csv"
csv_data = drinks.to_csv(fileToSend, index=False)


# %%
emailfrom = "app.tester.031490@gmail.com"
emailto = "chan.dev.031490@gmail.com"
username = "app.tester.031490@gmail.com"
port = 465  # For SSL
password = getpass("Type your password and press enter: ")

context = ssl.create_default_context()


# %%
# Setup message
msg = MIMEMultipart()
msg["From"] = emailfrom
msg["To"] = emailto
msg["Subject"] = "This is an email from a python script"
msg.preamble = "Great"

content = f"""
This is a sample email content
"""

msg.attach(MIMEText(content, "plain"))


# %%
ctype, encoding = mimetypes.guess_type(fileToSend)
if ctype is None or encoding is not None:
    ctype = "application/octet-stream"

print(ctype)
print(encoding)


# %%
maintype, subtype = ctype.split("/", 1)

if maintype == "text":
    fp = open(fileToSend)
    # Note: we should handle calculating the charset
    attachment = MIMEText(fp.read(), _subtype=subtype)
    fp.close()
elif maintype == "image":
    fp = open(fileToSend, "rb")
    attachment = MIMEImage(fp.read(), _subtype=subtype)
    fp.close()
elif maintype == "audio":
    fp = open(fileToSend, "rb")
    attachment = MIMEAudio(fp.read(), _subtype=subtype)
    fp.close()
else:
    fp = open(fileToSend, "rb")
    # should we replace it with MIMEApplication?
    attachment = MIMEBase(maintype, subtype)
    attachment.set_payload(fp.read())
    fp.close()
    encoders.encode_base64(attachment)
attachment.add_header("Content-Disposition", "attachment", filename=fileToSend)
msg.attach(attachment)


# %%
with smtplib.SMTP_SSL("smtp.gmail.com", port, context=context) as server:
    server.login(username,password)
    server.sendmail(emailfrom, emailto, msg.as_string())
    print('Email sent')


