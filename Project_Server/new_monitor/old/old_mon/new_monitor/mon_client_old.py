import socket
import time
import sys
from zlib import compress
import io
from mss import mss
import ctypes
from PIL import ImageGrab, Image
import lz4.frame
user32 = ctypes.windll.user32
wid_hei = user32.GetSystemMetrics(0), user32.GetSystemMetrics(1)

WIDTH = 0
HEIGHT = 0

SERVER_HOST = "10.0.0.4"
SERVER_PORT = 4646

class Pixle_sender():

    def __init__(self):
        self.conn = self.Get_connection()
        self.WIDTH = 0
        self.HEIGHT = 0


    def Get_connection(self):
        so = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # connect to the server
        so.connect((SERVER_HOST, SERVER_PORT))
        return so

    def Get_Screen_Size(self):
        self.conn.send((str(wid_hei[0]) + " " + str(wid_hei[1])).encode())
        recv = self.conn.recv(1024).decode()
        if (recv == "OK"):
            return int(wid_hei[0]), int(wid_hei[1])
        wid = recv.split(" ")[0]
        hei = recv.split(" ")[1]
        print("OK")
        return int(wid), int(hei)







    def Main(self):

        self.WIDTH, self.HEIGHT = self.Get_Screen_Size()
        print(str(self.WIDTH))
        print(str(self.HEIGHT))
        # The region to capture
        time.sleep(0.5)
        while 'recording':
            # Capture the screen
            img = ImageGrab.grab(bbox=None)
            print("took")
            resized_img = img.resize((self.WIDTH, self.HEIGHT))
            image_bytes = io.BytesIO()
            resized_img.save(image_bytes, format='PNG')
            # Tweak the compression level here (0-9)
            pixels = lz4.frame.compress(image_bytes.getvalue())
            print(len(pixels))
            # Send the pixels
            #print(pixels)
            s = time.time()
            self.Sender(pixels)
            print(str(time.time() - s))


    def Sender(self, pixels):
        pix = io.BytesIO(pixels)
        f1 = pix.read(1024)
        self.conn.send(f1)
        while f1:
            f1 = pix.read(1024)
            if(len(f1) < 1024):
                #print("ok")
                self.conn.send(f1 + "_".encode() + (1023 - len(f1)) * "$".encode())
                self.conn.send(("+" * 1024).encode())
                print("Sent")
                break
            else:
                #print("sent")
                self.conn.send(f1)
        #print("exited")






ps = Pixle_sender()
ps.Main()
