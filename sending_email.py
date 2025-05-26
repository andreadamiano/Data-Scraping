import smtplib #to esttablish a connection with a SMTP server 
from email.mime.text import MIMEText  #creates a message object


#create a message 
msg = MIMEText("scusa , ti amo <3")
msg['Subject'] = 'An email from python'
msg['From'] = 'decong.ad@gmail.com'
msg['To'] = 'janellemorales003@gmail.com'

#smtp server credentials 
smtp_server = "smtp.gmail.com"
smtp_port = 587
username = 'decong.ad@gmail.com'  
password = input()  #use app password to bypass 2FA

#connnect to the server and send email
with smtplib.SMTP(smtp_server, smtp_port) as server:
    server.starttls()  # Enable encryption
    server.login(username, password)
    server.send_message(msg)
print("Email sent successfully!")