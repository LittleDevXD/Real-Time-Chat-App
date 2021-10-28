import socket
import threading

HOST = "192.168.75.1"
PORT = 5500
BUFSIZE = 1024
FORMAT = "utf-8"
ADDR = (HOST, PORT)

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect(ADDR)

def receive_msg():
	while True:
		try:
			msg = client_socket.recv(BUFSIZE).decode(FORMAT)
			print(msg)
		except Exception as e:
			print(f"[EXCEPTION] {e}")
			break

def send_msg(msg):
	message = bytes(msg, FORMAT)
	client_socket.send(message)
	if msg == "quit":
		client_socket.close()

receive_thread = threading.Thread(target=receive_msg)
receive_thread.start()

send_msg("Tim")
input()
send_msg("Hello World")
input()
send_msg("hi tim")
input()
send_msg("quit")




