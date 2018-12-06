import socket
import argparse
import libcrypt
import connection as conn


def main():	
	sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	sock.connect((conn.HOST, conn.PORT))
	sock.send(bytes("Hierocrypt-L1", "UTF-8"))

	data = sock.recv(conn.NBYTES)
	print(data.decode())

	sock.close()
	
def parse_arguments():
	parser=argparse.ArgumentParser()
	parser.add_argument("mess", type=int)
	arg=parser.parse_args()
	return(arg.mess)

if __name__ == "__main__":
	main()
