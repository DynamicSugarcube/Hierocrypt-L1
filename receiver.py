import socket

import libcrypt
import connection as conn

def main():
	sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	sock.bind((conn.HOST, conn.PORT))
	sock.listen(conn.NCLIENTS)

	while True:
		client_connection, client_address = sock.accept()
		print("Connected client: " + str(client_address))
		client_data = client_connection.recv(conn.NBYTES)
		print("Received data:\n" + client_data.decode())
		client_connection.close()
		
	sock.close()

if __name__ == "__main__":
	main()
