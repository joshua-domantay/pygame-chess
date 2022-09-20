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

        # Up
        i = (self.y - 1)
        while(i >= 0):
            move = (self.x, i)
            if self.check_move(move):
                break
            i -= 1
        
        # Down
        i = (self.y + 1)
        while(i <= 7):
            move = (self.x, i)
            if self.check_move(move):
                break
            i += 1
        
        # Left
        i = (self.x - 1)
        while(i >= 0):
            move = (i, self.y)
            if self.check_move(move):
                break
            i -= 1

        # Right
        i = (self.x + 1)
        while(i <= 7):
            move = (i, self.y)
            if self.check_move(move):
                break
            i += 1
    
    def check_move(self, move):
        if(self.game.chessMatrix[move[1]][move[0]] == None):
            self.possibleMoves.append(move)
            self.captureMoves.append(move)
        else:
            if(self.game.chessMatrix[move[1]][move[0]].color != self.color):        # If there is a piece and is not the same color, then add move
                self.possibleMoves.append(move)
                self.captureMoves.append(move)
            return True     # Stop checking moves since blocked by another piece
        return False
    
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

        # Move Up
        if((self.y - 2) >= 0):
            move = ((self.x - 1), (self.y - 2))
            self.check_move(move)
            move = ((self.x + 1), (self.y - 2))
            self.check_move(move)
        
        # Move Down
        if((self.y + 2) <= 7):
            move = ((self.x - 1), (self.y + 2))
            self.check_move(move)
            move = ((self.x + 1), (self.y + 2))
            self.check_move(move)

        # Move Left
        if((self.x - 2) >= 0):
            move = ((self.x - 2), (self.y - 1))
            self.check_move(move)
            move = ((self.x - 2), (self.y + 1))
            self.check_move(move)
        
        # Move Down
        if((self.x + 2) <= 7):
            move = ((self.x + 2), (self.y - 1))
            self.check_move(move)
            move = ((self.x + 2), (self.y + 1))
            self.check_move(move)
    
    def check_move(self, move):
        if(check_move_bounds(move)):
            if(self.game.chessMatrix[move[1]][move[0]] == None):
                self.possibleMoves.append(move)
                self.captureMoves.append(move)
            else:
                if(self.game.chessMatrix[move[1]][move[0]].color != self.color):
                    self.possibleMoves.append(move)
                    self.captureMoves.append(move)
    
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
    
    def get_moves_h(self, iX, iY, iXadd, iYadd):
        while True:
            move = (iX, iY)
            if self.check_move(move):
                break
            iX += iXadd
            iY += iYadd

    def get_moves(self):
        reset_moves(self)
        
        self.get_moves_h((self.x - 1), (self.y - 1), -1, -1)    # Diagonal Up-Left
        self.get_moves_h((self.x + 1), (self.y - 1), 1, -1)     # Diagonal Up-Right
        self.get_moves_h((self.x - 1), (self.y + 1), -1, 1)     # Diagonal Down-Left
        self.get_moves_h((self.x + 1), (self.y + 1), 1, 1)      # Diagonal Down-Right
    
    def check_move(self, move):
        if(check_move_bounds(move)):
            if(self.game.chessMatrix[move[1]][move[0]] == None):
                self.possibleMoves.append(move)
                self.captureMoves.append(move)
            else:
                if(self.game.chessMatrix[move[1]][move[0]].color != self.color):        # If there is a piece and is not the same color, then add move
                    self.possibleMoves.append(move)
                    self.captureMoves.append(move)
                return True     # Stop checking moves since blocked by another piece
            return False
        return True
    
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

    def get_rook_moves(self):
        # Up
        i = (self.y - 1)
        while(i >= 0):
            move = (self.x, i)
            if self.check_move_r(move):
                break
            i -= 1
        
        # Down
        i = (self.y + 1)
        while(i <= 7):
            move = (self.x, i)
            if self.check_move_r(move):
                break
            i += 1
        
        # Left
        i = (self.x - 1)
        while(i >= 0):
            move = (i, self.y)
            if self.check_move_r(move):
                break
            i -= 1

        # Right
        i = (self.x + 1)
        while(i <= 7):
            move = (i, self.y)
            if self.check_move_r(move):
                break
            i += 1

    def get_bishop_moves_h(self, iX, iY, iXadd, iYadd):
        while True:
            move = (iX, iY)
            if self.check_move_b(move):
                break
            iX += iXadd
            iY += iYadd
    
    def get_bishop_moves(self):
        self.get_bishop_moves_h((self.x - 1), (self.y - 1), -1, -1)     # Diagonal Up-Left
        self.get_bishop_moves_h((self.x + 1), (self.y - 1), 1, -1)      # Diagonal Up-Right
        self.get_bishop_moves_h((self.x - 1), (self.y + 1), -1, 1)      # Diagonal Down-Left
        self.get_bishop_moves_h((self.x + 1), (self.y + 1), 1, 1)       # Diagonal Down-Right

    def get_moves(self):
        reset_moves(self)
        
        self.get_rook_moves()
        self.get_bishop_moves()
    
    def check_move_r(self, move):
        if(self.game.chessMatrix[move[1]][move[0]] == None):
            self.possibleMoves.append(move)
            self.captureMoves.append(move)
        else:
            if(self.game.chessMatrix[move[1]][move[0]].color != self.color):        # If there is a piece and is not the same color, then add move
                self.possibleMoves.append(move)
                self.captureMoves.append(move)
            return True     # Stop checking moves since blocked by another piece
        return False
    
    def check_move_b(self, move):
        if(check_move_bounds(move)):
            if(self.game.chessMatrix[move[1]][move[0]] == None):
                self.possibleMoves.append(move)
                self.captureMoves.append(move)
            else:
                if(self.game.chessMatrix[move[1]][move[0]].color != self.color):        # If there is a piece and is not the same color, then add move
                    self.possibleMoves.append(move)
                    self.captureMoves.append(move)
                return True     # Stop checking moves since blocked by another piece
            return False
        return True
    
# TODO: Castling - main.py: Check if moving a same color piece will check King. Check if King capturing piece will check King. Maybe??? Check if move will capture King next turn
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

        for i in range(-1, 2, 1):
            for j in range(-1, 2, 1):
                move = ((self.x + j), (self.y + i))
                if(move != (self.x, self.y)):
                    self.check_move(move)
    
    def check_move(self, move):
        if(check_move_bounds(move)):
            if(self.game.chessMatrix[move[1]][move[0]] == None):
                self.possibleMoves.append(move)
                self.captureMoves.append(move)
            else:
                if(self.game.chessMatrix[move[1]][move[0]].color != self.color):        # If there is a piece and is not the same color, then add move
                    self.possibleMoves.append(move)
                    self.captureMoves.append(move)
    