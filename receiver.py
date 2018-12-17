import socket
import pickle

import libcrypt
import hierocrypt_l1
import connection as conn

def main():
	sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	sock.bind((conn.HOST, conn.PORT))
	sock.listen(conn.NCLIENTS)

	while True:
		client_connection, client_address = sock.accept()
		print("Connected client:", client_address)
		
		received_data = client_connection.recv(conn.NBYTES)
		client_data = pickle.loads(received_data)
		
		f = open(conn.DUMP, 'w')
		pickle.dump(client_data, f)
		f.close
		print("Received data has been dumped.")
		
		client_connection.close()
		
	sock.close()

if __name__ == "__main__":
	main()
