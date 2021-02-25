#Servery time (mmm vscode colours look nice)

import smtplib, getpass, time, threading, os, socket, sys
from smtplib import SMTPException
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from Crypto.Cipher import AES

############################### Servery Fun stuff ##################################

data = None
decrypt = None
debug = True
class serverfun():
    def __init__(self, debug):
        self.debug = debug
        self.runtrack = 3
        self.verify_code = "KITT50Pontiac28Firebird58Trans70Am05541!"

    def startser(self):
        ciphered_data = ""
        key = ""
        iv = ""
        print("Starting server...")
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_address = ('localhost', 5010)
        sock.bind(server_address)
        sock.listen(1)
        verify = False
        decrypt_pass = ""
        while True:
            sock.listen(1)
            connection, client_address = sock.accept()  #all of this may be temporary because of multi user stuff
            while True:
                #global data
                length = connection.recv(16)     #this sets the buffer based on the length of the data the client is trying to send caution without this things dont work
                try:
                    length = int(length.decode())
                except:
                    print("This is not a number assuming 2000 as a last ditch effort \n", length)
                    length = 2000
                data = connection.recv(length)
                data = data.decode("utf-8").replace('\\\\','\\')
                try:                    
                    if data[1] == "a":               #recieve iv from data
                        ciphered_data = data[2:-1]
                    elif data[1] == "b":             #recieve key from data
                        key = data[2:-1]
                    elif data[1] == "c":
                        iv = data[2:-1]
                        iv = iv.encode()
                    elif data[1] == "d":
                        if data[1:3] == "d1":
                            username = data[3:-1]
                        elif data[1:3] == "d2":
                            password = data[3:-1]
                            l = Login(username, password)
                            l.verification()
                    elif data[1] == "e":
                        if data[1:3] == "e1":
                            username = data[3:-1]
                        elif data[1:3] == "e2":
                            password = data[3:-1]
                            l = Login(username, password)
                            l.accounts()
                        else:
                            print("Uhhh what?")


                finally:
                    self.encrypted_data = data
                    connection.sendall(data.encode())
                    break
            if ciphered_data != "" and key != "" and iv != "":
                print(ciphered_data, key, iv)
                #decryption(key, iv, ciphered_data)
                ciphered_data = ""
                key = ""
                iv = ""
                print("yay")

    def intermediary(self):        
        consock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_address = ('localhost', 1000)
        consock.connect(server_address)
        #send the decrypted data
        while True:
            consock.sendall(decrypt.decode())
            #no way of getting sent length yet so must assume 2000 if too slow will fix it
            consock.recv(2000)

################################ Login System #####################################

class Login:
    def __init__(self, username, password):
        self.username = username
        self.password = password

    def accounts(self):
        account_file = open("VPNaccounts.txt", 'a')
        details = f"{self.username}\n{self.password}\nc\n"
        account_file.write(details)
        account_file.close()
        Login(self.username,self.password).sending_email()
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
                elif login_details1 == account_array[int((int(count)/3)-1)] and word == "c":
                    print("New account. ")
            count += 1

        if accepted == False:
            print("You cannot log in. ")

    def sending_email(self):
        subject = "Someone is attempting to create a new VPN account. "
        mail_content = f"Username: {str(self.username)} \nPassword: {str(self.password)}" 
        sender_email = "_________________________________________________"
        sender_password = "______________________________________________"
        receiver_email = "_______________________________________________"        
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
        print("Mail sent (HOPEFULLY) ")


################################# Encryption ######################################

def encryption(data_to_encrypt):
    key = get_random_bytes(32) 
    cipher_encrypt = AES.new(key, AES.MODE_CFB)
    ciphered_data = cipher_encrypt.encrypt((data_to_encrypt.encode("utf-8")))
    return key, cipher_encrypt, ciphered_data

def decryption(key, cipher_encrypt, ciphered_data):
    cipher_decrypt = AES.new(key, AES.MODE_CFB, iv=cipher_encrypt)
    decrypted_data = (cipher_decrypt.decrypt(ciphered_data)).decode('utf-8')
    return decrypted_data    


if __name__ == '__main__':
    s = serverfun(debug)
    s.startser()
    print("yay?")
