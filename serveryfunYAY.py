#Servery time (mmm vscode colours look nice)

import socket,sys
from Crypto.Cipher import AES

data = None
decrypt = None
debug = True

class serverfun():
    def __init__(self, debug):
        self.debug = debug
        self.runtrack = 3
        self.verify_code = "KITT50Pontiac28Firebird58Trans70Am05541!"

    def startser(self):
        print("Starting")
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_address = ('localhost', 5010)
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        sock.bind(server_address)
        sock.listen(1)
        verify = False
        decrypt_pass = ""
        while True:
            print("yay")
            connection, client_address = sock.accept()
            while True:
                global data
                print("yayyyy")
                length = connection.recv(16)     #this sets the buffer based on the length of the data the client is trying to send caution without this things dont work
                print("Hmmmm")
                try:
                    print("trying len thing")
                    length = int(length.decode())
                except:
                    print("This is not a number assuming zero as a last ditch effort \n" + length.decode())  #Would assert but that doesnt work here plus error handling for debugging
                    length = 0
                data = connection.recv(length)
                print("Hmmmmmmmm")
                data = data.decode()
                self.runtrack += 1
                if self.runtrack == 1:               #receive iv from data
                    self.cipher_encrypt = data[2]
                elif self.runtrack == 2:             #receive key from data
                    self.key = data[0]
                elif self.runtrack == 3:
                    #verification 
                    encryption(self)
                    connection.sendall(ciphered_data.encode())
                    data = connection.recv(len(self.verify_code))
                    assert data.decode() != self.verify_code, "You failed the verification tough now the server is down happy \n well since we cant do verification with multiple ip's just yet crashing is ok"

                #decryption goes here
                #pass gobal variable to intermediary

        
    def intermediary(self):                 # prevents a feedback loop on the socket and doesnt force me to add a header
        consock = socket.socket(socket.AF_INET, socket.SOCK_STREAM) #may have header soon to allow multiple users
        server_address = ('localhost', 1000)
        consock.connect(server_address)
        #send the decrypted data
        while True:
            consock.sendall(decrypt.decode())
            #no way of getting sent length yet so must assume 2000 if too slow will fix it
            consock.recv(2000)

def encryption(data_to_encrypt):
    key = get_random_bytes(32) 
    cipher_encrypt = AES.new(key, AES.MODE_CFB)
    ciphered_data = cipher_encrypt.encrypt((data_to_encrypt.encode("utf-8")))
    return key, cipher_encrypt, ciphered_data

def decryption(key, cipher_encrypt, ciphered_data):
    cipher_decrypt = AES.new(key, AES.MODE_CFB, iv=cipher_encrypt.iv)
    decrypted_data = (cipher_decrypt.decrypt(ciphered_data)).decode('utf-8')
    return decrypted_data    

if __name__ == '__main__':
    s = serverfun(debug)
    s.startser()
    print("yay?")
