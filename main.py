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
    def __init__(self):
        pg.init()
        self.screen = pg.display.set_mode((WIDTH, HEIGHT))
        pg.display.set_caption(TITLE)
        self.clock = pg.time.Clock()
        self.load_data()
        # Set self.running boolean to true ??

    def load_data(self):
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
        pg.display.flip()

# Start
g = Game()
g.new()
