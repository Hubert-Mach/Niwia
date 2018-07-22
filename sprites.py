import pygame
import time
from os import path
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
        self.step = 0
        self.move = dict()
        self.action = False

    def set_move(self, direction):
        if direction == "UP":
            motion = [self.y - TILESIZE, direction]
        elif direction == 'DOWN':
            motion = [self.y + TILESIZE, direction]
        elif direction == 'LEFT':
            motion = [self.x - TILESIZE, direction]
        elif direction == 'RIGHT':
            motion = [self.x + TILESIZE, direction]

        self.move[self.counter] = motion
        self.counter += 1

    def get_move(self):
        if len(self.move) > self.step:
            direction = self.move.get(self.step)[1]
            destination = self.move.get(self.step)[0]

            # check direction and set vx ,vy values
            #if self.move.get(self.step) is not None:
    

            if direction == 'LEFT' :
                if self.x > destination:
                    self.action = True
                    self.vx = -PLAYER_SPEED
                else:
                    # stop, correct position, increment step
                    self.x = destination 
                    self.stop_motion()
            
            elif direction == 'RIGHT' :
                if self.x < destination:
                    self.action = True
                    self.vx = PLAYER_SPEED
                else:
                    # stop, correct position, increment step
                    self.x = destination
                    self.stop_motion()

            elif direction == 'UP' :
                if self.y > destination:
                    self.action = True
                    self.vy = -PLAYER_SPEED
                else:
                    # stop, correct position, increment step
                    self.y = destination
                    self.stop_motion()

            elif direction == 'DOWN' :
                if self.y < destination:
                   self.action = True
                   self.vy = PLAYER_SPEED
                else:
                    # stop, correct position, increment step
                    self.y = self.move.get(self.step)[0]
                    self.stop_motion()

    def stop_motion(self):
        self.vx, self.vy = 0, 0
        self.step += 1
        self.action = False


    def move(self, dx=0, dy=0):
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
        if pygame.sprite.spritecollideany(self,self.game.walls):
            self.x -= self.vx * self.game.dt
            self.y -= self.vy * self.game.dt
            self.rect.topleft = (self.x, self.y)
            self.stop_motion()

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
