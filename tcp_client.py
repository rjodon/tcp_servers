import time
import socket


def client(ip, port, message):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.connect((ip, port))
        print("sending")
        sock.sendall(bytes(message, "utf-8"))
        print("message {}".format(message))




if __name__ == "__main__":
    host = "localhost"
    port = 2222
    for i in range(0, 1000):
        try:
            client(host, port, "Hello {}".format(i))
        except:
            pass
        time.sleep(0.002)
