from settings import *
import logging
import socket
import sys
import os
logging.basicConfig(format='%(asctime)s %(message)s', level=logging.INFO)


class GameEvent:
    def __init__(self, vx, vy):
        self.vx = vx
        self.vy = vy


class Client:
#    def __init__(self):
        # create an INET, STREAMing socket
#        try:
#            self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#        except socket.error:
#            logging.error('Failed to create socket')
#            sys.exit()
#
#        logging.info('Socket Created')
#
#        try:
#            remote_ip = socket.gethostbyname(SERVER_ADDRESS)
#
#        except socket.gaierror:
#            # could not resolve
#            print('Hostname could not be resolved. Exiting')
#            sys.exit()
#
#        # Connect to remote server
#        self.s.connect((SERVER_ADDRESS, SERVER_PORT))
#
#        print('Socket Connected to ' + SERVER_ADDRESS + ' on ip ' + remote_ip)

    def send(self, msg):
        try:
            # Set the whole string
            self.s.sendall(msg.encode())
            return self.s.recv(4096)
        except socket.error:
            # Send failed
            logging.error('Send failed')

    def close(self):
        self.s.close()


class Writer:
    def __init__(self):
        self.seq = 0
        self.directory = TMPDIR

    def send(self, msg):
        f = os.path.join(self.directory, str(self.seq))
        file = open(f, "w")
        file.write(msg)
        file.close()
#        print("####  Wrote "+msg+" to "+f) 
        self.seq = self.seq + 1


class Player:

    def __init__(self):
        self.s = Writer()

    def move_up(self):
        self.s.send("UP")

    def move_down(self):
        self.s.send("DOWN")

    def move_right(self):
        self.s.send("RIGHT")

    def move_left(self):
        self.s.send("LEFT")

