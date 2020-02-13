import datetime
import queue as q
import threading

# server
class Client: # client... ??
    """ The protocol used by the socket
    <size of message [2 bytes]><message [size of message bytes]>
    max message size: 65,535 bytes (or chars)
    """

    MESSAGE_LEN_PACKET_SIZE = 2
    BYTE_ORDER = "big"

    def __init__(self, socket, host=False):

        self.socket = socket
        self.valid = self.socket is not None

        self.received_queue = q.Queue()
        self.send_queue = q.Queue()

        self.inbound_thread = threading.Thread(target=self.inbound, args=(socket,))
        self.outbound_thread = threading.Thread(target=self.outbound, args=(socket,))

    def start(self):

        if self.inbound_thread.is_alive() or self.outbound_thread.is_alive():
            print("Error: can not start client, already alive")
            return

        self.inbound_thread.start()
        self.outbound_thread.start()

    def inbound(self, socket):
        # receive messages until it fails :/
        while self.is_valid():
            if not self.receive():
                return

    def outbound(self, socket):
        # send messages until its fails :/
        while self.is_valid():
            if not self.send_queue.empty():
                if not self.send():
                    return

    def is_valid(self, print_message=False):

        if print_message and not self.valid:
            print("Error: Invalid Socket")

        return self.valid and self.socket is not None

    def send(self):
        """ Send message from the start of the send que

        :return:            true if a message was sent
        """

        if not self.is_valid(True):
            return False

        message = self.send_queue.get(block=True, timeout=None)

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
        """ Receives message putting it on top of the recived queue

        :return:    True if successful, false other wise.
        """

        if not self.is_valid(True):
            return False

        try:
            # receive the first bytes couple of bytes for our message len
            data = self.socket.recv(self.MESSAGE_LEN_PACKET_SIZE)
            message_len = int.from_bytes(data, self.BYTE_ORDER)

            # receive the message
            message = self.socket.recv(message_len).decode("utf-8")
            self.received_queue.put(message, block=True, timeout=None)

            # self.timestamp_received = int(
            #    (datetime.datetime.utcnow() - datetime.datetime(1970, 1, 1) ).total_seconds())

        except Exception as e:
            print(e)
            self.valid = False
            return False

        return True
