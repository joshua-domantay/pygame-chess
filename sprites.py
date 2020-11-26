"""
Title:          Pygame Chess
Author:         Joshua Anthony Domantay
Description:    Chess made with Python and Pygame. Practice using Github and Python.
Date:           25 November 2020
"""
import pygame as pg
from settings import *

class ChessTile(pg.sprite.Sprite):
    def __init__(self, game, x, y):
        pg.sprite.Sprite.__init__(self, game.chessTiles)
        self.game = game
        self.rect = pg.Rect(0, 0, TILESIZE, TILESIZE)
        self.rect.topleft = (x * TILESIZE, y * TILESIZE)
        self.chessPiece = None

    def setChessPiece(self, chessPiece):
        self.chessPiece = chessPiece 