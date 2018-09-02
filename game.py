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

        # In game buttons
        self.execButton = tkinter.Button(self.root, text="EXEC", fg="red", command=self.exec, cursor="hand2")
        self.showMenu = tkinter.Button(self.root, text="MAP", fg="red", command=self.showMap)

        # Text widget
        self.S = Scrollbar(self.root)
        self.T = Text(self.root, height=200, width=int(self.width * (1 - WIDTH_FACTOR) + 80), bg="GREEN",
                      font=("Helvetica", 18))
        self.S.place(x=int(self.width - 20), y=(MARGIN * 2) + BUTTON_HEIGHT, width=20,
                     height=int(self.height * TEXT_WIDGET_FACTOR))
        self.T.place(x=int(self.width * WIDTH_FACTOR) + MARGIN, y=(MARGIN * 2) + BUTTON_HEIGHT,
                     width=int(self.width * (1 - WIDTH_FACTOR) - 30), height=int(self.height * TEXT_WIDGET_FACTOR))
        self.S.config(command=self.T.yview)
        self.T.config(yscrollcommand=self.S.set)


        # Embed svg image: https://stackoverflow.com/questions/22583035/can-you-display-an-image-inside-of-a-python-program-without-using-pygame
        self.canvas = Canvas(root, width=self.width, height=self.height,)
        self.canvas.place(x=0, y=0)

        # Map buttons
        self.level1Button = tkinter.Button(self.root, text="1", fg="red", command=lambda: self.load_data("1"))
        self.level2Button = tkinter.Button(self.root, text="2", fg="red", command=lambda: self.load_data("2"))
        self.quitButton = tkinter.Button(self.root, text="QUIT", fg="red", command=self.quit)
        
        self.placeMapButtons()

        #self.showMenu.place(x=int(self.width / 2 - 100) + MARGIN, y=MARGIN, width=80, height=BUTTON_HEIGHT)

        #canvas.delete(canvas_id)
        #canvas.pack_forget()

        self.placeButtons()

        # pygame init
        os.environ['SDL_WINDOWID'] = str(self.pygame.winfo_id())
        if sys.platform == "win32":
            os.environ['SDL_VIDEODRIVER'] = 'windib'
        self.root.attributes("-fullscreen", True)

        pygame.display.init()
        self.screen = pygame.display.set_mode((self.dw, self.dh))
        self.position = 0
        self.step = 1

        # initialy load level 1
        game_folder = path.dirname(__file__)
        #self.map = Map(game_folder, "1")
        self.map = TiledMap(os.path.join(game_folder, "levels", "1", "map.tmx"))
        self.map_img = self.map.make_map()
        self.map_rect = self.map_img.get_rect()
        self.new()
        self.game_loop()

    def placeButtons(self):
        self.quitButton.place(x=int(self.width) - MARGIN - 80, y=MARGIN, width=80, height=BUTTON_HEIGHT)
        self.execButton.place(x=int(self.width * WIDTH_FACTOR) + MARGIN + 80, y=MARGIN, width=80, height=BUTTON_HEIGHT)

    def load_data(self, level):
        # Load map
        game_folder = path.dirname(__file__)
        map_folder = os.path.join(game_folder, "levels")
        self.map = TiledMap(os.path.join(map_folder, level, "map.tmx"))
        self.map_img = self.map.make_map()
        self.map_rect = self.map_img.get_rect()
        # Clean text widget
        self.T.delete('1.0', END)
        # Read and put template code to text widget
        template = open(os.path.join("levels", str(level), "code.template"), "r")
        self.T.insert(CURRENT, template.read())
        # Hide overlay
        self.hide()

        # start new game
        self.new()

    def new(self):
        # initialize all variables and do all the setup for a new game
        self.seq = 0
        self.all_sprites = pg.sprite.Group()
        self.walls = pg.sprite.Group()
        #for row, tiles in enumerate(self.map.data):
        #    for col, tile in enumerate(tiles):
        #        if tile == '1':
        #            Wall(self, col, row)
        #        if tile == 'P':
        #            print("Put player on: "+str(col)+" ,"+str(row))
        #            self.player = Player(self, col, row)
        for tile_object in self.map.tmxdata.objects:
            if tile_object.name == "Player":
                self.player = Player(self, tile_object.x, tile_object.y)
            if tile_object.name == "wall":
                Obstacle(self, tile_object.x, tile_object.y,
                         tile_object.width, tile_object.height)
        self.camera = Camera(self.map.width, self.map.height)
        self.all_sprites.update()
        self.camera.update(self.player, self.dw, self.dh)

    def game_loop(self):
        self.events()
        self.update()
        self.draw()

    def draw(self):
        #self.screen.fill(BGCOLOR)
        self.screen.blit(self.map_img, self.camera.apply_rect(self.map_rect))
        #self.draw_grid()
        for sprite in self.all_sprites:
            self.screen.blit(sprite.image, self.camera.apply(sprite))

        pygame.display.flip()

        self.pygame.after(5, self.game_loop)

    def startPlay(self):
        self.cleanup()
        print("################## Start play ################################")
        self.playing = True
        self.T.config(state=DISABLED)
        self.T.config(bg="BLUE")
        self.execButton["text"] = "STOP"

        # Put contents of text box to file
        script = open(CODEFILE, "w")
        script.write(self.T.get("1.0", 'end-1c'))
        script.close()
        self.pid = subprocess.Popen([sys.executable, CODEFILE])  # call subprocess

    def stopPlay(self):
        print("################## Stop play ##############################")
        self.playing = False
        self.T.config(state=NORMAL)
        self.T.config(bg="GREEN")
        self.execButton["text"] = "EXEC"
        try:
            if sys.platform == "win32":
                os.kill(self.pid.pid, signal.CTRL_BREAK_EVENT)
            else:
                os.kill(self.pid.pid, signal.SIGKILL)
        except OSError:
            print("Failed to kill script")
            return False

        # Reinit level
        self.new()
        self.cleanup()

    def exec(self):
        if self.playing:
            self.stopPlay()
        else:
            self.startPlay()

    def makeEmptyResponse(self, seq):
        r = os.path.join(self.directory, str(seq)+"r")
        open(r, 'a').close()

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


                        if event == 'UP':
                            self.player.set_move('UP')
                            self.player.update()
                            self.makeEmptyResponse(self.seq)
                        elif event == 'DOWN':
                            self.player.set_move('DOWN')
                            self.player.update()
                            self.makeEmptyResponse(self.seq)
                        elif event == 'RIGHT':
                            self.player.set_move('RIGHT')
                            self.player.update()
                            self.makeEmptyResponse(self.seq)
                        elif event == 'LEFT':
                            self.player.set_move('LEFT')
                            self.player.update()
                            self.makeEmptyResponse(self.seq)
                        os.remove(file)
                        self.seq += 1
            pygame.event.clear()

    def hide(self):
        # Destroy overlay and level buttons
        self.canvas.destroy()
        self.level1Button.destroy()
        self.level2Button.destroy()
        self.showMenu = tkinter.Button(self.root, text="MAP", fg="red", command=self.showMap)
        self.showMenu.place(x=int(self.width * WIDTH_FACTOR) + MARGIN, y=MARGIN, width=80, height=BUTTON_HEIGHT)

    def showMap(self):
        self.canvas = Canvas(self.root, width=self.width, height=self.height,)
        self.canvas.place(x=0, y=0)
        self.showMenu.destroy()
        # Map buttons
        self.level1Button = tkinter.Button(self.root, text="1", fg="red", command=lambda: self.load_data("1"))
        self.level2Button = tkinter.Button(self.root, text="2", fg="red", command=lambda: self.load_data("2"))
        self.quitButton = tkinter.Button(self.root, text="QUIT", fg="red", command=self.quit)
        self.placeMapButtons()

    def placeMapButtons(self):
        self.level1Button.place(x=20, y=MARGIN , width=80, height=BUTTON_HEIGHT)
        self.level2Button.place(x=20, y=MARGIN + 80 , width=80, height=BUTTON_HEIGHT)
        self.quitButton.place(x=int(self.width) - MARGIN - 80, y=MARGIN, width=80, height=BUTTON_HEIGHT)

    def quit(self):
        if self.playing:
            self.stopPlay()
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
        height = info_object.current_h
        for x in range(0, width, TILESIZE):
            pygame.draw.line(self.screen, LIGHTGREY, (x, 0), (x, height))
        for y in range(0, height, TILESIZE):
            pygame.draw.line(self.screen, LIGHTGREY, (0, y), (width, y))
