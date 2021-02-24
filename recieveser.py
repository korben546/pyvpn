#Servery time (mmm vscode colours look nice)
import socket,sys
from Crypto.Cipher import AES
data = None
decrypt = None
debug = True
class serverfun():
    def __init__(self):
        self.debug = debug
        self.runtrack = 3
        self.verify_code = "KITT50Pontiac28Firebird58Trans70Am05541!"
    def startser(self):
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_address = ('localhost', 1010)
        sock.bind(server_address)
        sock.listen(1)
        verify = False
        decrypt_pass = ""
        while True:
            connection, client_address = sock.accept()  #all of this may be temporary because of multi user stuff
            while True:
                #global data
                length = connection.recv(16)     #this sets the buffer based on the length of the data the client is trying to send caution without this things dont work
                try:
                    length = int(length.decode())
                except:
                    print("This is not a number assuming 2000 as a last ditch effort \n" + length.decode())  #Would assert but that doesnt work here plus error handling for debugging
                    length = 2000
                data = connection.recv(length)
                data = data.decode()
                if self.runtrack != 4:
                    self.runtrack += 1
                if self.runtrack = 1:               #recieve iv from data
                    self.cipher_encrypt = data
                elif self.runtrack = 2:             #recieve key from data
                    self.key = data
                elif self.runtrack = 3:
                    #verification 
                    encryption(self)
                    connection.sendall(ciphered_data.encode())
                    data = connection.recv(len(self.verify_code))
                    assert data.decode() != self.verify_code, "You failed the verification now the server is down happy \n well since we cant do verification with multiple ip's just yet crashing is ok"
                else:
                    self.encrypted_data = data
                    decryption(self)
                
                

                #decryption goes here
                #pass gobal variable to intermediary
    def encryption(self):  #this will either go in a seperate class or in another file with decrypt
        #key = get_random_bytes(32) 
        #cipher_encrypt = AES.new(key, AES.MODE_CFB)
        self.verify_code = data_to_encrypt.encode("utf-8")
        iv = self.cipher_encrypt
        ciphered_data = cipher_encrypt.encrypt(data)
        if self.debug = True:
            print("Encrypted:", ciphered_data)
        return ciphered_data

    def decryption(self):
        # key = "_____" - The key that is sent from client
        # ciphered_data = "______" - Again, this is sent from client
        iv = self.cipher_encrypt      ## Currently uses global variable but needs to use the one sent
        cipher_decrypt = AES.new(self.key, AES.MODE_CFB, iv=iv)
        deciphered_bytes = cipher_decrypt.decrypt(self.encrypted_data)
        self.decrypted_data = deciphered_bytes.decode('utf-8')
        if self.debug == True:
            print("The decrypted message is:", decrypted_data)
        
    def intermediary(self):                 # prevents a feedback loop on the socket and doesnt force me to add a header
        consock = socket.socket(socket.AF_INET, socket.SOCK_STREAM) #may have header soon to allow multiple users
        server_address = ('localhost', 1000)
        consock.connect(server_address)
        #send the decrypted data
        while True:
            consock.sendall(self.decrypted_data.encode())
            #no way of getting sent length yet so must assume 2000 if too slow will fix it
            consock.recv(2000)

if __name__ == '__main__':
    s = serverfun(debug)
    s.startser()
    print("yay?")   #nay?
