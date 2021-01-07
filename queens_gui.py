"""
Author: Trevor Stalnaker
File: queens_gui.py
"""

import pygame, time, random
from queens import Board
from _thread import start_new_thread

TILE_WIDTH = 50
QUEEN = pygame.image.load("queen.png")

class QueensGUI():

    def __init__(self, n=8):
        pygame.init()
        pygame.font.init()
        pygame.display.set_caption('Checker Board GUI')
        self._n = n
        dim = TILE_WIDTH * n #pixelsPerSquare * (numSquares + padding)
        self._screen = pygame.display.set_mode((dim+20,dim+90))

        global QUEEN
        QUEEN = QUEEN.convert()
        QUEEN.set_colorkey(QUEEN.get_at((0,0)))

        self.makeButtons()
        self.makeInstructions()
        
        self._RUNNING = True
        self._board = Board()
        self.makeBoard()
        self._solved = False
        self._animating = False
        self._waitForPlayer = False

    def makeButtons(self):
        y = (TILE_WIDTH * self._n) + 50
        self._newButton = Button((100, y), "New")
        x = self._newButton.getWidth() + self._newButton._pos[0] + 10
        self._quickSolveButton = Button((x, y), "Quick Solve")
        x = self._quickSolveButton.getWidth() + \
            self._quickSolveButton._pos[0] + 10
        self._stepSolveButton = Button((x, y), "Step Solve")

    def makeInstructions(self):
        font = pygame.font.SysFont("Times New Roman", 16)
        self._instructions = font.render("Place a Queen Above", True, (0,0,0))
  
    def quickSolve(self):
        self._solved = True
        self._board.solve()
        self.makeBoard()
        
    def animatedSolve(self):
        self._animating = True
        start_new_thread(self._solve, ())

    def _solve(self):
        self._board.solve(self.animate)
        self.makeBoard()
        self._solved = True

    def animate(self):
        if self._animating:
            self.makeBoard()
            time.sleep(.5)

    def makeBoard(self):
        tiles = []
        for i in range(8):
            for j in range(8):
                x = (TILE_WIDTH * (j)) + 10
                y = (TILE_WIDTH * (i)) + 10
                if i%2 == j%2:
                    color = (255,0,0)
                else:
                    color = (0,0,0)
                queen = self._board._board[i][j] == 1
                tiles.append(BoardTile((x,y),color, queen))
        self._tiles = tiles
        
    def draw(self):
        self._screen.fill((230,230,230))
        for t in self._tiles:
            t.draw(self._screen)
        
        self._newButton.draw(self._screen)
        self._quickSolveButton.draw(self._screen)
        self._stepSolveButton.draw(self._screen)
        if self._waitForPlayer:
            self._screen.blit(self._instructions, (142,420))
        pygame.display.flip()

    def handleEvents(self): 
        for event in pygame.event.get():
            
            if (event.type == pygame.QUIT):
                self._RUNNING = False

            ## Handle events on the solve buttons
            self._stepSolveButton.handleEvent(event, self.solveAnimated)
            self._quickSolveButton.handleEvent(event, self.solveQuick)

            ## Keyboard Short-cut for a new board          
            if event.type == pygame.KEYDOWN and \
               event.key == pygame.K_n:
                self.newBoard()

            ## Button press for a new board
            self._newButton.handleEvent(event, self.newBoard)

            ## Allow the player to place a new queen on the board
            if self._waitForPlayer:
                if event.type == pygame.MOUSEBUTTONDOWN and \
                   event.button == 1 and event.pos[1] < 8*TILE_WIDTH + 10:
                    x, y = event.pos
                    column = (x - 10)  // TILE_WIDTH
                    row = (y - 10) // TILE_WIDTH
                    self._board.placeQueen(row, column)
                    self.makeBoard()
                    self._waitForPlayer = False

    def newBoard(self):
        self._board = Board(None)
        self.makeBoard()
        if self._animating:
            self._animating = False
            #Allow the other thread to terminate
            time.sleep(.25) 
        self._solved = False
        self._waitForPlayer = True

    def solveAnimated(self):
        if not self._solved:
            self.animatedSolve()

    def solveQuick(self):
        if not self._solved:
            if not self._animating:
                self.quickSolve()
            else:
                self._animating = False
                    
    def runGameLoop(self):
        while self.isRunning():
            self.draw()
            self.handleEvents()
        pygame.quit()

    def isRunning(self):
        return self._RUNNING

class BoardTile():

    def __init__(self, pos, color, queen=False):
        self._pos = pos
        self._image = pygame.Surface((TILE_WIDTH,TILE_WIDTH))
        self._image.fill(color)
        if queen:
            x_pos = (TILE_WIDTH // 2) - (QUEEN.get_width() // 2)
            y_pos = (TILE_WIDTH // 2) - (QUEEN.get_height() // 2)
            self._image.blit(QUEEN, (x_pos,y_pos))

    def draw(self, screen):
        screen.blit(self._image, self._pos)

class Button():

    def __init__(self, pos, text, onclick=None):

        self._pos = pos
        
        font = pygame.font.SysFont("Times New Roman", 16)
        t = font.render(text, True, (0,0,0))
        padding = 6
        dims = (t.get_width() + padding, t.get_height() + padding)
        self._image = pygame.Surface(dims)
        self._image.fill((120,120,120))  
        self._image.blit(t, (padding//2,padding//2))

    def draw(self, screen):
        screen.blit(self._image, self._pos)

    def handleEvent(self, event, func):
        rect = self._image.get_rect()
        rect = rect.move(*self._pos)
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if rect.collidepoint(event.pos):
                func()

    def getWidth(self):
        return self._image.get_width()


g =QueensGUI(8)
g.runGameLoop()
