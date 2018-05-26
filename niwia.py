from settings import *
import os.path

class Player:
    
    def move_up(self):
        self.save("u")

    
    def move_down(self):
        self.save("d")

    
    def move_right(self):
        self.save("r")

    
    def move_left(self):
        self.save("l")

    
    def save(self,msg):
        fileName = self.getCommandFile()
        f = open(fileName, "a+")
        f.write(msg+"\n")
        f.close()

    
    def getCommandFile(self):
        return os.path.join(COMDIR,COMFILE)
