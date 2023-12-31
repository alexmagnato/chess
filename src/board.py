from const import *
from square import Square
from piece import *
from move import Move
import os

class Board:

    def __init__(self):
        self.squares = [[0, 0, 0, 0, 0, 0, 0, 0] for col in range(COLS)]

        self._create()
        self._add_pieces('white')
        self._add_pieces('black')

    def calc_moves(self, piece, row, col):
        #
        #Calculates all the valid moves
        #

        def pawn_moves():
            # steps
            steps = 1 if piece.moved else 2

            # vertical moves
            start = row + piece.dir
            end = row + (piece.dir * (1 + steps))
            for possible_move_row in range(start,end, piece.dir):
                if Square.in_range(possible_move_row):
                    if self.squares[possible_move_row][col].isempty():
                        #create initial and final move square
                        initial = Square(row, col)
                        final = Square(possible_move_row, col)
                        # create a new move
                        move = Move(initial,final)
                        # append new move
                        piece.add_move(move)
                    # blocked
                    else: break
                # not in range
                else: break
                        

            # diagonal moves
            possible_move_row = row + piece.dir
            possible_move_cols = [col-1, col+1]
            for possible_move_col in possible_move_cols:
                if Square.in_range(possible_move_row, possible_move_col):
                     if self.squares[possible_move_row][possible_move_col].has_enemy_piece(piece.color):
                        #create initial and final move square
                        initial = Square(row, col)
                        final = Square(possible_move_row, possible_move_col)
                        # create a new move
                        move = Move(initial,final)
                        # append new move
                        piece.add_move(move)
           

        def knight_moves():
            # 8 possible moves
            possible_moves = [
                (row-2, col+1),
                (row-1, col+2),
                (row+1, col+2),
                (row+2, col+1),
                (row+2, col-1),
                (row+1, col-2),
                (row-1, col-2),
                (row-2, col-1),
            ]

            for possible_move in possible_moves:
                possible_move_row, possible_move_col = possible_move
                
                if Square.in_range(possible_move_row, possible_move_col):
                    if self.squares[possible_move_row][possible_move_col].isempty_or_enemy(piece.color):
                        # create Square of the new move
                        initial = Square(row, col)
                        final = Square(possible_move_row,possible_move_col) 
                        # create new move
                        move = Move(initial, final)
                        # append new valid move 
                        piece.add_move(move)

        def straightline_move(incrs):
            for incr in incrs:
                row_incr, col_incr = incr
                possible_move_row = row + row_incr
                possible_move_col = col + col_incr

                while True:
                    if Square.in_range(possible_move_row, possible_move_col):
                        
                        # create square of the possible new move
                        initial = Square (row, col)
                        final = Square (possible_move_row, possible_move_col)
                        # create a possible new move
                        move = Move(initial, final)


                        # empty squares
                        if self.squares[possible_move_row][possible_move_col].isempty():
                            # append new move
                            piece.add_move(move)

                        # has find an enemy piece
                        if self.squares[possible_move_row][possible_move_col].has_enemy_piece(piece.color):
                            # append new move
                            piece.add_move(move)
                            break

                        # has find an ally piece
                        if self.squares[possible_move_row][possible_move_col].has_team_piece(piece.color):
                            break

                    # not in range
                    else: break

                    # incrementing incrs 
                    possible_move_row = possible_move_row + row_incr
                    possible_move_col = possible_move_col + col_incr

        def king_moves():
            adjs = [
                (row-1, col+1), # up-right
                (row-1, col+0), # up
                (row-1, col-1), # up-left
                (row+0, col+1), # right
                (row+0, col-1), # left
                (row+1, col+1), # down-rigt
                (row+1, col+0), # down
                (row+1, col-1), # down-left
            ]

            for possible_move in adjs:
                possible_move_row, possible_move_col = possible_move

                if Square.in_range(possible_move_row, possible_move_col):
                    if self.squares[possible_move_row][possible_move_col].isempty_or_enemy(piece.color):
                        # create Square of the new move
                        initial = Square(row, col)
                        final = Square(possible_move_row,possible_move_col) 
                        # create new move
                        move = Move(initial, final)
                        # append new valid move 
                        piece.add_move(move)

        if isinstance(piece, Pawn): 
            pawn_moves()
        elif isinstance(piece, Knight): 
            knight_moves()        
        elif isinstance(piece, Bishop): 
            straightline_move([
                (-1, 1), # up-right
                (-1, -1), # up-left
                (1, 1), # down-right
                (1, -1) # down-left
            ])
        elif isinstance(piece, Rook): 
            straightline_move([
                (-1, 0), # up
                (0, 1), # right
                (1, 0), # down
                (0, -1) # left
            ])
        elif isinstance(piece, Queen): 
            straightline_move([
                (-1, 1), # up-right
                (-1, -1), # up-left
                (1, 1), # down-right
                (1, -1), # down-left(-1, 0)
                (-1, 0), # up
                (0, 1), # right
                (1, 0), # down
                (0, -1) # left
            ])
        elif isinstance(piece, King): 
            king_moves()

    def _create(self):
        for row in range(ROWS):
            for col in range(COLS):
                self.squares[row][col] = Square(row, col)

    def _add_pieces(self, color):
        row_pawn, row_other = (6, 7) if color == 'white' else (1,0)

        #Pawn
        for col in range(COLS):
           self.squares[row_pawn][col] = Square(row_pawn, col, Pawn(color))
        self.squares[5][1] = Square(5, 1, Pawn(color))
        #Knight
        self.squares[row_other][1] = Square(row_other, 1, Knight(color))
        self.squares[row_other][6] = Square(row_other, 6, Knight(color))

        #Bishop
        self.squares[row_other][2] = Square(row_other, 2, Bishop(color))
        self.squares[row_other][5] = Square(row_other, 5, Bishop(color))
        self.squares[3][5] = Square(3, 5, Bishop('white'))


        #Rook
        self.squares[row_other][0] = Square(row_other, 0, Rook(color))
        self.squares[row_other][7] = Square(row_other, 7, Rook(color))
        self.squares[4][4] = Square(4, 4, Rook(color))


        #Queen
        self.squares[row_other][3] = Square(row_other, 1, Queen(color))
        self.squares[5][4] = Square(row_other, 1, Queen(color))


        #King
        self.squares[row_other][4] = Square(row_other, 1, King(color))
        self.squares[5][3] = Square(5, 3, King(color))