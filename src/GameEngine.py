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
        self.listKeys = []
        self.__showKeys()

    def __showKeys(self):
        for line in range(3, 10):
            column = randrange(len(self.board))
            self.board[line][column] = const.KEY
            self.listKeys.append([line, column])

    def getKeyList(self):
        return self.listKeys

    def endGame(self, player):
        if player.keysSaved == 4:
            textsurface = self.myFont.render('{name} ganhou!!!'.format(name=player.name), False, (0, 0, 0))
            self.screen.blit(textsurface, (0, 0))

    def showMovements(self, possiblePositions):
        for position in possiblePositions:
            try:
                piece = self.board[position[0]][position[1]]
                if piece == const.KEY:
                    self.board[position[0]][position[1]] = const.IS_KEY_SELECTED
                elif piece != const.PLAYER_ONE_PIECE and piece != const.PLAYER_TWO_PIECE:
                    self.board[position[0]][position[1]] = const.HIGHLIGHT_MOVEMENT
            except IndexError:
                '''
                    A posição a ser desenha está fora do tabuleiro
                    Continua para a próxima iteração de posições
                '''
                continue

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




















