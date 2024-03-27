# Ayala Aftergut

LENGTH_FIELD_SIZE = 2
SERVER_PORT = 5555


def create_msg(data):
    """Creates a protocol message with length field"""
    length = str(len(data))
    zfill_length = length.zfill(LENGTH_FIELD_SIZE)
    message = zfill_length + data
    return message.encode()


def get_msg(my_socket):
    """Extracts a message by field size, returns True if the msg had a length field (and False if id doesn't have)
    and a proper msg"""
    try:
        msg_length = my_socket.recv(LENGTH_FIELD_SIZE).decode()
        if msg_length.isdigit():
            return True, my_socket.recv(int(msg_length)).decode()
        elif msg_length == "":
            # in case of close()
            return False, ""
        else:
            return False, "ERROR, can not read the message"
    except ConnectionResetError:
        # Connection error
        return False, ""
    except ConnectionAbortedError:
        return False, ""