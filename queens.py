"""
Author: Trevor Stalnaker
File: queens.py
"""

import pprint

class Board():

    def __init__(self, seed=(0,0)):

        self._board = [[0 for x in range(8)]
                       for y in range(8)]

        # Seed the first queen
        if seed != None:
            self.placeQueen(*seed)
            

    def solve(self, displayFunction=None):
        for row in range(8):
            if not 1 in self.getRow(row):
                for column in range(8):
                    if self._board[row][column] == 0:
                        if self.validPlacement(row, column):
                            self.placeQueen(row, column)
                            if displayFunction != None: displayFunction()
                            self.solve(displayFunction)
                            if not self.isSolved():
                                self._board[row][column] = 0
                return
                   
    def validPlacement(self, row, column):
        inRow       = 1 in self.getRow(row)
        inColumn    = 1 in self.getColumn(column)
        inDiagonals = 1 in self.getValuesOnDiagonalsIntersectingAt(row, column)
        return not inRow and not inColumn and not inDiagonals

    def placeQueen(self, row, column):
        self._board[row][column] = 1

    def printBoard(self):
        pprint.pprint(self._board)

    def getRow(self, row):
        return self._board[row]

    def getColumn(self, column):
        return [row[column] for row in self._board]

    def getValuesOnDiagonalsIntersectingAt(self, r, c):
        return [column for i, row in enumerate(self._board)
                for j, column in enumerate(row)
                if abs(r-i) == abs(c-j)]

    def isSolved(self):
        return 8 == len([column for row in self._board
                         for column in row
                         if column == 1])



    
