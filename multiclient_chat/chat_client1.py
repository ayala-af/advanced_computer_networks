# Ayala Aftergut

import socket
import select
import msvcrt
import chat_protcol
# NAME <name> will set name. Server will reply error if duplicate
# GET_NAMES will get all names
# MSG <NAME> <message> will send message to client name
# EXIT will close client

my_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
my_socket.connect(("127.0.0.1", chat_protcol.SERVER_PORT))
print("Pls enter commands\n")
msg = ""
while msg != "EXIT":
    rlist, wlist, xlist = select.select([my_socket], [], [], 0.1)
    if rlist:
        data = chat_protcol.get_msg(my_socket)
        if not data[0]:
            print("error")
            break
        print("Server sent:", data[1])
    if msvcrt.kbhit():
        char = msvcrt.getch().decode()
        print(char, end="", flush=True)
        if char == "\r":
            print()
            my_socket.send(chat_protcol.create_msg(msg))
            msg = ""
        else:
            msg += char
my_socket.close()


