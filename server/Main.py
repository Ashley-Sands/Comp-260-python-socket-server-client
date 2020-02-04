import socket
import time
import protocol
import threading

threads = {}


def client_task(client):
    print("starting client task")

    while client.is_valid():
        client.send("Helloo Socket Protocol")

        if client.is_valid():
            if client.receive():
                print( client.message )

        if client.is_valid():
            client.send("OK")

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
            threads[addr] = threading.Thread( target=client_task, args=(socket_protocol,) )
            threads[addr].start()
        else:
            print("Error: rejecting connection, they already have a thread")
            client.close()