"""
Title:          Pygame Chess
Author:         Joshua Anthony Domantay
Description:    Chess made with Python and Pygame. Practice using Github and Python.
Date:           25 November 2020
"""
import os
import random
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
        game_folder = os.path.dirname(__file__)
        imgs_dir = os.path.join(game_folder, "imgs")

        self.spritesheet = Spritesheet(os.path.join(imgs_dir, SPRITESHEET_IMG))

    def new(self):
        # Groups
        self.chessTiles = pg.sprite.Group()
        self.chessPieces = pg.sprite.Group()

        self.setChessArray()
        self.setChessPieces()

        self.playing = True

        self.turn = "white"
        self.selectedPiece = None
        self.moving = False

        self.printTurn()
        self.run()

    def swapTurn(self):
        self.turn = "white" if (self.turn == "black") else "black"
        self.printTurn()
    
    def printTurn(self):
        os.system("cls")
        print("Pygame Chess")
        print("Turn: " + self.turn.title())
        self.printChessArray()

    def setChessArray(self):
        self.chessArray = [ [], [], [], [], [], [], [], [] ]
        for y in range(8):
            for x in range(8):
                tile = ChessTile(self, x, y)
                self.chessArray[y].append(tile)

    def printChessArray(self):
        for y in range(8):
            for x in range(8):
                info = ""
                if self.chessArray[y][x].chessPiece is None:
                    info = "Null"
                else:
                    info = self.chessArray[y][x].chessPiece.color + " " + self.chessArray[y][x].chessPiece.piece
                print("{:15}".format(info), end="")
            print()

    def setChessPieces(self):
        self.whiteBottom = (random.randint(1, 2) % 2) == 0

        nonPawns = []
        if self.whiteBottom:
            nonPawns = ["rook", "knight", "bishop", "queen",
                        "king", "bishop", "knight", "rook"]
        else:
            nonPawns = ["rook", "knight", "bishop", "king",
                        "queen", "bishop", "knight", "rook"]

        black = self.whiteBottom
        # Top chess pieces
        for x in range(8):
            # Nonpawns
            ChessPiece(self, x, 0, nonPawns[x], "black" if black else "white", self.chessArray[0][x])

            # Pawns
            ChessPiece(self, x, 1, "pawn", "black" if black else "white", self.chessArray[1][x])
        
        black = not black
        # Bottom chess pieces
        for x in range(8):
            # Pawns
            ChessPiece(self, x, 6, "pawn", "black" if black else "white", self.chessArray[6][x])

            # Nonpawns
            ChessPiece(self, x, 7, nonPawns[x], "black" if black else "white", self.chessArray[7][x])
                    
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
            if(event.type == pg.MOUSEBUTTONUP):
                self.getPieceMove()
    
    def getPieceMove(self):
        pos = pg.mouse.get_pos()
        if not self.moving:
            for i in self.chessTiles:
                if i.chessPiece is not None:
                    i.chessPiece.emptyMoves()
                    if i.rect.collidepoint(pos):
                        if(i.chessPiece.color == self.turn):
                            i.chessPiece.getMoves()
                            self.moving = len(i.chessPiece.moves) > 0
                            if self.moving:
                                self.selectedPiece = i.chessPiece
        else:
            for i in self.chessTiles:
                if i.rect.collidepoint(pos):
                    for move in self.selectedPiece.moves:
                        if((i.chessArrayPos[0] == move[0]) and (i.chessArrayPos[1] == move[1])):
                            # Remove chess piece from chessTile
                            if i.chessPiece is not None:
                                i.chessPiece.kill()
                                i.chessPiece = None

                            # Castling
                            if(self.selectedPiece.piece == "king"):
                                x = move[0]
                                y = move[1]
                                moveDir = x - self.selectedPiece.chessArrayPos[0]
                                if(moveDir <= -2):
                                    rookTile = self.chessArray[y][0]
                                    rook = rookTile.chessPiece
                                    rookMove = (x + 1, y)
                                    rook.movePiece(rookMove, rookTile)
                                elif(moveDir >= 2):
                                    rookTile = self.chessArray[y][7]
                                    rook = rookTile.chessPiece
                                    rookMove = (x - 1, y)
                                    rook.movePiece(rookMove, rookTile)

                            # Update selected chess piece
                            self.selectedPiece.movePiece(move, i)

                            self.swapTurn()
                            break
            self.moving = False

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
