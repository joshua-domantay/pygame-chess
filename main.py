"""
Title:          Pygame Chess
Author:         Joshua Anthony Domantay
Description:    2D Chess that supports two players made with Pygame and Python.
Date:           14 September 2022
"""
import os
import random
import pygame as pg
from settings import *

class Game:
    def __init__(self, size):
        pg.init()
        self.load_data(size)
        self.screen = pg.display.set_mode((self.width, self.width))
        pg.display.set_caption(TITLE)
        self.clock = pg.time.Clock()

    def load_data(self, size):
        self.tilesize = TILESIZE * size
        self.width = self.tilesize * 8
        game_folder = os.path.dirname(__file__)

    def new(self):
        self.playing = True
        self.run()

    def run(self):
        while self.playing:
            self.events()
            self.update()
            self.draw()

    def update(self):
        pass
    
    def event_quit(self, event):
        if(event.type == pg.QUIT):
            pg.quit()
            quit()
        if(event.type == pg.KEYDOWN):
            if(event.key == pg.K_ESCAPE):
                pg.quit()
                quit()

    def events(self):
        for event in pg.event.get():
            self.event_quit(event)

    def draw(self):
        self.draw_tiles()
        pg.display.flip()

    def draw_tiles(self):
        lightTile = True
        for x in range(0, self.width, self.tilesize):
            for y in range(0, self.width, self.tilesize):
                rect = pg.Rect(x, y, self.tilesize, self.tilesize)
                if lightTile:
                    pg.draw.rect(self.screen, LIGHT_BROWN, rect)
                else:
                    pg.draw.rect(self.screen, DARK_BROWN, rect)
                lightTile = not lightTile
            lightTile = not lightTile

# Start
size = 2

ans = input("Change window size (Y/N)?\t> ")
if(ans.lower() == "y"):
    newSize = input("Enter window size multiplier from 1 to 4 (default 2).\t> ")
    if(newSize.isnumeric()):
        size = int(newSize)
        if(size < 1):
            size = 1
        elif(size > 4):
            size = 4

g = Game(size)
g.new()
