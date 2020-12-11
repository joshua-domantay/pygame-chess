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
        self.chessArrayPos = (x, y)
        self.chessPiece = None
    
    def setChessPiece(self, chessPiece):
        self.chessPiece = chessPiece

class ChessPiece(pg.sprite.Sprite):
    def __init__(self, game, x, y, piece, color, chessTile):
        groups = game.chessPieces
        if(color == "white"):
            groups = game.chessPieces, game.whitePieces
        else:
            groups = game.chessPieces, game.blackPieces
        pg.sprite.Sprite.__init__(self, groups)
        self.game = game
        self.piece = piece
        self.color = color
        self.load_data()
        self.updatePos(x, y)
        self.chessTile = None
        self.setChessTile(chessTile)
        self.moved = False
        self.moves = []     # Tuples (x, y)
        self.captureMoves = []
    
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
    
    def setChessTile(self, chessTile):
        if self.chessTile is not None:
            self.chessTile.chessPiece = None
        self.chessTile = chessTile
        self.chessArrayPos = self.chessTile.chessArrayPos
        self.chessTile.chessPiece = self
    
    def movePiece(self, move, chessTile):
        self.updatePos(move[0], move[1])
        self.moved = True
        self.setChessTile(chessTile)
    
    def emptyMoves(self):
        self.moves = []
        self.captureMoves = []
    
    def getCaptureMoves(self):
        self.getMoves()

    def getMoves(self):
        self.emptyMoves()
        if(self.piece == "pawn"):
            self.getPawnMoves()
        elif(self.piece == "rook"):
            self.getRookMoves()
        elif(self.piece == "knight"):
            self.getKnightMoves()
        elif(self.piece == "bishop"):
            self.getBishopMoves()
        elif(self.piece == "queen"):
            self.getQueenMoves()
        else:
            self.getKingMoves()
        
        # Test print
        print("\t" + self.color + " " + self.piece + ": ", end="")
        print(self.moves)

    def sameColorTile(self, x, y):
        return self.game.chessArray[y][x].chessPiece.color == self.color

    def emptyTile(self, x, y):
        return self.game.chessArray[y][x].chessPiece is None

    def validMove(self, move):
        if((move[0] >= 0) and (move[0] < 8)):
            if((move[1] >= 0) and (move[1] < 8)):
                return True
        return False
    
    def pawnMove(self, move):
        if self.validMove(move):
            if self.emptyTile(move[0], move[1]):
                self.moves.append(move)

    def pawnCapture(self, move):
        if self.validMove(move):
            if ((not self.emptyTile(move[0], move[1])) and (not self.sameColorTile(move[0], move[1]))):
                self.moves.append(move)
            self.captureMoves.append(move)

    # TODO: Promotion
    def getPawnMoves(self):
        moveTowards = 0
        if(self.color == "white"):
            moveTowards = -1 if self.game.whiteBottom else 1
        else:
            moveTowards = 1 if self.game.whiteBottom else -1
        
        x = self.chessArrayPos[0]
        y = self.chessArrayPos[1]
        
        # Move forward once
        move = (x, y + moveTowards)
        self.pawnMove(move)
        
        # Move forward twice
        if not self.moved:
            if(len(self.moves) > 0):    # Move forward once is not blocked
                move = (x, y + (moveTowards * 2))
                self.pawnMove(move)
        
        # Capture left diagonal
        move = (x - 1, y + moveTowards)
        self.pawnCapture(move)
        
        # Capture right diagonal
        move = (x + 1, y + moveTowards)
        self.pawnCapture(move)

    def rookMove(self, move):
        if self.emptyTile(move[0], move[1]):    # Move
            self.moves.append(move)
            self.captureMoves.append(move)
            return False
        else:
            if not self.sameColorTile(move[0], move[1]):    # Capture
                self.moves.append(move)
            self.captureMoves.append(move)
            return True

    def getRookMoves(self):
        x = self.chessArrayPos[0]
        y = self.chessArrayPos[1]

        # Move + Capture Up
        for moveY in range(y - 1, -1, -1):
            move = (x, moveY)
            if self.rookMove(move):
                break

        # Move + Capture Down
        for moveY in range(y + 1, 8, 1):
            move = (x, moveY)
            if self.rookMove(move):
                break

        # Move + Capture Left
        for moveX in range(x - 1, -1, -1):
            move = (moveX, y)
            if self.rookMove(move):
                break

        # Move + Capture Right
        for moveX in range(x + 1, 8, 1):
            move = (moveX, y)
            if self.rookMove(move):
                break

    def knightMove(self, move):
        if self.validMove(move):
            if self.emptyTile(move[0], move[1]):    # Move
                self.moves.append(move)
                self.captureMoves.append(move)
            else:
                if not self.sameColorTile(move[0], move[1]):    # Capture
                    self.moves.append(move)
                self.captureMoves.append(move)

    def getKnightMoves(self):
        x = self.chessArrayPos[0]
        y = self.chessArrayPos[1]

        # Move + Capture Up
        move = (x - 1, y - 2)
        self.knightMove(move)
        move = (x + 1, y - 2)
        self.knightMove(move)

        # Move + Capture Down
        move = (x - 1, y + 2)
        self.knightMove(move)
        move = (x + 1, y + 2)
        self.knightMove(move)

        # Move + Capture Left
        move = (x - 2, y - 1)
        self.knightMove(move)
        move = (x - 2, y + 1)
        self.knightMove(move)
        
        # Move + Capture Right
        move = (x + 2, y - 1)
        self.knightMove(move)
        move = (x + 2, y + 1)
        self.knightMove(move)

    def bishopMove(self, move):
        if self.validMove(move):
            return self.rookMove(move)
        else:
            return True

    def getBishopMoves(self):
        x = self.chessArrayPos[0]
        y = self.chessArrayPos[1]

        # Move + Capture Diagonal Up Left
        for i in range(1, 8):
            move = (x - i, y - i)
            if self.bishopMove(move):
                break

        # Move + Capture Diagonal Up Right
        for i in range(1, 8):
            move = (x + i, y - i)
            if self.bishopMove(move):
                break

        # Move + Capture Diagonal Down Left
        for i in range(1, 8):
            move = (x - i, y + i)
            if self.bishopMove(move):
                break

        # Move + Capture Diagonal Down Right
        for i in range(1, 8):
            move = (x + i, y + i)
            if self.bishopMove(move):
                break

    def getQueenMoves(self):
        self.getRookMoves()
        self.getBishopMoves()

    def kingCastling(self, pos, add):
        x = self.chessArrayPos[0]
        y = self.chessArrayPos[1]

        if not self.emptyTile(pos, y):
            rookTile = self.game.chessArray[y][pos]
            rook = rookTile.chessPiece
            if not rook.moved:
                move = (x + add, y)
                loopAdd = -1 if (add < 0) else 1
                clear = True
                for i in range(x + loopAdd, pos, loopAdd):
                    if not self.emptyTile(i, y):
                        clear = False
                        break
                if clear:
                    if(self.color == "white"):
                        if move in self.game.blackCaptureMoves:
                            return
                    else:
                        if move in self.game.whiteCaptureMoves:
                            return
                    self.moves.append(move)

    def kingMove(self, move):
        if(move != self.chessArrayPos):
            if(self.color == "white"):
                if move in self.game.blackCaptureMoves:
                    return
            else:
                if move in self.game.whiteCaptureMoves:
                    return
            self.moves.append(move)
            self.captureMoves.append(move)

    # TODO: Find moves that are able to prevent checks without leaving the king on check
    # TODO: Checkmate algorithm something that will end the game
    # TODO: Stalemate or draw algorithm that either ends the game after 50 moves rule, king vs king or king having no moves available
    def getKingMoves(self):
        x = self.chessArrayPos[0]
        y = self.chessArrayPos[1]

        # Move + Capture
        for newY in range(-1, 2, 1):
            for newX in range(-1, 2, 1):
                move = (x + newX, y + newY)
                if self.validMove(move):
                    if self.emptyTile(move[0], move[1]):
                        self.kingMove(move)
                    else:
                        if not self.sameColorTile(move[0], move[1]):
                            self.kingMove(move)
        
        # Castling
        if not self.moved:
            # Left rook
            self.kingCastling(0, -2)

            # Right rook
            self.kingCastling(7, 2)
