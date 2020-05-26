#!/usr/bin/python3

import threading
import socket
import os
import threading_class
import time
GUIHOST = '127.0.0.1'
GUIPORT = 4000
GUIADDR = (GUIHOST, GUIPORT)

class Server_Side_Connection():
    def __init__(self):
        self.listen_addr = '10.0.0.7'
        self.listen_port = 8082
        self.dir_path = os.path.dirname(os.path.realpath(__file__)) + "\\..\\"
        self.thread_lst = []
        self.guisock = self.Get_Connection_GUI()
        self.stopEvent = threading.Event()

    def Get_Secure_Connection(self):
        bindsocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        bindsocket.bind((self.listen_addr, self.listen_port))
        bindsocket.listen(101)
        newsocket = ""
        i = 0
        while (True):
            print("Waiting for client")
            newsocket, fromaddr = bindsocket.accept()
            print("Client connected: {}:{}".format(fromaddr[0], fromaddr[1]))
            if self.stopEvent.is_set() == True:
                print("oK")
                break
            self.thread_lst.append(threading_class.Client_Thread_Side(newsocket, self.guisock, i))#add thread
            self.thread_lst[i].start()
            i += 1

        newsocket.close()
        print("Exited from the thread")

    def Get_Connection_GUI(self):
        guisock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        guisock.connect(GUIADDR)
        return guisock

    def Get_Data_From_Gui(self):
        data = self.guisock.recv(1024).decode()
        data = data[:data.find('*')]
        return data

    def Exit_Process(self):
        for x in self.thread_lst:
            try:
                x.conn.send("Exit".encode())# send to the clients exit message
                x.stopEvent.set() # exit the client - threads... set the loop event to true
            except socket.error: # if client has been disconnected by itself in the past.
                pass

        # stop the thread
        self.stopEvent.set() # stop event to the thread that waiting for new clients..
        self.guisock.close() # close the connection with the gui socket
        fake_client = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # create fake client
        fake_client.connect((self.listen_addr, self.listen_port)) # connect it to the server



    def Check_Port(self, port):
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        result = False
        try:
            sock.bind((self.listen_addr, int(port)))
            result = True
            print("PORT_SUCCESS")
        except:
            print("Port is in use")
        sock.close()
        return result

    def Handel_Port(self, data):
        if (self.Check_Port(data.split(" ")[2])):
            msg = data.split(" ")[0].encode() + "$PORT_SUCCESS".encode()
        else:
            msg = data.split(" ")[0].encode() + "$PORT_ERROR".encode()
        self.guisock.send(msg + '*'.encode() * (1024 - len(msg)))
        print(msg)




    def Send_To_Client(self):
        while True:
            data = self.Get_Data_From_Gui()
            if('PORT' in data):
                self.Handel_Port(data)
                continue

            if(data == "Exit"): # does the GUI server want to exit?
                self.Exit_Process() # Enter the exit process
                break # exit this function - exit the sever...
            data = data.split(" ")
            client_num = int(data[0])
            print(data)
            if(len(data) == 3):
                self.thread_lst[client_num - 1].conn.send(data[1].encode() + " ".encode() + data[2].encode())
            else:
                self.thread_lst[client_num-1].conn.send(data[1].encode())
        



c = Server_Side_Connection()
conn_thread = t = threading.Thread(target=c.Get_Secure_Connection)
conn_thread.start()
c.Send_To_Client()
print("Finished the job with code 0")








