### Group VPN project attempt
### Creators:
### - MrCraftyCreeper
### - MarvelousMatt04
### - LostLuke

import smtplib, getpass, time, threading, os, socket
from smtplib import SMTPException                   ## Dis is here incase we add email to client side
from email.mime.multipart import MIMEMultipart      ## Might be helpful IDK
from email.mime.text import MIMEText
from Crypto.Random import get_random_bytes          ## Important for generating a key
from Crypto.Protocol.KDF import PBKDF2

hostname = socket.gethostname()                     ## Gets hostname
ip_address = socket.gethostbyname(hostname)         ## Gets user's IP address


class ServeryThings:
    def __init__(self, ip_address, hostname):
        self.ip_address = ip_address
        self.hostname = hostname

    def encryption(self):
        salt = get_random_bytes(32)                 ## A salt is random data that is used as an additional input to a one-way function that "hashes" data.
        salt = str(salt)                            ## Converts to string, idk if necessary but oh well
        print(salt)
        password = 'password123'                    ## Password or some shit idk
        key = PBKDF2(password, salt, dkLen=32)      ## Your key that you can encrypt with

    def debug(self):
        print(f'Hostname: {self.hostname}')
        print(f'IP Address: {self.ip_address}')


class Login:
    def __init__(self, username, password):
        self.username = username
        self.password = password

    def createNew(self):
        for i in range(4):
            newAccVerif = input("Please enter the verification code to create a new account: ")
            if newAccVerif == "0000" and (4-i) > 0:
                self.username = input("Enter username: ")
                self.password = input("Enter password: ")
                self.usersEmail = input("Please enter your email so we can contact you when/if your account is accepted: ")
                ### Send over to the server
                time.sleep(2)
                print("You account has been created successfully. Please wait for a response confirming whether you login has been accepted or denied access. ")
                break
            elif newAccVerif != "0000" and (3-i) > 0:
                print(f'You have {3-i} attempts remaining. ')
            else:
                print("You have no attempts remaining.")
                time.sleep(2)
                quit()

    def verification(self):
        ### Send to server and check against pre-existing accounts
        ### Receive whether account is accepted
        accepted = True
        if accepted == True:
            print("You have logged in successfully. ")
        else:
            print("Your login detailes are invalid. ")
            quit()
        

def login():
    isUserNew = input("If you do not have a pre-existing account please enter 'Create new'. ").lower()
    if isUserNew == "create new":
        l = Login(username="",password="")
        l.createNew()
    else:
        username = input("Enter your username: ")
        password = input("Enter your password: ")
        l = Login(username,password)
        l.verification()

def main():
    login()
    s = ServeryThings(ip_address, hostname)
    s.encryption()

if __name__ == '__main__':
    main()
