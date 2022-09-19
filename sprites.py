"""
Title:          Pygame Chess
Author:         Joshua Anthony Domantay
Description:    2D Chess that supports two players made with Pygame and Python.
Date:           14 September 2022
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

class Pawn(pg.sprite.Sprite):
    def __init__(self, game, color, dir, x, y):
        pg.sprite.Sprite.__init__(self, game.all_sprites)
        self.game = game
        self.piece = "pawn"
        self.color = color
        self.dir = dir
        self.load_data(x, y)

    def load_data(self, x, y):
        self.get_image()
        self.update_pos(x, y)
        self.allMoves = []
        self.possibleMoves = []
    
    def get_image(self):
        sY = 0
        if(self.color == "black"):
            sY = 1
        self.image = self.game.spritesheet.get_image(0, (sY * TILESIZE), TILESIZE, TILESIZE)
        self.image = pg.transform.scale(self.image, (self.game.tilesize, self.game.tilesize))
        self.rect = self.image.get_rect()
    
    def update_pos(self, x, y):
        self.rect.topleft = (x * self.game.tilesize, y * self.game.tilesize)

    def get_moves(self):
        self.reset_moves()

    def reset_moves(self):
        self.allMoves.clear()
        self.possibleMoves.clear()
    
class Rook(pg.sprite.Sprite):
    def __init__(self, game, color, x, y):
        pg.sprite.Sprite.__init__(self, game.all_sprites)
        self.game = game
        self.piece = "rook"
        self.color = color
        self.load_data(x, y)

    def load_data(self, x, y):
        self.get_image()
        self.update_pos(x, y)
        self.allMoves = []
        self.possibleMoves = []
    
    def get_image(self):
        sY = 0
        if(self.color == "black"):
            sY = 1
        self.image = self.game.spritesheet.get_image(TILESIZE, (sY * TILESIZE), TILESIZE, TILESIZE)
        self.image = pg.transform.scale(self.image, (self.game.tilesize, self.game.tilesize))
        self.rect = self.image.get_rect()
    
    def update_pos(self, x, y):
        self.rect.topleft = (x * self.game.tilesize, y * self.game.tilesize)

    def get_moves(self):
        self.reset_moves()

    def reset_moves(self):
        self.allMoves.clear()
        self.possibleMoves.clear()
    
class Knight(pg.sprite.Sprite):
    def __init__(self, game, color, x, y):
        pg.sprite.Sprite.__init__(self, game.all_sprites)
        self.game = game
        self.piece = "knight"
        self.color = color
        self.load_data(x, y)

    def load_data(self, x, y):
        self.get_image()
        self.update_pos(x, y)
        self.allMoves = []
        self.possibleMoves = []
    
    def get_image(self):
        sY = 0
        if(self.color == "black"):
            sY = 1
        self.image = self.game.spritesheet.get_image((2 * TILESIZE), (sY * TILESIZE), TILESIZE, TILESIZE)
        self.image = pg.transform.scale(self.image, (self.game.tilesize, self.game.tilesize))
        self.rect = self.image.get_rect()
    
    def update_pos(self, x, y):
        self.rect.topleft = (x * self.game.tilesize, y * self.game.tilesize)

    def get_moves(self):
        self.reset_moves()

    def reset_moves(self):
        self.allMoves.clear()
        self.possibleMoves.clear()
    
class Bishop(pg.sprite.Sprite):
    def __init__(self, game, color, x, y):
        pg.sprite.Sprite.__init__(self, game.all_sprites)
        self.game = game
        self.piece = "bishop"
        self.color = color
        self.load_data(x, y)

    def load_data(self, x, y):
        self.get_image()
        self.update_pos(x, y)
        self.allMoves = []
        self.possibleMoves = []
    
    def get_image(self):
        sY = 0
        if(self.color == "black"):
            sY = 1
        self.image = self.game.spritesheet.get_image((3 * TILESIZE), (sY * TILESIZE), TILESIZE, TILESIZE)
        self.image = pg.transform.scale(self.image, (self.game.tilesize, self.game.tilesize))
        self.rect = self.image.get_rect()
    
    def update_pos(self, x, y):
        self.rect.topleft = (x * self.game.tilesize, y * self.game.tilesize)

    def get_moves(self):
        self.reset_moves()

    def reset_moves(self):
        self.allMoves.clear()
        self.possibleMoves.clear()
    
class Queen(pg.sprite.Sprite):
    def __init__(self, game, color, x, y):
        pg.sprite.Sprite.__init__(self, game.all_sprites)
        self.game = game
        self.piece = "queen"
        self.color = color
        self.load_data(x, y)

    def load_data(self, x, y):
        self.get_image()
        self.update_pos(x, y)
        self.allMoves = []
        self.possibleMoves = []
    
    def get_image(self):
        sY = 0
        if(self.color == "black"):
            sY = 1
        self.image = self.game.spritesheet.get_image((4 * TILESIZE), (sY * TILESIZE), TILESIZE, TILESIZE)
        self.image = pg.transform.scale(self.image, (self.game.tilesize, self.game.tilesize))
        self.rect = self.image.get_rect()
    
    def update_pos(self, x, y):
        self.rect.topleft = (x * self.game.tilesize, y * self.game.tilesize)

    def get_moves(self):
        self.reset_moves()

    def reset_moves(self):
        self.allMoves.clear()
        self.possibleMoves.clear()
    
class King(pg.sprite.Sprite):
    def __init__(self, game, color, x, y):
        pg.sprite.Sprite.__init__(self, game.all_sprites)
        self.game = game
        self.piece = "king"
        self.color = color
        self.load_data(x, y)

    def load_data(self, x, y):
        self.get_image()
        self.update_pos(x, y)
        self.allMoves = []
        self.possibleMoves = []
    
    def get_image(self):
        sY = 0
        if(self.color == "black"):
            sY = 1
        self.image = self.game.spritesheet.get_image((5 * TILESIZE), (sY * TILESIZE), TILESIZE, TILESIZE)
        self.image = pg.transform.scale(self.image, (self.game.tilesize, self.game.tilesize))
        self.rect = self.image.get_rect()
    
    def update_pos(self, x, y):
        self.rect.topleft = (x * self.game.tilesize, y * self.game.tilesize)

    def get_moves(self):
        self.reset_moves()

    def reset_moves(self):
        self.allMoves.clear()
        self.possibleMoves.clear()
    