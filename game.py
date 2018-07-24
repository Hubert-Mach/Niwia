import os
import signal
import tkinter
import subprocess
import logging
from tkinter import *
from sprites import *
from settings import *
from tilemap import *


class Game(object):
    def __init__(self, root):
        self.playing = False
        self.root = root
        self.pid = ''
        self.seq = 0
        self.directory = TMPDIR
        self.flag = os.path.join(self.directory, FLAGFILE)
        self.width = self.root.winfo_screenwidth()
        self.height = self.root.winfo_screenheight()
        self.dw = int(self.width * WIDTH_FACTOR)
        self.dh = self.height
        self.clock = pygame.time.Clock()
        self.dt = self.clock.tick(FPS) / 1000

        # Cleaning flag. We are clean on start
        self.clean = True

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
        self.screen = pygame.display.set_mode((self.dw, self.dh))
        self.position = 0
        self.step = 1

        # Initialize level
        self.all_sprites = pygame.sprite.Group()
        self.walls = pygame.sprite.Group()
        self.player = Player(self, 5, 5)
        self.player.update()
        for x in range(3, 6):
            Wall(self, x, 3)

        self.load_data("level1")
        self.new()
        self.game_loop()

    def load_data(self, level):
        game_folder = path.dirname(__file__)
        self.map = Map(game_folder, level)

    def new(self):
        # initialize all variables and do all the setup for a new game
        self.seq = 0
        self.all_sprites = pg.sprite.Group()
        self.walls = pg.sprite.Group()
        for row, tiles in enumerate(self.map.data):
            for col, tile in enumerate(tiles):
                if tile == '1':
                    Wall(self, col, row)
                if tile == 'P':
                    print("Put player on: "+str(col)+" ,"+str(row))
                    self.player = Player(self, col, row)
        self.camera = Camera(self.map.width, self.map.height)
        self.all_sprites.update()
        self.camera.update(self.player, self.dw, self.dh)

    def game_loop(self):
        self.events()
        self.update()
        self.draw()

    def draw(self):
        self.screen.fill(BGCOLOR)
        self.draw_grid()
        for sprite in self.all_sprites:
            self.screen.blit(sprite.image, self.camera.apply(sprite))

        pygame.display.flip()

        self.pygame.after(5, self.game_loop)

    def exec(self):
        if self.playing:
            print("################## Stop play ##############################")
            self.playing = False
            self.T.config(state=NORMAL)
            self.T.config(bg="GREEN")
            self.bExe["text"] = "EXEC"
            try:
                os.kill(self.pid.pid, signal.CTRL_BREAK_EVENT)  # or signal.SIGKILL
            except OSError:
                print("Failed to kill script")
                return False

            # Reinit level
            self.new()
            self.cleanup()
        else:
            if self.clean:
                print("################## Start play ################################")
                self.playing = True
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
            if not self.player.action:
                # read file contents
                file = os.path.join(self.directory, str(self.seq))
                if os.path.isfile(self.flag):
                    if os.path.isfile(file):
                        print("Reading file: "+str(file))
                        with open(file, "r") as f:
                            event = f.read()
                            print("Read "+event+" from "+str(f.name))
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
        self.cleanup()
        sys.exit(0)

    def cleanup(self):
        self.clean = False
        # remove script file
        print("Cleaning up temp files")
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
        self.clean = True

    def update(self):
        if self.playing:
            # update portion of the game loop
            self.all_sprites.update()
            self.camera.update(self.player, self.dw, self.dh)

    def draw_grid(self):
        info_object = pygame.display.Info()
        width = info_object.current_w
        height:width = info_object.current_h
        for x in range(0, width, TILESIZE):
            pygame.draw.line(self.screen, LIGHTGREY, (x, 0), (x, height))
        for y in range(0, height, TILESIZE):
            pygame.draw.line(self.screen, LIGHTGREY, (0, y), (width, y))
