import os
import signal
import tkinter
import subprocess
import logging
from tkinter import *
from sprites import *
from settings import *


class Game(object):
    def __init__(self, root):
        self.playing = FALSE
        self.root = root
        self.pid = ''
        self.seq = 0
        self.directory = TMPDIR
        self.width = self.root.winfo_screenwidth()
        self.height = self.root.winfo_screenheight()
        w = int(self.width * WIDTH_FACTOR)
        h = self.height
        self.clock = pygame.time.Clock()
        self.dt = self.clock.tick(FPS) / 1000

        # Tk init
        self.pygame = tkinter.Frame(self.root, width=int(self.width * WIDTH_FACTOR), height=self.height)
        self.pygame.pack(side=LEFT)
        root.update()

        # GUI Elements
        button = tkinter.Button(self.root, text="QUIT", fg="red", command=self.quit)
        button.place(x=int(self.width * WIDTH_FACTOR) + MARGIN, y=MARGIN, width=80, height=BUTTON_HEIGHT)

        self.bExe = tkinter.Button(self.root, text="EXEC", fg="red", command=self.exec)
        self.bExe.place(x=int(self.width * WIDTH_FACTOR) + MARGIN + 80, y=MARGIN, width=80, height=BUTTON_HEIGHT)

        # Text widget
        self.S = Scrollbar(self.root)
        self.T = Text(self.root, height=200, width=int(self.width * (1 - WIDTH_FACTOR) + 80), bg="GREEN",
                      font=("Helvetica", 18))
        self.S.pack(side=RIGHT, fill=Y)
        self.S.place(x=int(self.width - 20), y=(MARGIN * 2) + BUTTON_HEIGHT, width=20,
                     height=int(self.height * TEXT_WIDGET_FACTOR))
        self.T.place(x=int(self.width * WIDTH_FACTOR) + MARGIN, y=(MARGIN * 2) + BUTTON_HEIGHT,
                     width=int(self.width * (1 - WIDTH_FACTOR) - 30), height=int(self.height * TEXT_WIDGET_FACTOR))
        self.S.config(command=self.T.yview)
        self.T.config(yscrollcommand=self.S.set)

        # Get template code
        template = open(os.path.join("templates", "level_1.template"), "r")
        self.T.insert(CURRENT, template.read())

        # pygame init
        os.environ['SDL_WINDOWID'] = str(self.pygame.winfo_id())
        if sys.platform == "win32":
            os.environ['SDL_VIDEODRIVER'] = 'windib'
        self.root.attributes("-fullscreen", True)

        pygame.display.init()
        self.screen = pygame.display.set_mode((w, h))
        self.position = 0
        self.step = 1

        # Initialize level
        self.all_sprites = pygame.sprite.Group()
        self.walls = pygame.sprite.Group()
        self.player = Player(self, 5, 5)
        self.player.update()
        for x in range(3, 6):
            Wall(self, x, 3)

        self.game_loop()

    def game_loop(self):
        self.events()
        self.update()
        self.draw()

    def draw(self):
        self.screen.fill(BGCOLOR)
        self.draw_grid()
        self.all_sprites.draw(self.screen)
        pygame.display.flip()

        self.pygame.after(5, self.game_loop)

    def incr_step(self, inc):
        self.step += inc

    def exec(self):
        if self.playing:
            print("################## Stoping play ##############################")
            self.playing = FALSE
            self.T.config(state=NORMAL)
            self.T.config(bg="GREEN")
            self.bExe["text"] = "EXEC"
            self.seq = 0
            try:
                os.kill(self.pid.pid, signal.SIGTERM)  # or signal.SIGKILL
            except OSError:
                return False
        else:
            print("################## Start play ################################")
            self.playing = TRUE
            self.T.config(state=DISABLED)
            self.T.config(bg="BLUE")
            self.bExe["text"] = "STOP"

            # Put contents of text box to file
            script = open(CODEFILE, "w")
            script.write(self.T.get("1.0", 'end-1c'))
            script.close()
            self.pid = subprocess.Popen([sys.executable, CODEFILE])  # call subprocess

    def events(self):
        if self.playing:
            # Read next action only when no action pending
            if self.player.action == False:
                # read file contents
                file = os.path.join(self.directory, str(self.seq))
                if os.path.isfile(file):
                    #print("########## Reading file "+ str(file)+ " #############")
                    f = open(file, "r")
                    event = f.read()
                    f.close()
                    os.remove(os.path.join(self.directory, str(self.seq)))
                    self.seq += 1
    
                    if event == 'UP':
                        self.player.set_move('UP')
                        self.player.update()
                    elif event == 'DOWN':
                        self.player.set_move('DOWN')
                        self.player.update()
                    elif event == 'RIGHT':
                        self.player.set_move('RIGHT')
                        self.player.update()
                    elif event == 'LEFT':
                        self.player.set_move('LEFT')
                        self.player.update()
    
            pygame.event.clear()

    def quit(self):
        # remove script file
        if os.path.isfile(CODEFILE):
            os.remove(CODEFILE)

        # remove temporary files
        for the_file in os.listdir(self.directory):
            file_path = os.path.join(self.directory, the_file)
            try:
                if os.path.isfile(file_path):
                    os.unlink(file_path)
            except Exception as e:
                logging.error(e)
        sys.exit(0)

    def update(self):
        if self.playing:
        # update portion of the game loop
            self.all_sprites.update()

    def draw_grid(self):
        info_object = pygame.display.Info()
        WIDTH = info_object.current_w
        HEIGHT = info_object.current_h
        for x in range(0, WIDTH, TILESIZE):
            pygame.draw.line(self.screen, LIGHTGREY, (x, 0), (x, HEIGHT))
        for y in range(0, HEIGHT, TILESIZE):
            pygame.draw.line(self.screen, LIGHTGREY, (0, y), (WIDTH, y))
