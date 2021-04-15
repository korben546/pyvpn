import getpass, time, threading, os, socket, sys
from Crypto.Random import get_random_bytes
from Crypto.Cipher import AES

def login():
    isUserNew = input("Type 'Create new' if you don't have an account. ").lower()
    if isUserNew == "create new":
        l = Login(username="",password="")
        l.createNew()
    else:
        username = "d1" + input("Enter your username: ")
        password = "d2" + input("Enter your password: ")
        s = ServeryThings(username)
        s.sendThings()                             # Sends over username
        time.sleep(0.1)
        s = ServeryThings(password)
        s.sendThings()                             # Sends over password
        l = Login(username,password)
        accepted = s.activateAcc()
        l.verification(accepted)

#################################################################################################################################

class Login:
    def __init__(self, username, password):
        self.username = username
        self.password = password

    def createNew(self):
        hostname = socket.gethostname()
        ip_address = socket.gethostbyname(hostname)
        for i in range(4):
            newAccVerif = input("Please enter the verification code to create a new account: ")
            if newAccVerif == "0000" and (4-i) > 0:
                username = input("Enter username: ")
                password = input("Enter password: ")
                usersEmail = input("Please enter your email so we can contact you when/if your account is accepted: ")
                username = "e1" + str(username)
                password = "e2" + str(password)
                s = ServeryThings(username)
                s.sendThings()
                time.sleep(0.1)
                s = ServeryThings(password)
                s.sendThings()
                print("You account has been created successfully. ")
                time.sleep(5)
                quit()
            elif newAccVerif != "0000" and (3-i) > 0:
                print(f'You have {3-i} attempts remaining. ')
            else:
                print("You have no attempts remaining.")
                time.sleep(2)
                quit()

    def verification(self, accepted):
        if accepted == True:
            print("You have logged in successfully. ")
        else:
            print("Your login detailes are invalid. ")

#################################################################################################################################

class ServeryThings:
    def __init__(self, data):
        self.data = data

    def sendThings(self):
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_address = ('localhost', 5010)
        sock.connect(server_address)
        time.sleep(0.1)
        try:
            sendingData = str(self.data)
            encodedLength = int(len(repr(sendingData).encode()))
            sock.sendall(repr(encodedLength).encode())
            amount_received = 0
            while amount_received < len(sendingData):
                sock.sendall(repr(sendingData).encode())
                receivedMessage = sock.recv(16)
                amount_received += len(receivedMessage)
        finally:
            sock.close()

    def activateAcc(self):
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_address = ('localhost', 5011)
        sock.bind(server_address)
        while True:
            sock.listen(1)
            connection, client_address = sock.accept()
            while True:
                length = connection.recv(16)
                try:
                    length = int(length)
                except:
                    length = 1024
                data = connection.recv(length)
                data = data.decode().replace('\\\\','\\')
                try:
                    if data[1] == "a":
                        accepted = True
                    elif data[1] == "b":
                        accepted = False
                    elif data[1] == "c":
                        accepted = False
                        print("New account. ")
                finally:
                    connection.sendall(data.encode())
                    breakloop = True
                    break
            if breakloop == True:
                break
        return accepted

#################################################################################################################################

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

#################################################################################################################################

if __name__ == '__main__':
    login()