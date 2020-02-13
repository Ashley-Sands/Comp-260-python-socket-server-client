import socket
import time
import threading

from client import Client

clients = {}
client_count = 0

accepting_conn_thread = None
accepting_connections = True
thread_lock = threading.Lock()


def accept_clients(socket_):
    global accepting_connections
    print("starting to accept clients")

    while True:

        try:
            client = socket_.accept()[0]

            thread_lock.acquire()

            if not accepting_connections:
                break

            clients["client" + str(client_count)] = Client(client)
            clients["client" + str(client_count)].start()
            print("new client accepted!")
            thread_lock.release()
        except Exception as e:
            print("error on socket, ", e)

            thread_lock.acquire()
            accepting_connections = False
            thread_lock.release()
            break

        time.sleep(0.5)

    print("that's enough clients for now")


if __name__ == "__main__":

    socket_inst = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    #socket_inst.settimeout(0.0) # prevent the recv function from blocking

    socket_inst.bind(("127.0.0.1", 8222))
    socket_inst.listen(5)

    # start a thread to receive connections
    accepting_conn_thread = threading.Thread(target=accept_clients, args=(socket_inst,))
    accepting_conn_thread.start()

    print ("\nwaiting for connections...")

    #socket_inst.close()

    # process all the data :)
    while True:
        pass
