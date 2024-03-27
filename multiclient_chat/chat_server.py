# Ayala Aftergut

import socket
import select
import chat_protcol

SERVER_IP = "0.0.0.0"


def create_error_reply(data):
    """create an error reply while trying to read the msg"""
    return " ".join(data)


def create_name_reply(current_socket, data, clients_names):
    """create a reply for NAME query
    return Hello  + client_name in the case if correct query and the name is still un- taken
    return Name is already taken in case the name  is already taken
    and in case their is no name in the msg return Uncorrected NAME msg, your name is missing """
    if len(data) >= 2:
        client_name = data[1]
        if client_name in clients_names:
            return "Name Is Already Taken"
        else:
            # if the client already have name
            for entry in clients_names.keys():
                # finds the sender's name
                if clients_names[entry] == current_socket:
                    clients_names.pop(entry)
                    break
            clients_names[client_name] = current_socket
            return "Hello " + client_name
    else:
        return "Uncorrected NAME Msg, Your Name Is Missing"


def create_get_names_reply(clients_names):
    """returns a string with the name of all participants """
    reply = ""
    for name in clients_names.keys():
        reply += name + " "
    return reply


def create_msg_reply(current_socket, data, clients_names):
    """returns a string with the reply, if the msg query is correct and the receiver exists
     returns the msg to the receiver and his socket, otherwise, returns  a proper reply to the sender and his socket"""
    if len(data) >= 2:
        send_to = data[1]
        if send_to in clients_names:
            # if send_to exists
            has_name = False
            for entry in clients_names.keys():
                # finds the sender's name
                if clients_names[entry] == current_socket:
                    sender_name = entry
                    has_name = True
                    break
            if len(data) >= 3:
                # if there is msg
                # the socket of the client that the sender wants to sent
                dest_socket = clients_names[send_to]
                msg = data[2]
                if has_name:
                    reply = sender_name + " sent " + msg
                else:
                    reply = "In Order To Send A Msg- You Have To Register, Use Name Command"
                    dest_socket = current_socket
            else:
                # if there no msg
                reply = "No Content In MSG"
                dest_socket = current_socket
        else:
            # if send_to doesn't exist
            reply = send_to + " Doesnt Exist"
            dest_socket = current_socket
    else:
        reply = "Uncorrected Msg- No send_to Name, And No Content In MSG"
        dest_socket = current_socket
    return dest_socket, reply


def create_illegal_command_reply():
    # reply for  illegal command
    return "Illegal Command"


def handle_client_request(current_socket, data, clients_names):
    """base on the current socket, the data that the client sent, and the clients_names dictionary
    returns the correct response and the dest_socket to send the response"""
    data = data.split()
    dest_socket = current_socket
    if len(data) > 0:
        # if "\r" was sent, data.split() is an empty list
        cmd = data[0]
        if cmd.startswith("ERROR"):
            reply = create_error_reply(data)

        elif cmd == "NAME":
            reply = create_name_reply(current_socket, data, clients_names)

        elif cmd == "GET_NAMES":
            reply = create_get_names_reply(clients_names)

        elif cmd == "MSG":
            (dest_socket, reply) = create_msg_reply(current_socket, data, clients_names)

        else:
            reply = create_illegal_command_reply()

    else:
        reply = create_illegal_command_reply()

    return reply, dest_socket


def print_client_sockets(client_sockets):
    """print the clients connection sockets"""
    for c in client_sockets:
        print("\t", c.getpeername())


def main():
    print("Setting up server...")
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((SERVER_IP, chat_protcol.SERVER_PORT))
    server_socket.listen()
    print("Listening for clients...")
    client_sockets = []
    messages_to_send = []
    clients_names = {}
    while True:
        read_list = client_sockets + [server_socket]
        ready_to_read, ready_to_write, in_error = select.select(read_list, client_sockets, [], 0.1)
        for current_socket in ready_to_read:
            if current_socket is server_socket:
                client_socket, client_address = server_socket.accept()
                print("New client joined!\n", client_address)
                client_sockets.append(client_socket)
                print_client_sockets(client_sockets)
            else:
                print("New data from client")
                data = chat_protcol.get_msg(current_socket)
                if not (data[0]) and (not data[1] == ""):
                    # error while trying to read data: the user didn't use the length field properly
                    # and it is not a close() msg
                    print(data[1])
                    (response, dest_socket) = handle_client_request(current_socket, data[1], clients_names)
                    messages_to_send.append((dest_socket, response))
                elif (not data[0]) and data[1] == "":
                    # the user didn't use the length field, but it is  a close() msg
                    print("Connection closed\n")
                    for entry in list(clients_names.keys()):
                        if clients_names[entry] == current_socket:
                            sender_name = entry
                            clients_names.pop(sender_name)
                    client_sockets.remove(current_socket)
                    current_socket.close()
                else:
                    # end every other message
                    # also If the client send "" and used the length field(it is not close() msg),
                    # or sent "\r"
                    print(data[1] + "\n")
                    (response, dest_socket) = handle_client_request(current_socket, data[1], clients_names)
                    messages_to_send.append((dest_socket, response))

        # write to everyone (note: only ones which are free to read...)
        for message in messages_to_send:
            current_socket, data = message
            if current_socket in ready_to_write:
                current_socket.send(chat_protcol.create_msg(data))
                messages_to_send.remove(message)


if __name__ == '__main__':
    main()
