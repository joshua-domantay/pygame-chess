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
from sprites import *

class Game:
    def __init__(self, size):
        self.tilesize = TILESIZE * size
        self.width = self.tilesize * 8

        pg.init()
        self.screen = pg.display.set_mode((self.width, self.width))
        pg.display.set_caption(TITLE)
        self.clock = pg.time.Clock()
        self.load_data()

    def load_data(self):
        game_folder = os.path.dirname(__file__)
        imgs_dir = os.path.join(game_folder, "imgs")
        self.spritesheet = Spritesheet(os.path.join(imgs_dir, "spritesheet.png"))
    
    def generate_chess_matrix(self):
        self.chessMatrix = []
        blackTop = (random.randrange(2) == 0)
        color = "white"
        dir = "down"
        if(blackTop):
            color = "black"
        swap = 0
        for i in range(8):
            row = []
            if((i == 0) or (i == 7)):       # Pieces
                row.append(Rook(self, color, 0, i))
                row.append(Knight(self, color, 1, i))
                row.append(Bishop(self, color, 2, i))
                if(blackTop):
                    row.append(Queen(self, color, 3, i))
                    row.append(King(self, color, 4, i))
                else:
                    row.append(King(self, color, 3, i))
                    row.append(Queen(self, color, 4, i))
                row.append(Bishop(self, color, 5, i))
                row.append(Knight(self, color, 6, i))
                row.append(Rook(self, color, 7, i))
                swap += 1
            elif((i == 1) or (i == 6)):     # Pawns
                for j in range(8):
                    row.append(Pawn(self, color, dir, j, i))
                swap += 1
            else:
                for j in range(8):
                    row.append(None)
            if(swap == 2):      # Basically pieces and pawns are placed so swap color and direction for pawns
                if(color == "black"):
                    color = "white"
                else:
                    color = "black"
                dir = "up"
            self.chessMatrix.append(row)

    def new(self):
        self.playing = True
        self.all_sprites = pg.sprite.Group()
        self.generate_chess_matrix()
        for i in self.all_sprites:
            if(i.piece == "king"):
                if(i.color == "white"):
                    self.king_white = i
                else:
                    self.king_black = i
        self.turnColor = "white"
        self.selectedPiece = None
        self.run()

    def run(self):
        while self.playing:
            self.events()
            self.update()
            self.draw()

    def update(self):
        pass

    def get_enemy_moves(self):
        moves = []
        for i in self.all_sprites:
            if(i.color != self.turnColor):
                i.get_moves()
                for move in i.possibleMoves:
                    moves.append(move)
        return moves

    def check_move(self):       # Can be used to see if king is in check -> not self.check_move()
        moves = self.get_enemy_moves()
        for move in moves:
            if(self.turnColor == "white"):
                if((move[0] == self.king_white.x) and (move[1] == self.king_white.y)):      # To check if next enemy move captures king
                    return False
            else:
                if((move[0] == self.king_black.x) and (move[1] == self.king_black.y)):      # To check if next enemy move captures king
                    return False
        return True

    def end_move(self):
        if(self.turnColor == "white"):
            self.turnColor = "black"
        else:
            self.turnColor = "white"
        self.selectedPiece = None
    
    def move_piece(self, move):
        prevX = self.selectedPiece.x
        prevY = self.selectedPiece.y
        prevPiece = self.chessMatrix[move[1]][move[0]]

        self.chessMatrix[prevY][prevX] = None     # Remove piece from current tile on Chess 2D array  
        toKill = self.chessMatrix[move[1]][move[0]]     # If capturing, remove enemy piece from game later if valid move
        self.selectedPiece.move(move[0], move[1])       # Move piece
        self.chessMatrix[move[1]][move[0]] = self.selectedPiece     # Move piece on Chess 2D array
        
        # Check if king is safe after move
        validMove = self.check_move()
        if(validMove):      # If valid move, kill captured piece
            if(toKill != None):
                toKill.kill()
        else:       # If not valid move, revert before move
            self.chessMatrix[prevY][prevX] = self.selectedPiece
            self.selectedPiece.move(prevX, prevY)
            self.chessMatrix[move[1]][move[0]] = prevPiece
        return validMove
    
    def is_checkmate(self):
        if(not self.check_move()):      # If check
            for i in self.all_sprites:
                if(i.color == self.turnColor):
                    i.get_moves()
                    if(len(i.possibleMoves) > 0):       # TODO: This checks piece possible moves, but not for ensuring king's safe
                        print(i.piece + " : " + i.color + " : " + str(i.x) + " : " + str(i.y))
                        for move in i.possibleMoves:
                            print(move)
                        return False
            return True
        return False
    
    def event_quit(self, event):
        if(event.type == pg.QUIT):
            pg.quit()
            quit()
        if(event.type == pg.KEYDOWN):
            if(event.key == pg.K_ESCAPE):
                pg.quit()
                quit()
        if(event.type == pg.MOUSEBUTTONUP):
            pos = pg.mouse.get_pos()
            pos = (int(pos[0] / self.tilesize), int(pos[1] / self.tilesize))        # Easier to get which tile is clicked and easier access to chessMatrix
            if(self.selectedPiece == None):     # Get moving piece
                if(self.chessMatrix[pos[1]][pos[0]] != None):       # Check if there is a piece on tile
                    if(self.chessMatrix[pos[1]][pos[0]].color == self.turnColor):       # Check if piece is the same color as turn
                        self.selectedPiece = self.chessMatrix[pos[1]][pos[0]]
                        self.selectedPiece.get_moves()
            else:
                if(pos in self.selectedPiece.possibleMoves):    # Check if possible move
                    if(self.move_piece(pos)):       # End move if success
                        self.end_move()
                        if(self.is_checkmate()):
                            print("CHECKMATE")
                    else:
                        self.selectedPiece = None
                else:
                    self.selectedPiece = None

    def events(self):
        for event in pg.event.get():
            self.event_quit(event)

    def draw(self):
        self.draw_tiles()
        self.all_sprites.draw(self.screen)
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
size = 3

ans = input("Change window size (Y/N)?\t> ")
if(ans.lower() == "y"):
    newSize = input("Enter window size multiplier from 1 to 7 (default 3).\t> ")
    if(newSize.isnumeric()):
        size = int(newSize)
        if(size < 1):
            size = 3
        elif(size > 7):
            size = 7

g = Game(size)
g.new()
