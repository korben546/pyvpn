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
ciphered_data = []

#################################### Login ########################################

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

################################# Encryption ######################################

def encryption(data_to_encrypt):
    key = get_random_bytes(32) 
    cipher_encrypt = AES.new(key, AES.MODE_CFB)
    ciphered_data = cipher_encrypt.encrypt((data_to_encrypt.encode("utf-8")))
    return key, cipher_encrypt, ciphered_data

def decryption(key, cipher_encrypt, ciphered_data):
    cipher_decrypt = AES.new(key, AES.MODE_CFB, iv=cipher_encrypt.iv)
    decrypted_data = (cipher_decrypt.decrypt(ciphered_data)).decode('utf-8')
    return decrypted_data     

def encryptionProcess():
    data = str(input("Enter string to be encrypted: "))
    ciphered_data = encryption(data)  # ciphered_data[0 is the key, 1 is the iv thing, 2 is encrypted data]
    print("Encrypted data:", ciphered_data[2]) 
    decrypted_data = decryption(ciphered_data[0], ciphered_data[1], ciphered_data[2]) 
    print("Decrypted data:", decrypted_data)
    return ciphered_data

############################### Connect to server ##################################

class ServeryThings:
    def __init__(self, ip_address, hostname, ciphered_data):
        self.ip_address = ip_address
        self.hostname = hostname
        self.ciphered_data = ciphered_data

    def establishConnection(self):
        print("Test")           ### Cursed print statement
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_address = ('localhost', 5010)
        sock.connect(server_address)
        try:
            print("Trying")         ### Cursed print statement
            message = self.ciphered_data
            mystring = str(len(message))
            sock.sendall(mystring.encode('utf-8'))
            amount_received = 0
            amount_expected = len(message)
            while amount_received < amount_expected:
                sock.sendall(message)
                data = sock.recv(16)
                amount_received += len(data)
                print("received")
        finally:
            print("Closing socket.")
            sock.close()

    def debug(self):
        print(f'Hostname: {self.hostname}')
        print(f'IP Address: {self.ip_address}') 

###################################################################################

if __name__ == '__main__':
    login()
    ciphered_data = encryptionProcess()
    print(ciphered_data[2])     ### Cursed print statement
    s = ServeryThings(ip_address, hostname, ciphered_data[2])
    s.establishConnection()
