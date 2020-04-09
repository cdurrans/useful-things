#will include how to email using google later

import smtplib

def send_mail(email, password,message):
    server = smtplib.SMTP("smtp-relay-....", portNumber.....)
    server.starttls()
    server.login(email,password)
    server.sendmail(email, email, message)
    server.quit()

send_mail('myemail','myPassword','myMessage')