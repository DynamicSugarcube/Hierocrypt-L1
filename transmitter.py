import socket
import argparse

import libcrypt
import connection as conn
import hierocrypt_l1

ENCODING = "ASCII"

def main():
	data = parse_arguments()
	encrypted = hierocrypt_l1.encrypt(bytearray(data, encoding="ASCII"))
		
	sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	sock.connect((conn.HOST, conn.PORT))
	sock.send(bytes(encrypted))

	data = sock.recv(conn.NBYTES)
	print(data.decode())

	sock.close()
	
def parse_arguments():
	parser=argparse.ArgumentParser()
	parser.add_argument("message", type=str)
	arg=parser.parse_args()
	return(arg.message)

if __name__ == "__main__":
	main()
