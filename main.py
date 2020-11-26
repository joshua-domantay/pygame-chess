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
        self.chessTiles = pg.sprite.Group()
        self.chessPieces = pg.sprite.Group()

        self.setChessArray()

        self.playing = True
        self.run()

    def setChessArray(self):
        self.chessArray = [ [], [], [], [], [], [], [], [] ]
        for y in range(8):
            for x in range(8):
                tile = ChessTile(self, x, y)
                self.chessArray[y].append(tile)
                
        self.printChessArray()

    def printChessArray(self):
        for y in range(8):
            for x in range(8):
                info = ""
                if self.chessArray[y][x].chessPiece is None:
                    info = "Null"
                else:
                    info = "x"
                print("{:15}".format(info), end="")
            print()

    def run(self):
        while self.playing:
            self.events()
            self.update()
            self.draw()

    def update(self):
        # now = pg.time.get_ticks()
        self.chessPieces.update()
    
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
        self.chessPieces.draw(self.screen)
        pg.display.flip()

    def draw_tiles(self):
        lightTile = True
        for x in range(0, WIDTH, TILESIZE):
            for y in range(0, HEIGHT, TILESIZE):
                rect = pg.Rect(x, y, TILESIZE, TILESIZE)
                if lightTile:
                    pg.draw.rect(self.screen, LIGHT_BROWN, rect)
                else:
                    pg.draw.rect(self.screen, DARK_BROWN, rect)
                lightTile = not lightTile
            lightTile = not lightTile

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