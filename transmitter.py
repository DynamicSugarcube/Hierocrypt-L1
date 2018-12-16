import socket
import pickle
import argparse
import random

import libcrypt
import connection as conn
import hierocrypt_l1

def main():
	args = parse_arguments()
	
	data = ''
	if (args.message):
		data += args.message
	if (args.path):
		f = open(args.path	, 'r')
		data += f.read()
		f.close()
	if (data == ''):
		print('Nothing to send')
		return
	
	keys = [random.getrandbits(hierocrypt_l1.KEY_SIZE) for i in range(6)]
	encrypted = hierocrypt_l1.encrypt(bytearray(data, encoding = conn.ENCODING), keys)
		
	sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	sock.connect((conn.HOST, conn.PORT))
	
	package = pickle.dumps((encrypted, keys))
	sock.send(package)

	data = sock.recv(conn.NBYTES)
	print(data.decode())

	sock.close()
	
def parse_arguments():
	parser = argparse.ArgumentParser()
	parser.add_argument('-m', '--message', action = 'store')
	parser.add_argument('-p', '--path', action = 'store')
	args = parser.parse_args()
	return args

if __name__ == "__main__":
	main()
