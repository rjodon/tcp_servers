import multiprocessing as mp
import socket



def handle(connection, address, queue):
    try:
        print("Handling {}".format(address))
        data = connection.recv(1024)
        msg = data.decode()
        print("{} says: {}".format(address, msg))
        queue.put_nowait(msg)
    except:
        print("Problem handling request")
    finally:
        print("Closing socket")
        connection.close()


class Server:
    def __init__(self, hostname, port, queue):
        self.hostname = hostname
        self.port = port
        self.queue = queue

    def start(self):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.bind((self.hostname, self.port))
        self.socket.listen(1)

        while True:
            conn, address = self.socket.accept()
            process = mp.Process(target=handle, args=(conn, address, self.queue))
            process.daemon = True
            process.start()

if __name__ == "__main__":
    msgs = mp.Queue()
    server = Server("0.0.0.0", 2222, msgs)
    try:
        print("Listening")
        server.start()
    except:
        print("Unexpected exception")
    finally:
        print("Shutting down")
        msgs.put('STOP')
        for process in mp.active_children():
            print("Shutting down process %r", process)
            process.terminate()
            process.join()
        msg = []
        for i in iter(msgs.get_nowait, 'STOP'):
            msg.append(i)
        print("Messages received: {} ".format(msg))
        print(len(msg))