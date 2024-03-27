"""Encrypted socket client implementation
   Author:Ayala Aftergut
   Date: 04/02/2024
"""
import socket
import protocol

RSA_PUBLIC_KEY = 83
RSA_PRIVATE_KEY = 14747


def main():
    my_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    my_socket.connect(("127.0.0.1", protocol.PORT))

    # Diffie Hellman
    # 1 - choose private key
    private_key = protocol.diffie_hellman_choose_private_key()
    # 2 - calc public key
    public_key = protocol.diffie_hellman_calc_public_key(private_key)
    # 3 - interact with server and calc shared secret
    my_socket.send(protocol.create_msg(str(public_key)).encode())
    valid_msg, message = protocol.get_msg(my_socket)
    if not valid_msg:
        print("ERROR")
        print("Closing\n")
        my_socket.close()

    other_side_public_key = int(message)
    shared_secret = protocol.diffie_hellman_calc_shared_secret(other_side_public_key, private_key)
    # RSA
    # Exchange RSA public keys with server
    my_socket.send(protocol.create_msg(str(RSA_PUBLIC_KEY)).encode())
    valid_msg, message = protocol.get_msg(my_socket)
    if not valid_msg:
        print("ERROR")
        print("Closing\n")
        my_socket.close()
    server_rsa_public = int(message)
    while True:
        user_input = input("Enter command\n")
        # Add MAC (signature)
        # 1 - calc hash of user input
        hash_msg = protocol.calc_hash(user_input)
        # 2 - calc the signature
        signature = protocol.calc_signature(hash_msg, RSA_PRIVATE_KEY)
        # Encrypt
        # apply symmetric encryption to the user's input
        encrypt_msg = protocol.symmetric_encryption(user_input, shared_secret)
        # Send to server
        # Combine encrypted user's message to MAC, send to server
        msg = protocol.create_msg(encrypt_msg + signature)
        my_socket.send(msg.encode())

        if user_input == 'EXIT':
            break

        # Receive server's message
        valid_msg, message = protocol.get_msg(my_socket)
        if not valid_msg:
            print("Something went wrong with the length field")

        # Check if server's message is authentic
        # 1 - separate the message and the MAC
        message, mac = protocol.separate_mac(message)
        # 2 - decrypt the message
        message = protocol.symmetric_encryption(message, shared_secret)
        # 3 - calc hash of message
        hash_msg = protocol.calc_hash(message)
        # 4 - use server's public RSA key to decrypt the MAC and get the hash
        mac = protocol.calc_signature(mac, server_rsa_public)
        # 5 - check if both calculations end up with the same result
        if int(mac) != int(hash_msg):
            print("ERROR")
            break
        # Print server's message
        print(message)

    print("Closing\n")
    my_socket.close()


if __name__ == "__main__":
    main()
