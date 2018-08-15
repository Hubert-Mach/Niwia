from settings import *
import logging
import os
logging.basicConfig(format='%(asctime)s %(message)s', level=logging.INFO)


class GameEvent:
    def __init__(self, vx, vy):
        self.vx = vx
        self.vy = vy


class Writer:

    class __Writer:
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

    instance = None

    def __init__(self):
        if not Writer.instance:
            Writer.instance = Writer.__Writer()

    def __getattr__(self, name):
        return getattr(self.instance, name)


class Player:

    def __init__(self):
        self.s = Writer()

    def move_up(self, steps=1):
        for i in range(steps):
            self.s.send("UP")

    def move_down(self, steps=1):
        for i in range(steps):
            self.s.send("DOWN")

    def move_right(self, steps=1):
        for i in range(steps):
            self.s.send("RIGHT")

    def move_left(self, steps=1):
        for i in range(steps):
            self.s.send("LEFT")

