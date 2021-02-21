### Group VPN project attempt
### Current creators:
### - MrCraftyCreeper
### - MarvelousMatt04

# ===== Client side ===== #

import getpass, time, threading, os, socket, sys
from Crypto.Random import get_random_bytes
from Crypto.Cipher import AES

hostname = socket.gethostname()
ip_address = socket.gethostbyname(hostname)

###################################################################################

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
                time.sleep(1)
                print("Loading...")
                time.sleep(1)
                print("You account has been created successfully. Please wait for a response confirming whether your account has been accepted or denied access. ")
                quit()
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

###################################################################################

class EncryptionyThings:
    def __init__(self, ip_address, hostname):
        self.ip_address = ip_address
        self.hostname = hostname

    def encryption(self, data_to_encrypt):
        key = get_random_bytes(32) 
        cipher_encrypt = AES.new(key, AES.MODE_CFB)
        data = data_to_encrypt.encode("utf-8")
        ciphered_data = cipher_encrypt.encrypt(data)
        print("Encrypted:", ciphered_data)
        return cipher_encrypt, ciphered_data

    def decryption(self, cipher_encrypt, ciphered_data):
        iv = cipher_encrypt.iv
        cipher_decrypt = AES.new(key, AES.MODE_CFB, iv=iv)
        deciphered_bytes = cipher_decrypt.decrypt(ciphered_data)
        decrypted_data = deciphered_bytes.decode('utf-8')
        return decrypted_data       

###################################################################################

class ServeryThings:
    def __init__(self, ip_address, hostname, ciphered_data):
        self.ip_address = ip_address
        self.hostname = hostname
        self.ciphered_data = ciphered_data

    def establishConnection(self):
        pass

    def sendingData(self):
        pass

    def debug(self):
        print(f'Hostname: {self.hostname}')
        print(f'IP Address: {self.ip_address}') 

###################################################################################

def importantFunctionYes():
    data = str(input("Enter string to be encrypted: "))
    e = EncryptionyThings(ip_address, hostname)
    ciphered_data = e.encryption(data)
    cipher_encrypt = ciphered_data[0]
    encrypted_data = ciphered_data[1]
    # Send ciphered_data to server
    # receive encrypted packets
    print("Decrypted data:",e.decryption(cipher_encrypt, encrypted_data))


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


if __name__ == '__main__':
    login()
    importantFunctionYes()
