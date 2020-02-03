
class Protocol:
    """ The protocol used by the socket
    <size of message [2 bytes]><message [size of message bytes]>
    max message size: 65,535 bytes (or chars)
    """

    MESSAGE_LEN_PACKET_SIZE = 2
    BYTE_ORDER = "big"

    def __init__(self, socket, host=False):
        self.socket = socket
        self.host = host
        self.connected = host
        self.valid = self.socket is not None
        self.message = ""

    def is_valid(self, printMessage=False):

        if printMessage and not self.valid:
            print("Error: Invalid Socket")

        return self.valid

    def is_connected(self, printMessage=False):

        if printMessage and not self.connected:
            print("Not connected")
        elif printMessage:
            print("Already connected")

        return self.connected

    def connect(self, ip_str, port):
        if self.host:
            print("Unable to connect, I am the host!")
            return
        elif not self.is_valid(True) and self.is_connected(True):
            return

        self.socket.connect((ip_str, port))
        self.connected = True

    def send(self, message):
        """ Send message to socket

        :param message:     message to send
        :return:            true if successful otherwise false
        """

        if not self.is_valid(True):
            return False

        # check that the message is within the max message size
        if len(message) > pow(255, self.MESSAGE_LEN_PACKET_SIZE):
            print("Error: Message has exceeded the max message length.")
            return False

        message_length = len(message).to_bytes(self.MESSAGE_LEN_PACKET_SIZE, self.BYTE_ORDER)

        try:
            self.socket.send( message_length )
            self.socket.send( message.encode() )
        except Exception as e:
            print(e)
            self.valid = False
            return False

        return True

    def receive(self):
        """ Receives message from socket

        :return:    True if successful, false other wise.
        """

        if not self.is_valid(True):
            return False

        try:
            # receive the first bytes few bytes for our message len
            data = self.socket.recv(self.MESSAGE_LEN_PACKET_SIZE)
            message_len = int.from_bytes(data, self.BYTE_ORDER)

            # receive the message
            self.message = self.socket.recv(message_len).decode("utf-8")

        except Exception as e:
            print(e)
            self.valid = False
            self.message = ""
            return False

        return True
