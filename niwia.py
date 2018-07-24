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
        self.flagfile = os.path.join(self.directory, FLAGFILE)

    def send(self, msg):
        if self.seq >= MAXSEQ:
            # Do not send message.
            # TODO : Notify user about that
            return

        f = os.path.join(self.directory, str(self.seq))
        with open(f, "w") as file:
            file.write(msg)
        # Create flagfile after first file created
        if self.seq == 0:
            open(self.flagfile, 'a').close()
        self.seq = self.seq + 1


class Player:

    def __init__(self):
        self.s = Writer()

    def move_up(self, steps=1):
        for i in range(steps):
            self.s.send("UP")

    def move_down(self,steps=1):
        for i in range(steps):
            self.s.send("DOWN")

    def move_right(self, steps=1):
        for i in range(steps):
            self.s.send("RIGHT")

    def move_left(self, steps=1):
        for i in range(steps):
            self.s.send("LEFT")

