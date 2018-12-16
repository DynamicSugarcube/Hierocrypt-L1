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
		print("Connected client: " + str(client_address))
		
		received_data = client_connection.recv(conn.NBYTES)
		client_data = pickle.loads(received_data)
		data = client_data[0]
		keys = client_data[1]
		decrypted = hierocrypt_l1.decrypt(data, keys)
		
		print("Received data:\n")
		print(decrypted)
		
		client_connection.close()
		
	sock.close()

if __name__ == "__main__":
	main()
