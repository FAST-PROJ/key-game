from random import randrange
import constant as const

class GameState():
    def __init__(self, pyGame, screen):
        self.board = const.BOARD
        self.whiteToMove = True
        self.moveLog = []
        self.pyGame = pyGame
        self.screen = screen
        self.myFont = pyGame.font.SysFont('Comic Sans MS', 30)
        self.__showKeys()

    def __showKeys(self):
        for line in range(3, 10):
            column = randrange(len(self.board))
            self.board[line][column] = const.KEY

    def endGame(self, player):
        if player.keysSaved == 4:
            textsurface = self.myFont.render('{name} ganhou!!!'.format(name=player.name), False, (0, 0, 0))
            self.screen.blit(textsurface, (0, 0))

    def showMovements(self, possiblePositions):
        for position in possiblePositions:
            piece = self.board[position[0]][position[1]]
            if piece == const.KEY:
                self.board[position[0]][position[1]] = const.IS_KEY_SELECTED
            elif piece != const.PLAYER_ONE_PIECE and piece != const.PLAYER_TWO_PIECE:
                self.board[position[0]][position[1]] = const.HIGHLIGHT_MOVEMENT

    def clearMovements(self):
        for line in range(len(self.board)):
            for column in range(len(self.board[0])):
                piece = self.board[line][column]
                if piece == const.HIGHLIGHT_MOVEMENT:
                    self.board[line][column] = const.BLANK_SPACE
                elif piece == const.IS_KEY_SELECTED:
                    self.board[line][column] = const.KEY

    def isInsideBoard(self, x, y):
        return ((x < 0) or (x > len(self.board[0])) or (y < 0) or (y > len(self.board)))

class Move():
    ranksToRows = {"1": 7, "2": 6, "3": 5, "4": 4, "5": 3, "6": 2, "7": 1, "8": 0}
    rowsToRanks = {v: k for k, v in ranksToRows.items()}
    filesToCols = {"a": 0, "b": 1, "c": 2, "d": 3, "e": 4, "f": 5, "g": 6, "h": 7}
    colsToFiles = {v: k for k, v in filesToCols.items()}

    def __init__(self, startSq, endSq, board):
        self.startRow = startSq[0]
        self.startCol = startSq[1]
        self.endRow = endSq[0]
        self.endCol = endSq[1]
        self.pieceMoved = board[self.startRow][self.startCol]
        self.pieceCaptured = board[self.endRow][self.endCol]


    def getChessNotation(self):
        return self.getRankFile(self.startRow, self.startCol) + self.getRankFile(self.endRow, self.endCol)

    def getRankFile(self, r, c):
        return self.colsToFiles[c] + self.rowsToRanks[r]




















