import socket
import threading 

# GLOBAL CONSTANTS
HOST = "192.168.75.1"
PORT = 5500
BUFSIZE = 1024
FORMAT = "utf-8"
ADDR = (HOST, PORT)

# GLOBAL VARIABLES 
clients = {}
addresses = {}

# Initiate Server
SERVER = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
SERVER.bind(ADDR)

def broadcast(msg, name=""):
	"""
	Send the message to every connected clients 
	args:: message, name
	return:: None 
	"""
	for socket in clients:
		socket.send(bytes(name+": "+msg, FORMAT))

def handle_client(client, client_addr):
	"""
	Handle connected clients
	args:: client, client address
	return:: None
	"""
	try:
		name = client.recv(BUFSIZE).decode(FORMAT)
		clients[client] = name
		client.send(bytes("If you want to quit, type 'quit' to exit.\n", FORMAT))
		broadcast(f"{name} has joined the chat!", "")
		while True:
			msg_recv = client.recv(BUFSIZE)
			if msg_recv != bytes("quit", FORMAT):
				message = msg_recv.decode(FORMAT)
				broadcast(message, name)
			else:
				client.close()
				del clients[client]		
				print(f"[DISCONNECTED] {name} has disconnected.")
				message = f"{name} has left the chat!"
				broadcast(message, "")
				break 
	except Exception as e:
		print(f"[EXCEPTION] {e}")

def accept_incoming_connections():
	"""
	Wait for incoming connections 
	args:: None
	return:: None
	"""

	while True:
		client, client_addr = SERVER.accept() 
		# Send welcome_msg to client
		welcome_msg = bytes("Welcome to the server!", FORMAT)
		client.send(welcome_msg)
		print(f"[CONNECTED] {client_addr} is connected.")
		addresses[client] = client_addr
		# Start handle_client thread
		thread = threading.Thread(target=handle_client, args=(client, client_addr))
		thread.start()

if __name__ == "__main__":
	SERVER.listen(10)
	print(f"[STARTING] Server is hosted on {ADDR}")
	new_thread = threading.Thread(target=accept_incoming_connections)
	new_thread.start()
	new_thread.join()
	SERVER.close()