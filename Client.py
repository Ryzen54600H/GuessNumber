import socket

host = "0.tcp.ap.ngrok.io"
port = 18368
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((host, port))

client.sendall(b"Hello")

