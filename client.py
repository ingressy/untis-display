import socket

client = socket.socket()

HOST = '127.0.0.1'
PORT = 2450
BATTERY = ' - 42'
CLIENT = '2.311'

client.connect((HOST, PORT))

client.send(CLIENT.encode())
client.send(BATTERY.encode())
print(client.recv(1024).decode())

client.close()