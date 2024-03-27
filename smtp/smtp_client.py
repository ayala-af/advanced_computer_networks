# Ayala Aftergut
import smtp_protocol
import base64
import socket
import time

CLIENT_NAME = "client.com"
# Add the minimum required fields to the email
EMAIL_TEXT = "From:barbie\nTo:shookie\nData: So cool to use SMTP protocol!" + smtp_protocol.EMAIL_END


def create_ehlo():
    return "EHLO {}\r\n".format(CLIENT_NAME).encode()


def create_auth_login():
    return("AUTH LOGIN"+"\r\n").encode()


def create_user_name(user):
    return base64.b64encode(user.encode())


def create_password(password):
    return base64.b64encode(password.encode())


def create_mail_from(user):
    return ("MAIL FROM: <"+user+"@gmail.com>"+"\r\n").encode()


def create_rcpt_to(mail_to):
    return ("RCPT TO: <"+mail_to+"@gmail.com>"+"\r\n").encode()


def create_data():
    return ("DATA"+"\r\n").encode()


def create_email_conent():
    return (EMAIL_TEXT+"\r\n").encode()


def create_quit():
    return ("QUIT"+"\r\n").encode()


def connect_to_server( my_socket):
    try:
        my_socket.connect(("127.0.0.1", smtp_protocol.PORT))
        print('Connection succeeded!\r\n')
        return True

    except socket.error as e:
        print(f"Connection failed: {e}")
        my_socket.close()
        return False


def main():
    # Connect to server
    my_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    while not connect_to_server(my_socket):
        print("Retrying connection...")
        time.sleep(1)

    # 1 server welcome message
    response = my_socket.recv(1024).decode()
    print(response)
    # Check that the welcome message is according to the protocol
    if not response.startswith(smtp_protocol.SMTP_SERVICE_READY):
        print('Unable to connect to server. Unexpected response.')
        my_socket.close()
        return

    # 2 EHLO message
    message = create_ehlo()
    my_socket.send(message)
    response = my_socket.recv(1024).decode()
    print(response)
    if not response.startswith(smtp_protocol.REQUESTED_ACTION_COMPLETED):
        print("Error connecting")
        my_socket.close()
        return
    server_name = response.split()[1]

    # 3 AUTH LOGIN
    print("login")
    my_socket.send(create_auth_login())
    response = my_socket.recv(1024).decode()
    print(response)
    if not response.startswith(smtp_protocol.AUTH_INPUT):
        print("Error")
        my_socket.close()
        return

    # 4 User
    user = "barbie"
    my_socket.send(create_user_name(user)+"\r\n".encode())
    response = my_socket.recv(1024).decode()
    print(response)
    if not response.startswith(smtp_protocol.AUTH_INPUT):
        print("Error")
        my_socket.close()
        return

    # 5 password
    password = "helloken"
    my_socket.send(create_password(password)+"\r\n".encode())
    response = my_socket.recv(1024).decode()
    print(response)
    if not response.startswith(smtp_protocol.AUTH_SUCCESS):
        print("Error")
        my_socket.close()
        return

    # 6 mail from

    my_socket.send(create_mail_from(user))
    response = my_socket.recv(1024).decode()
    print(response)
    if not response.startswith(smtp_protocol.REQUESTED_ACTION_COMPLETED):
        print("Error")
        my_socket.close()
        return

    # 7 rcpt
    send_to = "shooki"
    my_socket.send(create_rcpt_to(send_to))
    response = my_socket.recv(1024).decode()
    print(response)
    if not response.startswith(smtp_protocol.REQUESTED_ACTION_COMPLETED):
        print("Error")
        my_socket.close()
        return

    # 8 data
    my_socket.send(create_data())
    response = my_socket.recv(1024).decode()
    print(response)
    if not response.startswith(smtp_protocol.ENTER_MESSAGE):
        print("Error")
        my_socket.close()
        return

    # 9 email content
    my_socket.send(create_email_conent())
    response = my_socket.recv(1024).decode()
    print(response)
    if not response.startswith(smtp_protocol.REQUESTED_ACTION_COMPLETED):
        print("Error")
        my_socket.close()
        return

    # 10 quit
    my_socket.send(create_quit())
    response = my_socket.recv(1024).decode()
    print(response)
    if not response.startswith(smtp_protocol.GOODBYE):
        print("Error")
        my_socket.close()
        return

    print("Closing\n")
    my_socket.close()


if __name__ == "__main__":
    main()