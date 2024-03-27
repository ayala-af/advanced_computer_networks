# Ayala Aftergut
import socket
import datetime
import smtp_protocol
import base64

IP = '0.0.0.0'
SOCKET_TIMEOUT = 10
SERVER_NAME = "test_SMTP_server.com"

user_names = {"shooki": "abcd1234", "barbie": "helloken"}


def create_initial_response():
    return (("220-" + SERVER_NAME + str(datetime.datetime.now()) + "\r\n"
                                                                   "220-We do not authorize the use of this system to transport unsolicited,\r\n"
                                                                   "220 and/or bulk e-mail.\r\n").encode())


def create_ehlo_response(client_message):
    """ Check if client message is legal EHLO message
        If yes - returns proper Hello response
        Else - returns proper protocol error code"""
    if not (client_message.startswith("EHLO") and " "in client_message):
        return ("{}".format(smtp_protocol.COMMAND_SYNTAX_ERROR)).encode()
    client_name = client_message.split()[1]
    return "{}-{} Hello {}\r\n".format(smtp_protocol.REQUESTED_ACTION_COMPLETED, SERVER_NAME, client_name).encode()


def create_auth_login_response(client_message):
    """ Check if client message is legal AUTH LOGIN message
           If yes - returns proper AUTH_INPUT response
           Else - returns proper protocol error code"""
    if not client_message == 'AUTH LOGIN\r\n':
        return ("{}-did not got AUTH LOGIN\r\n".format(smtp_protocol.COMMAND_SYNTAX_ERROR)).encode()
    return "{}-{}\r\n".format(smtp_protocol.AUTH_INPUT, base64.b64encode("Username".encode()).decode()).encode()


def create_user_response(client_message):
    """ Check if client message is legal USER message
           If yes - returns proper AUTH_INPUT response
           Else - returns proper protocol error code"""
    if not (client_message in user_names):
        return ("{}-non exist user name\r\n".format(smtp_protocol.INCORRECT_AUTH)).encode()
    return "{}-{}\r\n".format(smtp_protocol.AUTH_INPUT, base64.b64encode("Password".encode()).decode()).encode()


def create_password_response(user_name, password):
    """ Check if client message is legal password message
           If yes - returns proper AUTH_SUCCESS response
           Else - returns proper protocol error code"""
    if not (user_name in user_names and user_names[user_name] == password):
        return ("{}-wrong user name or wrong password (or both\r\n".format(smtp_protocol.INCORRECT_AUTH)).encode()
    return "{}-Authentication successful\r\n".format(smtp_protocol.AUTH_SUCCESS).encode()


def create_mail_from_response(mail_from, user_name):
    """ Check if client message is legal MAIL FROM message
           If yes - returns proper  REQUESTED_ACTION_COMPLETED RESPONSE
           Else - returns proper protocol error code"""
    if not (mail_from.startswith("MAIL FROM:") and "<" in mail_from and ">" in  mail_from):
        return ("{}-Syntax error\r\n".format(smtp_protocol.COMMAND_SYNTAX_ERROR)).encode()
    if not mail_from.split("<")[1].split("@")[0] == user_name :
        return ("{}-incorrect mail from address\r\n".format(smtp_protocol.COMMAND_SYNTAX_ERROR)).encode()

    return "{}-OK \r\n".format(smtp_protocol.REQUESTED_ACTION_COMPLETED).encode()


def create_rcpt_to_response(rcpt_to):
    """ Check if client message is legal RCPT _TO message
           If yes - returns proper  REQUESTED_ACTION_COMPLETED RESPONSE
           Else - returns proper protocol error code"""
    if not ( rcpt_to.startswith("RCPT TO:") and "<" in rcpt_to and ">" in rcpt_to):
        return ("{}-Syntax error\r\n".format(smtp_protocol.COMMAND_SYNTAX_ERROR)).encode()
    if not rcpt_to.split("<")[1].split("@")[0] in user_names:
        return ("{}-this person doesnt exist\r\n".format(smtp_protocol.COMMAND_SYNTAX_ERROR)).encode()

    return "{}-Accepted \r\n".format(smtp_protocol.REQUESTED_ACTION_COMPLETED).encode()


def create_data_response(message):
    """ Check if client message is legal DATA message
           If yes - returns proper  ENTER_MESSAGE
           Else - returns proper protocol error code"""
    if not message.startswith("DATA"):
        return ("{}-Syntax error\r\n".format(smtp_protocol.COMMAND_SYNTAX_ERROR)).encode()
    return "{}-Enter message, ending with '.' on a line by itself \r\n".format(smtp_protocol.ENTER_MESSAGE).encode()


def create_email_content_response(message):
    """ Check if client message is legal email content message
           If yes - returns proper  REQUESTED_ACTION_COMPLETED RESPONSE
           Else - returns proper protocol error code"""
    if message.find(smtp_protocol.EMAIL_END) == -1:
        return ("{}-Syntax error\r\n".format(smtp_protocol.COMMAND_SYNTAX_ERROR)).encode()
    return ("{}-OK id=1 \r\n".format(smtp_protocol.REQUESTED_ACTION_COMPLETED)).encode()


def create_quit_response(message):
    """ Check if client message is legal QUIT message
           If yes - returns proper  GOODBYE
           Else - returns proper protocol error code"""
    if not message.startswith("QUIT"):
        return ("{}-Syntax error\r\n".format(smtp_protocol.COMMAND_SYNTAX_ERROR)).encode()
    return "{}-{} closing connection\r\n".format(smtp_protocol.GOODBYE, SERVER_NAME).encode()


def handle_smtp_client(client_socket):
    # 1 send initial message
    message = create_initial_response()
    client_socket.send(message)
    print(message.decode())

    # 2 receive and send EHLO
    message = client_socket.recv(1024).decode()
    print(message)
    response = create_ehlo_response(message)
    client_socket.send(response)
    print(response.decode())
    if not response.decode().startswith(smtp_protocol.REQUESTED_ACTION_COMPLETED):
        print("EHLO error")
        return

    # 3 receive and send AUTH Login
    message = client_socket.recv(1024).decode()
    print(message)
    response = create_auth_login_response(message)
    client_socket.send(response)
    print(response.decode())
    if not response.decode().startswith(smtp_protocol.AUTH_INPUT):
        print("AUTH INPUT (1) error")
        return

    # 4 receive and send USER message
    user_name = base64.b64decode(client_socket.recv(1024)).decode().split()[0]
    print(user_name)
    response = create_user_response(user_name)
    client_socket.send(response)
    print(response.decode())
    if not response.decode().startswith(smtp_protocol.AUTH_INPUT):
        print("AUTH INPUT(2) error")
        return

    # 5 password
    password = base64.b64decode(client_socket.recv(1024)).decode().split()[0]
    print(password )
    response = create_password_response(user_name, password)
    client_socket.send(response)
    print(response.decode())
    if not response.decode().startswith(smtp_protocol.AUTH_SUCCESS):
        print("AUTH SUCCESS error")
        return

    # 6 mail from
    mail_from = client_socket.recv(1024).decode()
    print(mail_from )
    response = create_mail_from_response(mail_from, user_name)
    client_socket.send(response)
    print(response.decode())
    if not response.decode().startswith(smtp_protocol.REQUESTED_ACTION_COMPLETED):
        print("MAIL FROM error")
        return

    # 7 rcpt to
    rcpt_to = client_socket.recv(1024).decode()
    print(rcpt_to )
    response = create_rcpt_to_response(rcpt_to)
    client_socket.send(response)
    print(response.decode())
    if not response.decode().startswith(smtp_protocol.REQUESTED_ACTION_COMPLETED):
        print("RCPT TO error")
        return

    # 8 DATA
    message = client_socket.recv(1024).decode()
    print(message)
    response = create_data_response(message)
    client_socket.send(response)
    print(response.decode())
    if not response.decode().startswith(smtp_protocol.ENTER_MESSAGE):
        print("DATA to error")
        return

    # 9 email content
    # The server should keep receiving data, until the sign of end email is received
    message = client_socket.recv(1024).decode()
    print(message)
    response = create_email_content_response(message)
    client_socket.send(response)
    if not response.decode().startswith(smtp_protocol.REQUESTED_ACTION_COMPLETED):
        print("content mail error")
        return
    else:
        mail_content = message.split(smtp_protocol.EMAIL_END)[0]
        print(mail_content)

    # 10 quit
    message = client_socket.recv(1024).decode()
    print(message )
    response = create_quit_response(message)
    client_socket.send(response)
    print(response.decode())
    if not response.decode().startswith(smtp_protocol.GOODBYE):
        print("QUIT to error")
        return


def main():
    # Open a socket and loop forever while waiting for clients
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((IP, smtp_protocol.PORT))
    server_socket.listen()
    print("Listening for connections on port\r\n {}".format(smtp_protocol.PORT))

    while True:
        try:
            client_socket, client_address = server_socket.accept()
            print('New connection received\r\n')
            client_socket.settimeout(SOCKET_TIMEOUT)
            handle_smtp_client(client_socket)
            print("Connection closed\r\n")

        except socket.error as e:
            print(e)


if __name__ == "__main__":
    # Call the main handler function
    main()
