import socket
import ctypes
import cv2
import numpy as np
from PIL import Image
import lz4.frame
import io
import threading
import time
import sys
from threading import Thread
user32 = ctypes.windll.user32
SCREEN_SIZE = user32.GetSystemMetrics(0), user32.GetSystemMetrics(1)
SERVER_HOST = "10.0.0.9"
SERVER_PORT = int(sys.argv[1])
pixel_list_lock = threading.Lock()


class Get_Pixles_Thread(threading.Thread):
    def __init__(self, conn):
        threading.Thread.__init__(self)
        self.conn = conn
        self.pixel_list = []

    def run(self):
        while True:
            pixles = "".encode()
            while True:
                l = self.conn.recv(1024)
                if(l == '*'.encode() * 1024): # if last data is exactly 1024 we will get after it this pattern
                    break
                if ("+".encode() * 1000 in l): # it is the last data or just an ordinary package?
                    i = l.find(b'+') # because the last data is less then 1024 we need to make a split and get it..
                    last_pac_len = int(l[:i])
                    pixles = pixles[:-(1024 -last_pac_len)]
                    break
                pixles += l

            print("Got it")
            pixel_list_lock.acquire()
            self.pixel_list.append(pixles)
            pixel_list_lock.release()



class LiveScreen():
    def __init__(self):
        self.conn = self.Get_conn()
        self.WIDTH = 0
        self.HEIGHT = 0
        self.thread = ""

    def Get_conn(self):
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        print("try")
        s.bind((SERVER_HOST, SERVER_PORT))
        s.listen(1)
        s.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)
        conn, client_address = s.accept()
        return conn

    def Set_Screen_Size(self):
        wid_hei = self.conn.recv(1024).decode()
        wid = int(wid_hei.split(" ")[0])
        hei = int(wid_hei.split(" ")[1])
        if(SCREEN_SIZE[0] < wid or SCREEN_SIZE[1] < hei):
            sw = int(SCREEN_SIZE[0]) - 800
            sh = int(SCREEN_SIZE[1]) - 800
            self.conn.send((str(sw) + " " + str(sh)).encode())
            return sw, sh
        else:
            self.conn.send("OK".encode())
            return int(wid), int(hei)



    def Start_Get_Pixles_Thread(self):
        thread = Get_Pixles_Thread(self.conn)
        thread.start()
        self.thread = thread



    def main(self):
        empty_list_flag = False
        print(self.conn)
        self.WIDTH, self.HEIGHT = self.Set_Screen_Size()
        print(str(self.WIDTH))
        print(str(self.HEIGHT))
        i = 0
        #self.Create_Sample_Img()
        #print("ok")
        self.Start_Get_Pixles_Thread()
        while True:

            time.sleep(0.0001)
            try:
                pixel_list_lock.acquire()
                pixels = self.thread.pixel_list.pop(0)
            except:
                pixel_list_lock.release()
                #print("List empty")
                continue
            pixel_list_lock.release()
            img = Image.open(io.BytesIO(pixels))
            img_np = np.array(img)
            frame = cv2.cvtColor(img_np, cv2.COLOR_BGR2RGB)
            # show image on OpenCV frame
            cv2.imshow("Screen", frame)

            #print("Showed it")
            if cv2.waitKey(1) == 27:
                break
            #print (i)
            i+=1





ls = LiveScreen()
ls.main()


