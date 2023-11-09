
import socket
from threading import Thread
class Client:
    def __init__(self, host, port, serverhost, serverport):
        self.host = host
        self.port = port
        self.serverhost = serverhost
        self.serverport = serverport
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.choicelist={}
        self.currentRequest=""
        #bind on new thread
        thread= Thread(target=self.bind)
        thread.start()
        #connect to server
        self.connectserver()
        #register to server
        self.reg()
        #start loop
        self.loop()
        thread.join()

    def loop(self):
        ####################################################################
        ##################  MAIN LOOP OF THE PROGRAM #######################
        ####################################################################
        while True:
            cmd=input("input command: ")
            cmd= cmd.lower()
            cmd= cmd.split(" ")
            if cmd[0]=="push":
                print("pushing")
                self.push(cmd[1])
                print("pushed")
                continue

            elif cmd[0]=="reg": #DO NOT USE, ALREADY REGISTERED WHEN CREATED, TAKE NO EFFECT
                print("registering")
                self.reg()
                print("registered")
                continue

            elif cmd[0]=="get":
                print("getting")
                self.get(cmd[1])
                print("got")
 
            elif cmd[0]=="fetch":
                self.fetch(self.choicelist[int(cmd[1])])
                print("GOT FILE")
                continue

            elif cmd=="exit":
                break

        


    ####################################################################
    ################   CONNECT TO SERVER AND BIND    ###################
    ####################################################################
    def connectserver(self):
        self.connectsocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.connectsocket.connect((self.serverhost, self.serverport))

    def bind(self):
        self.socket.bind((self.host, self.port))
        self.socket.listen(5)
        print("Listening on port %s" % self.port)
        while True:
            c, addr = self.socket.accept()
            thread2 = Thread(target=self.on_new_client, args=(c, addr))
            thread2.start()
        c.close()




    ####################################################################
    ##########   HANDLE FILE REQUEST FROM ANOTHER PEER      ############
    ####################################################################
    def on_new_client(self, client_socket, addr):
        print(f"New connection from: {addr}")
        print("Waiting for file name")
        data=client_socket.recv(2048).decode()
        if data:
            header, data=self.decodemsg(data)
            if header=="GET":
                print("Sending file" + data)
                self.sendfile(client_socket, data)
               


    def sendfile(self, client_socket, filename):
        file = open(filename, 'rb')
        dat = file.read(2048)
        while (dat):
            client_socket.send(dat)
            dat = file.read(2048)
        file.close()
        client_socket.close()
        print('Done sending')




    ####################################################################
    ##################   HANDLE CLI FROM USER ##########################
    ####################################################################

    def push(self, filename):
        #get list of peer from server
        msg="<PUSH> " + filename + " </PUSH>"
        self.connectsocket.send(msg.encode())
        #get response from server

    def reg(self):
        #register to server
        msg="<REG> "
        msg+= self.host+":"+str(self.port)
        msg+=" </REG>"
        self.connectsocket.send(msg.encode())
        print("Register with address: "+msg)
        #TODO: get respone from server

    def get(self, filename):
        #send request to server
        msg="<GET_F> " + filename + " </GET_F>"
        self.connectsocket.send(msg.encode())
        #TODO: get respone from server

        #get list from server
        list=self.connectsocket.recv(4096).decode()
        self.choicelist=list.split(";")
        print("List of user that have the file:")
        print(self.choicelist)
        self.currentRequest=filename
    
    def fetch(self, peer):
        peerHOST=peer.split(":")[0]
        peerPORT=int(peer.split(":")[1])
        print(peer)
        #new connect to peer
        newsocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        newsocket.connect((peerHOST, peerPORT))
        #send file name to peer
        msg="<GET> " + self.currentRequest + " </GET>"
        newsocket.send(msg.encode())

        #TODO: get respone from peer

        #get file from peer
        FILENAME=self.currentRequest.split(".")[0]+"_copy."+self.currentRequest.split(".")[1]
        file=open(FILENAME,"wb")
        data=newsocket.recv(2048)
        while data:
            file.write(data)
            data=newsocket.recv(2048)

        newsocket.close()
        file.close()
        return 0


    ####################################################################
    ##################     ULTILITY FUNCTION ()       ##################
    ####################################################################
    def decodemsg(self, data):
        data= data.split("> ",1)
        header=data[0].split("<",1)[1]
        print(header)
        msg=data[1].split(" <",1)[0]
        return header, msg
        
        
        
    ####################################################################
    ##################     MAIN FUNCTION ()       ######################
    ####################################################################

PORT = int(input("PORT to start: "))
host = "192.168.0.105"
serverhost = "192.168.0.105"
serverport = 8080
client = Client(host, PORT, serverhost, serverport)


 

    



