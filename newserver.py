
import socket
from threading import Thread
import os
class Server:
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.listFile={}
        thread=Thread(target=self.start)
        thread.start()
        self.loop()
        thread.join()
        
    def loop(self):
        while True:
            cmd=input("")
            cmd= cmd.lower()
            if(cmd==""):
                break


    def decodemsg(self, data):
        data= data.split("> ",1)
        header=data[0].split("<",1)[1]
        print(header)
        msg=data[1].split(" <",1)[0]
        return header, msg
    
    def on_new_client(self, client_socket, addr):
        print(f"New connection from: {addr}")
        data=client_socket.recv(2048).decode()
        REG=0
        while True:
            if not data:
                continue
            header, msg=self.decodemsg(data)
            if (header == "REG" and REG == 0):
                id = msg
                REG = 1
                print("A client has registered with id: ", id)
                #send response
                client_socket.send("<REG_ACK/>".encode())
                
            elif(header=="PUSH"):
                #push file
                if(id in self.listFile):
                    self.listFile[id].append(msg)
                else:
                    self.listFile[id]=[msg]
                print(self.listFile)
                client_socket.send("<PUSH_ACK/>".encode())
                
            elif(header=="GET_F"):
                list=""
                for key in self.listFile:
                    if msg in self.listFile[key]:
                        list+=key+";"
                        break
                client_socket.send(list.encode())
                #send response  
                client_socket.send("<GET_F_ACK/>".encode())
            
            data=client_socket.recv(2048).decode()
               
                


  
    def start(self):
        self.socket.bind((self.host, self.port))
        self.socket.listen(1)
        print(f"Server listening on {self.host}:{self.port}")
        while True:
            conn, addr = self.socket.accept()
            print(f"Connected by {addr}")
            thread = Thread(target=self.on_new_client, args=(conn, addr))  # create the thread
            thread.start()  # start the thread

#main
PORT= 8080
host = "192.168.0.105"
server = Server(host, PORT)

