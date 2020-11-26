"""
Title:          Pygame Chess
Author:         Joshua Anthony Domantay
Description:    Chess made with Python and Pygame. Practice using Github and Python.
Date:           25 November 2020
"""
import pygame as pg
from settings import *

class Spritesheet:
    def __init__(self, filename):
        self.sheet = pg.image.load(filename).convert()
    
    def get_image(self, x, y, w, h):
        image = pg.Surface((w, h))
        image.set_colorkey(GREEN)
        image.blit(self.sheet, (0, 0), (x, y, w, h))
        return image

class ChessTile(pg.sprite.Sprite):
    def __init__(self, game, x, y):
        pg.sprite.Sprite.__init__(self, game.chessTiles)
        self.game = game
        self.rect = pg.Rect(0, 0, TILESIZE, TILESIZE)
        self.rect.topleft = (x * TILESIZE, y * TILESIZE)
        self.chessPiece = None
    
    def setChessPiece(self, chessPiece):
        self.chessPiece = chessPiece

class ChessPiece(pg.sprite.Sprite):
    def __init__(self, game, x, y, piece, color):
        pg.sprite.Sprite.__init__(self, game.chessPieces)
        self.game = game
        self.piece = piece
        self.color = color
        self.load_data()
        self.updatePos(x, y)
        self.moves = []
    
    def load_data(self):
        self.get_image()
        self.image = pg.transform.scale(self.image, (64, 64))
        self.rect = self.image.get_rect()

    def get_image(self):
        x = 0
        y = 0

        if(self.piece == "pawn"):
            x = 0
        elif(self.piece == "rook"):
            x = 1
        elif(self.piece == "knight"):
            x = 2
        elif(self.piece == "bishop"):
            x = 3
        elif(self.piece == "queen"):
            x = 4
        else:
            x = 5
        
        if(self.color == "black"):
            y = 1
        
        self.image = self.game.spritesheet.get_image((TILESIZE * x) / 2, (TILESIZE * y) / 2, 32, 32)

    def updatePos(self, x, y):
        self.rect.topleft = (x * TILESIZE, y * TILESIZE)
    
    def emptyMoves(self):
        self.moves = []

    def getMoves(self):
        self.emptyMoves()
        if(self.piece == "pawn"):
            pass
        elif(self.piece == "rook"):
            pass
        elif(self.piece == "knight"):
            pass
        elif(self.piece == "bishop"):
            pass
        elif(self.piece == "queen"):
            pass
        else:
            pass
        
        print(self.moves)
