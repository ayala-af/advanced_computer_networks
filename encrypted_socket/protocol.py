"""Encrypted sockets implementation
   Author:Ayala Aftergut
   Date:04/02/2024
"""
import random

LENGTH_FIELD_SIZE = 2
PORT = 8820

DIFFIE_HELLMAN_P = 89
DIFFIE_HELLMAN_G = 97

RSA_P = 137
RSP_Q = 151
# len(str(2^16))=5
MAC_LENGTH = 5


def symmetric_encryption(input_data, key):
    """Return the encrypted / decrypted data
    The key is 16 bits. If the length of the input data is odd, use only the bottom 8 bits of the key.
    Use XOR method"""
    len_shared = len(str(DIFFIE_HELLMAN_P))
    key = str(key).zfill(len_shared).encode()
    input_data = input_data.encode()
    encrypted_message = bytearray()
    for i in range(0, len(input_data)-1, 2):
        encrypted_message.append(input_data[i] ^ key[0])
        encrypted_message.append(input_data[i+1] ^ key[1])
    if len(input_data) % 2 == 1:
        encrypted_message.append(input_data[len(input_data)-1] ^ key[1])
    return encrypted_message.decode()


def diffie_hellman_choose_private_key():
    """Choose a 16 bit size private key """
    num = random.randint(0, 65536)
    return num


def diffie_hellman_calc_public_key(private_key):
    """G**private_key mod P"""
    return (DIFFIE_HELLMAN_G ** private_key) % DIFFIE_HELLMAN_P


def diffie_hellman_calc_shared_secret(other_side_public, my_private):
    """other_side_public**my_private mod P"""
    return (other_side_public**my_private) % DIFFIE_HELLMAN_P


def calc_hash(message):
    """Create some sort of hash from the message
    Result must have a fixed size of 16 bits"""
    return str(int.from_bytes(message.encode(), byteorder='big') % 20687)


def calc_signature(hash_msg, rsa_private_key):
    """Calculate the signature, using RSA algorithm
    hash**RSA_private_key mod (P*Q)"""
    return str((int(hash_msg)**rsa_private_key) % (RSA_P * RSP_Q)).zfill(5)


def create_msg(data):
    """Create a valid protocol message, with length field
    For example, if data = data = "hello world",
    then "11hello world" should be returned"""
    length = str(len(data))
    length = length.zfill(LENGTH_FIELD_SIZE)
    message = length+data
    return message


def get_msg(my_socket):
    """Extract message from protocol, without the length field
       If length field does not include a number, returns False, "Error" """
    msg_data_length = my_socket.recv(LENGTH_FIELD_SIZE).decode()
    return True, my_socket.recv(int(msg_data_length)).decode()


def separate_mac(msg):
    """separates the msg and mac"""
    return msg[0:len(msg)-MAC_LENGTH], msg[len(msg)-MAC_LENGTH:len(msg)]
