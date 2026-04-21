import socket
import sys

def check_server(host, port):
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(2)
        result = sock.connect_ex((host, int(port)))
        if result == 0:
            print("Server up")
        else:
            print("Server down")
        sock.close()
    except Exception:
        print("Server down")

if __name__ == "__main__":
    check_server(sys.argv[1], sys.argv[2])