#Servery time (mmm vscode colours look nice)
import socket,sys
data = None
decrypt = None
def startser():
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_address = ('localhost', 1010)
    sock.bind(server_address)
    sock.listen(1)
    verify = False
    decrypt_pass = ""
    while True:
        connection, client_address = sock.accept()
        while True:
            global data
            length = connection.recv(6)
            length = int(length.decode())
            data = connection.recv(length)
            data = data.decode()
            #decryption goes here
            #pass gobal variable to intermediary
def intermediary():
    consock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_address = ('localhost', 1000)
    consock.connect(server_address)
    #send the decrypted data
    while True:
        consock.sendall(decrypt.decode())
        #no way of getting sent length so must assume 2000 if too slow will fix it
        consock.recv(2000)
