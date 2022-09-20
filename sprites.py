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

def check_move_bounds(move):
    if(((move[0] >= 0) and (move[0] <= 7)) and ((move[1] >= 0) and (move[1] <= 7))):
        return True
    return False

def reset_moves(chessPiece):
    chessPiece.possibleMoves.clear()
    chessPiece.captureMoves.clear()

# TODO: Add en passant
class Pawn(pg.sprite.Sprite):
    def __init__(self, game, color, dir, x, y):
        pg.sprite.Sprite.__init__(self, game.all_sprites)
        self.x = x
        self.y = y
        self.game = game
        self.piece = "pawn"
        self.color = color
        self.dir = dir
        self.load_data()

    def load_data(self):
        self.get_image()
        self.rect.topleft = (self.x * self.game.tilesize, self.y * self.game.tilesize)
        self.possibleMoves = []
        self.captureMoves = []
        self.moved = False
        self.moveCount = 0      # Use for en passant
    
    def get_image(self):
        sY = 0
        if(self.color == "black"):
            sY = 1
        self.image = self.game.spritesheet.get_image(0, (sY * TILESIZE), TILESIZE, TILESIZE)
        self.image = pg.transform.scale(self.image, (self.game.tilesize, self.game.tilesize))
        self.rect = self.image.get_rect()
    
    def move(self, x, y):
        self.x = x
        self.y = y
        self.moved = True
        self.moveCount += 1
        self.rect.topleft = (x * self.game.tilesize, y * self.game.tilesize)

    def get_moves(self):
        reset_moves(self)
        if(self.dir == "down"):
            move = (self.x, (self.y + 1))
            self.check_move(move, False)
            if(not self.moved):     # 2 moves forward
                move = (self.x, (self.y + 2))
                self.check_move(move, False)
            
            # Capture moves
            move = ((self.x - 1), (self.y + 1))
            self.check_move(move, True)
            move = ((self.x + 1), (self.y + 1))
            self.check_move(move, True)
        else:
            move = (self.x, (self.y - 1))
            self.check_move(move, False)
            if(not self.moved):     # 2 moves forward
                move = (self.x, (self.y - 2))
                self.check_move(move, False)
            
            # Capture moves
            move = ((self.x - 1), (self.y - 1))
            self.check_move(move, True)
            move = ((self.x + 1), (self.y - 1))
            self.check_move(move, True)
    
    def check_move(self, move, capture):
        if(check_move_bounds(move)):
            if capture:
                self.captureMoves.append(move)
                if(self.game.chessMatrix[move[1]][move[0]] != None):
                    self.possibleMoves.append(move)
            else:
                if(self.game.chessMatrix[move[1]][move[0]] == None):
                    self.possibleMoves.append(move)
    
class Rook(pg.sprite.Sprite):
    def __init__(self, game, color, x, y):
        pg.sprite.Sprite.__init__(self, game.all_sprites)
        self.x = x
        self.y = y
        self.game = game
        self.piece = "rook"
        self.color = color
        self.load_data()

    def load_data(self):
        self.get_image()
        self.rect.topleft = (self.x * self.game.tilesize, self.y * self.game.tilesize)
        self.possibleMoves = []
        self.captureMoves = []      # all moves
        self.moved = False
    
    def get_image(self):
        sY = 0
        if(self.color == "black"):
            sY = 1
        self.image = self.game.spritesheet.get_image(TILESIZE, (sY * TILESIZE), TILESIZE, TILESIZE)
        self.image = pg.transform.scale(self.image, (self.game.tilesize, self.game.tilesize))
        self.rect = self.image.get_rect()
    
    def move(self, x, y):
        self.x = x
        self.y = y
        self.moved = True
        self.rect.topleft = (x * self.game.tilesize, y * self.game.tilesize)

    def get_moves(self):
        reset_moves(self)
    
    def check_move(self, move):
        pass
    
class Knight(pg.sprite.Sprite):
    def __init__(self, game, color, x, y):
        pg.sprite.Sprite.__init__(self, game.all_sprites)
        self.x = x
        self.y = y
        self.game = game
        self.piece = "knight"
        self.color = color
        self.load_data()

    def load_data(self):
        self.get_image()
        self.move(self.x, self.y)
        self.possibleMoves = []
        self.captureMoves = []      # all moves
    
    def get_image(self):
        sY = 0
        if(self.color == "black"):
            sY = 1
        self.image = self.game.spritesheet.get_image((2 * TILESIZE), (sY * TILESIZE), TILESIZE, TILESIZE)
        self.image = pg.transform.scale(self.image, (self.game.tilesize, self.game.tilesize))
        self.rect = self.image.get_rect()
    
    def move(self, x, y):
        self.x = x
        self.y = y
        self.rect.topleft = (x * self.game.tilesize, y * self.game.tilesize)

    def get_moves(self):
        reset_moves(self)
    
    def check_move(self, move):
        pass
    
class Bishop(pg.sprite.Sprite):
    def __init__(self, game, color, x, y):
        pg.sprite.Sprite.__init__(self, game.all_sprites)
        self.x = x
        self.y = y
        self.game = game
        self.piece = "bishop"
        self.color = color
        self.load_data()

    def load_data(self):
        self.get_image()
        self.move(self.x, self.y)
        self.possibleMoves = []
        self.captureMoves = []      # all moves
    
    def get_image(self):
        sY = 0
        if(self.color == "black"):
            sY = 1
        self.image = self.game.spritesheet.get_image((3 * TILESIZE), (sY * TILESIZE), TILESIZE, TILESIZE)
        self.image = pg.transform.scale(self.image, (self.game.tilesize, self.game.tilesize))
        self.rect = self.image.get_rect()
    
    def move(self, x, y):
        self.x = x
        self.y = y
        self.rect.topleft = (x * self.game.tilesize, y * self.game.tilesize)

    def get_moves(self):
        reset_moves(self)
    
    def check_move(self, move):
        pass
    
class Queen(pg.sprite.Sprite):
    def __init__(self, game, color, x, y):
        pg.sprite.Sprite.__init__(self, game.all_sprites)
        self.x = x
        self.y = y
        self.game = game
        self.piece = "queen"
        self.color = color
        self.load_data()

    def load_data(self):
        self.get_image()
        self.move(self.x, self.y)
        self.possibleMoves = []
        self.captureMoves = []      # all moves
    
    def get_image(self):
        sY = 0
        if(self.color == "black"):
            sY = 1
        self.image = self.game.spritesheet.get_image((4 * TILESIZE), (sY * TILESIZE), TILESIZE, TILESIZE)
        self.image = pg.transform.scale(self.image, (self.game.tilesize, self.game.tilesize))
        self.rect = self.image.get_rect()
    
    def move(self, x, y):
        self.x = x
        self.y = y
        self.rect.topleft = (x * self.game.tilesize, y * self.game.tilesize)

    def get_moves(self):
        reset_moves(self)
    
    def check_move(self, move):
        pass
    
class King(pg.sprite.Sprite):
    def __init__(self, game, color, x, y):
        pg.sprite.Sprite.__init__(self, game.all_sprites)
        self.x = x
        self.y = y
        self.game = game
        self.piece = "king"
        self.color = color
        self.load_data()

    def load_data(self):
        self.get_image()
        self.rect.topleft = (self.x * self.game.tilesize, self.y * self.game.tilesize)
        self.possibleMoves = []
        self.captureMoves = []      # all moves
        self.moved = False
    
    def get_image(self):
        sY = 0
        if(self.color == "black"):
            sY = 1
        self.image = self.game.spritesheet.get_image((5 * TILESIZE), (sY * TILESIZE), TILESIZE, TILESIZE)
        self.image = pg.transform.scale(self.image, (self.game.tilesize, self.game.tilesize))
        self.rect = self.image.get_rect()
    
    def move(self, x, y):
        self.x = x
        self.y = y
        self.moved = True
        self.rect.topleft = (x * self.game.tilesize, y * self.game.tilesize)

    def get_moves(self):
        reset_moves(self)
    
    def check_move(self, move):
        pass
    