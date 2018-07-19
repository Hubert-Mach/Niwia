import pygame
import time
from settings import *


class Player(pygame.sprite.Sprite):
    def __init__(self, game, x, y):
        self.groups = game.all_sprites
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = pygame.Surface((TILESIZE, TILESIZE))
        self.image.fill(YELLOW)
        self.rect = self.image.get_rect()
        self.vx, self.vy = 0, 0
        self.x = x * TILESIZE
        self.y = y * TILESIZE
        self.counter = 0
        self.position = 0
        self.move = dict()

    def set_move(self, direction):
        motion = [TILESIZE, direction]
        self.move[self.counter] = motion
        self.counter += 1

    def get_move(self):
        #print("get_move")
        #print(self.counter)
        if len(self.move) > self.position:
            print(self.move)
            print("Counter is "+str(self.position))
            movement = self.move.get(self.position)
            print("Movement")
            print(movement)
            if movement[0] > 0:

                # check direction and set vx ,vy values
                if self.move.get(self.position)[1] == 'LEFT':
                    self.vx = -PLAYER_SPEED
                if self.move.get(self.position)[1] == 'RIGHT':
                    self.vx = PLAYER_SPEED
                if self.move.get(self.position)[1] == 'UP':
                    self.vy = -PLAYER_SPEED
                if self.move.get(self.position)[1] == 'DOWN':
                    self.vy = PLAYER_SPEED

                self.move[self.position][0] = self.move[self.position][0] - 1
                # if we have reached 0 increase position
                if self.move.get(self.position)[0] == 0:
                    self.position += 1
        else:
            self.vx, self.vy = 0, 0

    def move(self, dx=0, dy=0):
        if not self.collide_with_walls(dx, dy):
            self.x += dx
            self.y += dy

    def collide_with_walls(self, dx=0, dy=0):
        for wall in self.game.walls:
            print("W: "+str(wall.x)+","+str(wall.y))
            if wall.x == self.x + dx and wall.y == self.y + dy:
                print("COLLISION AT: "+str(self.x+dx)+","+str(self.y+dy)+" with wall at "+str(wall.x)+","+str(wall.y))
                return True
        return False

    def update(self):
        self.get_move()
        self.x += self.vx * self.game.dt
        self.y += self.vy * self.game.dt
        self.rect.topleft = (self.x, self.y)
        #print ("Set position to "+str(self.x) +" , "+str(self.y))


class Wall(pygame.sprite.Sprite):
    def __init__(self, game, x, y):
        self.groups = game.all_sprites, game.walls
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = pygame.Surface((TILESIZE, TILESIZE))
        self.image.fill(GREEN)
        self.rect = self.image.get_rect()
        self.x = x
        self.y = y
        self.rect.x = x * TILESIZE
        self.rect.y = y * TILESIZE
