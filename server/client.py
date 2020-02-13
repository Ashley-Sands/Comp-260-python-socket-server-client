import datetime
import queue as q
import threading

# server
class Client:
    """ The protocol used by the socket
    <size of message [2 bytes]><message [size of message bytes]>
    max message size: 65,535 bytes (or chars)
    """

    MESSAGE_LEN_PACKET_SIZE = 2
    BYTE_ORDER = "big"

    def __init__(self, socket):

        self.socket = socket
        self._valid = self.socket is not None   # unsafe, use set and is valid functions

        self.received_queue = q.Queue()
        self.send_queue = q.Queue()

        self.inbound_thread = threading.Thread(target=self.inbound, args=(socket,))
        self.outbound_thread = threading.Thread(target=self.outbound, args=(socket,))
        self.thread_lock = threading.Lock()

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
        """ Thread safe method to see if the client is valid

        :param print_message: should a error message be displayed
        :return: True if the client is valid otherwise false
        """

        self.thread_lock.acquire()

        valid = self._valid and self.socket is not None

        self.thread_lock.release()

        if print_message and not valid:
            print("Error: Invalid Socket")

        return valid

    def set_is_vaild(self, vaild):
        """ Thread safe method to set is vaild

        :param vaild: is the socket vaild?
        """
        self.thread_lock.acquire()

        self._valid = vaild

        self.thread_lock.release()

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
            self.set_is_vaild( False )
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
            self.set_is_vaild( False )
            return False

        return True
