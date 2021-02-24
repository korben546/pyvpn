### Servery things

import smtplib, getpass, time, threading, os
from smtplib import SMTPException
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

class Login:
    def __init__(self, username, password):
        self.username = username
        self.password = password

    def accounts(self):
        account_file = open("VPNaccounts.txt", 'a')
        details = f"{self.username}\n{self.password}\nc\n"
        account_file.write(details)
        account_file.close()
        print("New account created")

    def verification(self):
        account_array = []
        login_details = []
        login_details1 = []
        count = 1
        accepted = False
        login_details1.append(self.username)
        login_details1.append(self.password)
        f = open("VPNaccounts.txt", 'r')
        for word in f:
            word = word[:-1]
            if count % 3 != 0:
                login_details.append(word)
            else:
                account_array.append(login_details)
                login_details = []
                if login_details1 == account_array[int((int(count)/3)-1)] and word == "a":
                    print("Account is authorised. ")
                    print("Logged in")
                    # Allow client to continue
                    accepted = True
                    break
                elif login_details1 == account_array[int((int(count)/3)-1)] and word == "b":
                    print("Account is blocked. ")
                    break
                elif word == "c":
                    print("New account. ")
            count += 1

        if accepted == False:
            print("You cannot log in. ")

    def sending_email(self):
        subject = "Someone is attempting to create a new VPN account. "
        mail_content = f"Username: {str(self.username)} \nPassword: {str(self.password)}" 
        sender_email = ""
        sender_password = ""
        receiver_email = ""        
        message = MIMEMultipart()
        message['From'] = sender_email
        message['To'] = receiver_email
        message['Subject'] = subject
        message.attach(MIMEText(mail_content, 'plain'))
        session = smtplib.SMTP('smtp.gmail.com', 587)
        session.starttls()
        session.login(sender_email, sender_password)
        text = message.as_string()
        session.sendmail(sender_email, receiver_email, text)
        session.quit()
        time.sleep(2)
        print("Mail sent (HOPEFULLY) ")

def main():
    new_account = False
    l = Login("Me", "Test2")
    if new_account == True:
        l.accounts()
        l.sending_email()
    else:
        l.verification()

if __name__ == '__main__':
    main()
