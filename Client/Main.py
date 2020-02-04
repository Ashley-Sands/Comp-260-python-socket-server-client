import socket
import time
import protocol

socket_protocol = None
connect_retry_len = 0.5
connect_attempt = 0

message_to_send = ""
message_recived = ""

noinput = False;

if __name__ == "__main__":

    while True:
        # do we have an active socket?
        if socket_protocol is None or not socket_protocol.is_valid():
            socket_inst = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            socket_protocol = protocol.Protocol(socket_inst, False)

        # connect to the host/server
        while not socket_protocol.connected:
            try:
                socket_protocol.connect("127.0.0.1", 8222)
                print("Connected to host")

                connect_retry_len = 0.5
                connect_attempt = 0
            except Exception as e:
                print(e, "Atemp:", connect_attempt, "retrying in ", connect_retry_len, "Seconds")
                connect_attempt += 1

                time.sleep(connect_retry_len)
                if connect_retry_len < 5:
                    connect_retry_len += 0.25

        if len(message_to_send) > 0 and socket_protocol.is_valid():
            # send messages
            # socket_protocol.socket.settimeout(1.0)  # take as long as it needs to send the message
            socket_protocol.send(message_to_send)
            message_to_send = ""



        if socket_protocol.is_valid():
            # socket_protocol.socket.settimeout(0.1)  # if we have a message grate, if not so bee it
            # receive messages

            try:
                socket_protocol.receive()
                print(socket_protocol.message)
            except Exception as e:  # but we do care if it timed out while receiving a message
                print(e)
                pass

        if not noinput:
            message_to_send = input("Say something: ")

        if message_to_send == "-noinput":
            message_to_send = "";
            noinput = True
