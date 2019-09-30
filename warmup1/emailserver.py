# import the smtplib module. It should be included in Python by default
import smtplib


sender = 'ubuntu@hw0.cloud.compas.cs.stonybrook.edu'

# receivers = ['stuy.rong.yu@gmail.com']

def sendEmail(key_string, reciever):
   message ="""From: Ubuntuu <ubuntu@hw0.cloud.compas.cs.stonybrook.edu>
To: {} <{}>
Subject: Email Confirmation Key
   
Please work.
Please work.
validation key: <{}>
   """.format(reciever, reciever, key_string)
   receivers = [reciever]
   # print(message)
   try:
      smtpObj = smtplib.SMTP('localhost')
      smtpObj.sendmail(sender, receivers, message)         
      print ("Successfully sent email")
   except Exception as e:
      print(e)
      print ("Error: unable to send email")
      
# sendEmail("abracadabra", "stuy.rong.yu@gmail.com")
