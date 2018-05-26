from tkinter import *
import tkinter as tk
import pygame
from pygame.locals import *
import os
from settings import *
from sprites import *
import logging
import subprocess
import sys

logging.basicConfig(format='%(asctime)s %(message)s', level=logging.INFO)



class Game:
    running = False
    def __init__(self):
        # Prepare main window and layout
        logging.debug('INIT')
        self.root = tk.Tk()
        self.clock = pygame.time.Clock()
        self.root.wm_title("OpenBox")
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()

        # Embed pygame canvas
        embed = tk.Frame(self.root, width = int(screen_width*WIDTH_FACTOR), height = screen_height)
        embed.pack(side=LEFT)
        windowid = embed.winfo_id()

        # Display options
        os.environ['SDL_WINDOWID'] = str(windowid)
        if sys.platform == "win32":
            os.environ['SDL_VIDEODRIVER'] = 'windib'
        self.root.attributes("-fullscreen", True)         

        # GUI Elements
        button = tk.Button(self.root, text="QUIT", fg="red", command=self.quit)
        button.place(x=int(screen_width*WIDTH_FACTOR)+MARGIN, y=MARGIN,width=80,height=BUTTON_HEIGHT)

        bExe = tk.Button(self.root, text="EXEC", fg="red", command=self.exec)
        bExe.place(x=int(screen_width*WIDTH_FACTOR)+MARGIN+80, y=MARGIN,width=80,height=BUTTON_HEIGHT)

        # Text widget
        S = Scrollbar(self.root)
        self.T = Text(self.root, height=200, width=int(screen_width*(1-WIDTH_FACTOR)+80), bg="GREEN",font=("Helvetica",18))
        S.pack(side=RIGHT, fill=Y)
        S.place(x=int(screen_width-20), y=(MARGIN*2)+BUTTON_HEIGHT,width=20,height=int(screen_height*TEXT_WIDGET_FACTOR))
        self.T.place(x=int(screen_width*WIDTH_FACTOR)+MARGIN, y=(MARGIN*2)+BUTTON_HEIGHT,width=int(screen_width*(1-WIDTH_FACTOR)-30),height=int(screen_height*TEXT_WIDGET_FACTOR))
        S.config(command=self.T.yview)
        self.T.config(yscrollcommand=S.set)

        # Get template code
        template = open(os.path.join("templates","level_1.template"),"r")
        self.T.insert(CURRENT, template.read())

    def exec(self):
        # Write contents of self.T to file
        filePath = os.path.join(CODEDIR,CODEFILE)
        file = open(filePath,"w") 
        file.write("### This is ugly workaround to make importing from parent dir possible\n")
        file.write("### Think of using environmental PATH as solution\n")
        file.write("import os,sys,inspect\n")
        file.write("currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))\n")
        file.write("parentdir = os.path.dirname(currentdir)\n")
        file.write("sys.path.insert(0,parentdir)\n")
        file.write(self.T.get("1.0",'end-1c'))
        file.close()  

        # now run saved file as python
        pid = subprocess.Popen([sys.executable, filePath]) # call subprocess
#        call(["python", filePath])

    def new(self):
        # initialize all variables and do all the setup for a new game
        self.all_sprites = pygame.sprite.Group()
        self.walls = pygame.sprite.Group()
        self.player = Player(self, 5, 5)
        self.player.update()
        for x in range(3, 6):
            Wall(self, x, 3)
        
    def quit(self):
        logging.debug ("Quit")
        self.running = False

    def run(self):
        # Pygame canvas
        pygame.init()
        pygame.display.init()
        infoObject = pygame.display.Info()
        self.screen = pygame.display.set_mode((infoObject.current_w,infoObject.current_h))
        self.dt = self.clock.tick(FPS) / 1000
        self.draw()

    def events(self):
        # Open file with commands
        content = ''
        filePath = os.path.join(COMDIR,COMFILE)
        if os.path.isfile(filePath):
            with open(filePath) as f:
                content = f.readlines()
                # remove whitespace characters like `\n` at the end of each line
                content = [x.strip() for x in content] 
            f.close()
            # Remove command file after reading not to read same stuff again
            os.unlink(filePath)

        # Basic movement - r(ight), l(eft), u(p), d(own)
        for c in content:
            if c == 'u':
                self.player.move(dy=-1)
                self.player.update()
            if c == 'd':
                self.player.move(dy=1)
                self.player.update()
            if c == 'l':
                self.player.move(dx=-1)
                self.player.update()
            if c == 'r':
                self.player.move(dx=1)
                self.player.update()

    def draw(self):
        self.screen.fill(BGCOLOR)
        self.draw_grid()
        self.all_sprites.draw(self.screen)
        pygame.display.flip()

    def update(self):
        # update portion of the game loop
        self.all_sprites.update()

    def draw_grid(self):
        infoObject = pygame.display.Info()
        WIDTH = infoObject.current_w
        HEIGHT = infoObject.current_h
        for x in range(0, WIDTH, TILESIZE):
            pygame.draw.line(self.screen, LIGHTGREY, (x, 0), (x, HEIGHT))
        for y in range(0, HEIGHT, TILESIZE):
            pygame.draw.line(self.screen, LIGHTGREY, (0, y), (WIDTH, y))

        

g = Game()
g.running = True
g.new()
while g.running:
    g.root.after(1,g.run)
    g.root.after(1,g.events)
    g.root.update()
