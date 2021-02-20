### Group VPN project attempt
### Creators:
### - MrCraftyCreeper
### - MarvelousMatt04

import getpass, time, threading, os, socket         ## All modules that might be necessary
from Crypto.Random import get_random_bytes          ## Important for generating a key
from Crypto.Cipher import AES

hostname = socket.gethostname()                     ## Gets hostname
ip_address = socket.gethostbyname(hostname)         ## Gets user's IP address

class ServeryThings:
    def __init__(self, ip_address, hostname):
        self.ip_address = ip_address
        self.hostname = hostname

### Encryption and decryption can both work on client or server side, however need to send the (currently)
### global variables across. These variables are: key, cipher_encrypt and ciphered_data. Once this is done they
### should no longer require the self parameter in front of them to function properly. That's probably a
### really poor description lol

    def encryption(self):
        self.key = get_random_bytes(32)             ## Creates a key - Needs to be sent to server
        data_to_encrypt = "test string"             ## String that gets encrypted
        
        data = data_to_encrypt.encode("utf-8")
        self.cipher_encrypt = AES.new(self.key, AES.MODE_CFB)   ## This needs to be sent too
        ciphered_bytes = self.cipher_encrypt.encrypt(data)
        self.ciphered_data = ciphered_bytes                     ## And this
        print("The encrypted message is:", self.ciphered_data)  ## Final encrypted message

    def decryption(self):
        # key = "_____" - The key that is sent from client
        # ciphered_data = "______" - Again, this is sent from client
        iv = self.cipher_encrypt.iv       ## Currently uses global variable but needs to use the one sent
        cipher_decrypt = AES.new(self.key, AES.MODE_CFB, iv=iv)
        deciphered_bytes = cipher_decrypt.decrypt(self.ciphered_data)
        decrypted_data = deciphered_bytes.decode('utf-8')
        print("The decrypted message is:", decrypted_data)      ## Decrypted message

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
    s.decryption()

if __name__ == '__main__':
    main()
