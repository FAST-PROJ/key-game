from random import randrange

class GameState():
    def __init__(self, pyGame):
        self.board = [
            ["bV", "bV", "bV", "bV", "bV", "bV", "bV", "bV", "bV", "bV", "bV", "bV", "bV"],
            ["--", "--", "--", "--", "--", "--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--", "--", "--", "--", "--", "--"],
            ["bA", "bA", "bA", "bA", "bA", "bA", "bA", "bA", "bA", "bA", "bA", "bA", "bA"]]
        self.whiteToMove = True
        self.moveLog = []
        self.pyGame = pyGame
        self.myFont = pyGame.font.SysFont('Comic Sans MS', 30)
        self.__showKeys()

    def __showKeys(self):
        for line in range(3, 10):
            column = randrange(len(self.board))
            self.board[line][column] = "key"

    def endGame(self, player):
        if player.keysSaved == 4:
            textsurface = self.myFont.render('{name} ganhou!!!'.format(name=player.name), False, (0, 0, 0))
            self.pyGame.screen.blit(textsurface, (0, 0))

    def showMoviments(self, possiblePositions):
        for position in possiblePositions:
            piece = self.board[position[0]][position[1]]
            if piece == "key":
                self.board[position[0]][position[1]] = "key_selected"
            elif piece != "bV" and piece != "bA":
                self.board[position[0]][position[1]] = "PP"

    def clearMoviments(self):
        for line in range(len(self.board)):
            for column in range(len(self.board[0])):
                piece = self.board[line][column]
                if piece == "PP":
                    self.board[line][column] = "--"
                elif piece == "key_selected":
                    self.board[line][column] = "key"



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

    


















