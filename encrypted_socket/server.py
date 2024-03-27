"""EX 2.6 server implementation
   Author:Ayala Aftergut
   Date: 04/02/2024
"""

import socket
import protocol

RSA_PUBLIC_KEY = 83
RSA_PRIVATE_KEY = 14747


def create_server_rsp(cmd):
    """Based on the command, create a proper response"""
    return "Server response: " + cmd


def main():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(("0.0.0.0", protocol.PORT))
    server_socket.listen()
    print("Server is up and running")
    (client_socket, client_address) = server_socket.accept()
    print("Client connected")

    # Diffie Hellman
    # 1 - choose private key
    private_key = protocol.diffie_hellman_choose_private_key()
    # 2 - calc public key
    public_key = protocol.diffie_hellman_calc_public_key(private_key)
    # 3 - interact with client and calc shared secret
    valid_msg, message = protocol.get_msg(client_socket)
    if not valid_msg:
        print("ERROR")
        print("Closing\n")
        client_socket.close()
    other_side_public = int(message)
    client_socket.send(protocol.create_msg(str(public_key)).encode())

    shared_secret = protocol.diffie_hellman_calc_shared_secret(other_side_public, private_key)
    # RSA
    # Exchange RSA public keys with client
    valid_msg, message = protocol.get_msg(client_socket)
    if not valid_msg:
        print("ERROR")
        print("Closing\n")
        client_socket.close()
    client_rsa_public = int(message)
    client_socket.send(protocol.create_msg(str(RSA_PUBLIC_KEY)).encode())
    while True:
        # Receive client's message
        valid_msg, message,  = protocol.get_msg(client_socket)
        if not valid_msg:
            print("Something went wrong with the length field")
        else:
            # Check if client's message is authentic
            # 1 - separate the message and the MAC
            message, mac = protocol.separate_mac(message)
            # 2 - decrypt the message
            decrypted_msg = protocol.symmetric_encryption(message, shared_secret)
            # 3 - calc hash of message
            hash_msg = protocol.calc_hash(decrypted_msg)
            # 4 - use client's public RSA key to decrypt the MAC and get the hash
            decrypted_hash = protocol.calc_signature(mac, client_rsa_public)
            # 5 - check if both calculations end up with the same result
            if int(decrypted_hash) != int(hash_msg):
                print("ERROR")
                break
            else:
                print(decrypted_msg)

            if decrypted_msg == "EXIT":
                break

            # Create response. The response would be the echo of the client's message
            rsp = create_server_rsp(decrypted_msg)

            # Encrypt
            # apply symmetric encryption to the server's message
            message = protocol.symmetric_encryption(rsp, shared_secret)
            # Send to client
            # Combine encrypted user's message to MAC, send to client
            mac = protocol.calc_signature(protocol.calc_hash(rsp), RSA_PRIVATE_KEY)
            msg = protocol.create_msg(message + mac)
            client_socket.send(msg.encode())

    print("Closing\n")
    client_socket.close()
    server_socket.close()


if __name__ == "__main__":
    main()
