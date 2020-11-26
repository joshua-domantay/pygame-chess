"""
Title:          Pygame Chess
Author:         Joshua Anthony Domantay
Description:    Chess made with Python and Pygame. Practice using Github and Python.
Date:           25 November 2020
"""
# from os import path
# import random
import pygame as pg
from settings import *
from sprites import *

class Game:
    def __init__(self):
        pg.init()
        self.screen = pg.display.set_mode((WIDTH, HEIGHT))
        pg.display.set_caption(TITLE)
        self.clock = pg.time.Clock()
        self.load_data()
        # Set self.running boolean to true ??

    def load_data(self):
        # game_folder = path.dirname(__file__)
        # imgs_dir = path.join(game_folder, "imgs")
        pass

    def new(self):
        # Groups
        self.all_sprites = pg.sprite.Group()

        self.playing = True
        self.run()

    def run(self):
        while self.playing:
            self.events()
            self.update()
            self.draw()

    def update(self):
        # now = pg.time.get_ticks()
        self.all_sprites.update()
    
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
        self.all_sprites.draw(self.screen)
        pg.display.flip()

# Start
mode = ""
while True:
    mode = input("Enter mode (1p, 2p, exit): ")
    if((mode.lower() == "1p") or (mode.lower() == "2p") or (mode.lower() == "exit")):
        break

if((mode.lower() == "1p") or (mode.lower() == "2p")):
    g = Game()
    # g.setMode(mode) ??
    g.new()