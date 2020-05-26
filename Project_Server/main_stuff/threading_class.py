#!/usr/bin/python3
import threading





class Client_Thread_Side(threading.Thread):
    def __init__(self, conn, guisock, i):
        threading.Thread.__init__(self)
        self.conn = conn
        self.guisock = guisock
        self.num = i
        self.stopEvent = threading.Event()

    def run(self):
        while self.stopEvent.is_set() == False:
            self.Send_Data_To_Gui() # from client
        print("Im out!")

    def Get_Info_From_Client(self):
        try:
            d = self.conn.recv(1024)
            if(d == b''):# client has been disconnected
                self.stopEvent.set() # set stop event to exit the thread
                print("exited")
                return "REMOVE"# this string will be send to the GUI server
        except:
            self.stopEvent.set()
            print("exited")
            return "REMOVE"
        return d.decode()



    def Send_Data_To_Gui(self):
        data = self.Get_Info_From_Client() # get message from client
        if(data != "Exited"): # is the client sent ACK exit message?
            alld = str(self.num +1) + "$" + data
            print(alld)
            alld += "*" * (1024 - len(alld))
            self.guisock.send(alld.encode())
        else:
            self.conn.close() # close the connection
            self.stopEvent.set() # exit the thread - set the stop event to true


    def Get_Data_From_Gui(self):
        data = self.guisock.recv(1024)
        return data

            
        
        






