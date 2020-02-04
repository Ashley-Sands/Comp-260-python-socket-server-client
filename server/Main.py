import socket
import time
import protocol
import threading

threads = {}

messages = []


def get_messages(client):

    if client.is_valid():
        if client.receive():
            messages.append(client.message)
            print(client.message, "time sent: ", client.timestamp_sent,
                  "time recived: ", client.timestamp_received,
                  "delta: ", (client.timestamp_received - client.timestamp_sent) / 1000)

        if client.is_valid():
            client.send("OK")


def client_task(client):
    print("starting client task")

    last_id = 0
    receive_thread = None

    while client.is_valid():

        if receive_thread is None or not receive_thread.is_alive() :
            receive_thread = threading.Thread(target=get_messages, args=(client,))
            receive_thread.start()

        # send all pending messages
        while last_id < len(messages):
            client.send(messages[last_id])
            last_id += 1

        time.sleep(0.5)

    print("Ending client task")

if __name__ == "__main__":

    socket_inst = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    #socket_inst.settimeout(0.0) # prevent the recv function from blocking

    socket_inst.bind(("127.0.0.1", 8222))
    socket_inst.listen(5)
    socket_protocol = None

    while True:

        #if socket_protocol is None or not socket_protocol.is_valid():
        client, addr = socket_inst.accept()
        socket_protocol = protocol.Protocol(client, True)

        if addr not in threads:
            socket_protocol.send("Connection-OK")
            threads[addr] = threading.Thread( target=client_task, args=(socket_protocol,) )
            threads[addr].start()
        else:
            print("Error: rejecting connection, they already have a thread")
            client.close()