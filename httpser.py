#https tunnel thing can only take 1 connection atm as far as I know
import SocketServer, SimpleHTTPServer ,urllib

PORT = 1000

class Getttps(SimpleHTTPServer.SimpleHTTPRequestHandler):
    def do_GET(self):
        store = open("udat.dat", "w+")
        #encrypt this but not yet
        file.write(str(self.path) + " ip: " + str(self.client_address))
    	url=self.path[1:]
    	self.send_response(200)
    	self.end_headers()
        self.copyfile(urllib.urlopen(url), self.wfile)


httpd = SocketServer.ForkingTCPServer(('', PORT), Getttps)
print("Taking requests at " + str(PORT))
httpd.serve_forever()



