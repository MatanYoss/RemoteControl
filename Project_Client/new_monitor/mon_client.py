import socket
import time
import io
import ctypes
from PIL import ImageGrab, Image
import sys
import threading
user32 = ctypes.windll.user32
wid_hei = user32.GetSystemMetrics(0), user32.GetSystemMetrics(1)

WIDTH = 0
HEIGHT = 0

SERVER_HOST = sys.argv[2]
SERVER_PORT = int(sys.argv[1])

class Pixle_sender():

    def __init__(self):
        self.conn = self.Get_connection()
        self.WIDTH = 0
        self.HEIGHT = 0
        self.exit_flag = False


    def Get_connection(self):
        so = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # connect to the server
        so.connect((SERVER_HOST, SERVER_PORT))
        so.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)
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

    def Server_Exit(self):
        d = self.conn.recv(1024).decode()
        if(d == "EXIT"):
            self.exit_flag = True








    def Main(self):

        self.WIDTH, self.HEIGHT = self.Get_Screen_Size()
        print(str(self.WIDTH))
        print(str(self.HEIGHT))
        # The region to capture
        time.sleep(0.5)
        check_for_exit_thread = threading.Thread(target=self.Server_Exit)
        check_for_exit_thread.start()
        i = 0
        while self.exit_flag == False:
            # Capture the screen
            img = ImageGrab.grab(bbox=None)
            print("took")
            resized_img = img.resize((self.WIDTH, self.HEIGHT))
            image_bytes = io.BytesIO()
            resized_img.save(image_bytes, format='JPEG')
            # Tweak the compression level here (0-9)
            pixels = image_bytes.getvalue()
            print(len(pixels))
            # Send the pixels
            #print(pixels)
            if(len(pixels) % 1024 == 0):
                i = 100000000000000000000000000000000
            self.Sender(pixels)
            #print(i)
            i += 1
        self.conn.close()


    def Sender(self, pixels):
        pix = io.BytesIO(pixels)
        f = False
        f1 = pix.read(1024)
        while f1:
            if(len(f1) < 1024):
                self.conn.send(f1 + "#".encode() * (1024 - len(f1)))
                f1_len = str(len(f1))
                self.conn.send(str(len(f1)).encode() + (1024 - len(f1_len)) * "+".encode())
                f = True
                #print("Sent")
                break
            self.conn.send(f1)
            f1 = pix.read(1024)

        if(f == False): # in case its 1024
            print("Sent *")
            self.conn.send(("*" * 1024).encode())









ps = Pixle_sender()
ps.Main()
print("exited")
