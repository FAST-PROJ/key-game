import constant as const
from Bishop import Bishop

POSSIBLE_MOVIMENT = 3
class Player():
    def __init__(self, position, color, name, baseName):
        self.position = position
        self.color = color
        self.keysSaved = 0
        self.keysOnPocket = 0
        self.yourTurn = False
        self.name = name
        self.baseName = baseName
        self.keysLimit = 1
        self.onBase = True

    '''
        Create the players pieces
    '''
    def possibleMovements(self, board, column):
        possiblePositions = []

        if self.onBase:
            self.position = [self.position[0], column]

        #faz um loop pelas posicoes permitidas verificando se a mesma pode ser feita
        for line in range(self.position[0] - POSSIBLE_MOVIMENT, (self.position[0] + POSSIBLE_MOVIMENT) + 1):
            for column in range(self.position[1] - POSSIBLE_MOVIMENT, (self.position[1] + POSSIBLE_MOVIMENT) + 1):
                if self.__movementPossibleTower([line, column], board):
                    possiblePositions.append([line, column])
                else:
                    continue

                # Testando os movimentos do bispo
                # moves = self.__movementPossibleBishop([line, column], board)
                # possiblePositions.append(moves[0])

        return possiblePositions

    '''
        Create the players pieces
    '''
    def __movementPossibleTower(self, move, board):
        if move[0] >= 0 and move[0] < len(board) and move[1] >= 0 and move[1] < len(board[0]):
            piece = board[move[0]][move[1]]
            if self.position[0] == move[0] or self.position[1] == move[1]:
                if self.__isBlankSpace(piece) or self.__isHighlightMovement(piece) or self.__isPlayerBase(piece) or self.__hasKeyOnPocket(piece):
                    return True

        return False

    '''
        @todo bishop movements
    '''
    def __movementPossibleBishop(self, move, board):
        B1 = Bishop(3, 3) #make one instance of the bishop class and initialize it at a position
        B2 = Bishop(4, 6) #make a different instance of the bishop class

        print("Current location if B1 - X: {} Y: {}".format(B1.x, B1.y))
        print("Current location if B2 - X: {} Y: {}".format(B2.x, B2.y))
        print(B1.getPossibleMoves())

    '''
        Create the players pieces
    '''
    def __isBlankSpace(self, piece):
        return piece == const.BLANK_SPACE

    '''
        Create the players pieces
    '''
    def __isHighlightMovement(self, piece):
        return piece == const.HIGHLIGHT_MOVEMENT

    '''
        Create the players pieces
    '''
    def __isPlayerBase(self, piece):
        return piece == self.baseName

    '''
        Create the players pieces
    '''
    def __hasKeyOnPocket(self, piece):
        return (piece == const.KEY and self.keysOnPocket < self.keysLimit)

    '''
        Create the players pieces
    '''
    def makeMove(self, move, chessEngine, player2):
        #pega o nome das posicoes iniciais e finais
        startPlay = chessEngine.board[self.position[0]][self.position[1]]
        endPlay = chessEngine.board[move[0]][move[1]]

        #seta os nomes das posicoes depois do movimento
        if startPlay != self.baseName:
            chessEngine.board[self.position[0]][self.position[1]] = const.BLANK_SPACE
        chessEngine.board[move[0]][move[1]] = self.name

        #seta que saimos da base
        self.onBase = False

        if endPlay == const.IS_KEY_SELECTED:
            chessEngine.board[move[0]][move[1]] = self.name
            self.keysOnPocket = self.keysOnPocket + 1
        elif move[0] != self.position[0]:
            startline = self.position[0] if self.position[0] < move[0] else move[0]
            endLine = move[0] if move[0] > self.position[0] else self.position[0]
            for line in range(startline, endLine):
                piece = chessEngine.board[line][move[1]]
                if piece == const.IS_KEY_SELECTED and self.keysOnPocket < self.keysLimit:
                    chessEngine.board[line][move[1]] = const.BLANK_SPACE
                    self.keysOnPocket = self.keysOnPocket + 1
                elif piece == player2.name and player2.keysOnPocket > 0 and self.keysOnPocket < self.keysLimit:
                    player2.keysOnPocket = player2.keysOnPocket - 1
                    self.keysOnPocket = self.keysOnPocket + 1
        elif move[1] != self.position[1]:
            startColumn = self.position[1] if self.position[1] < move[1] else move[1]
            endColumn = move[1] if move[1] > self.position[1] else self.position[1]
            for column in range(startColumn, endColumn):
                piece = chessEngine.board[move[0]][column]
                if piece == const.IS_KEY_SELECTED and self.keysOnPocket < self.keysLimit:
                    chessEngine.board[move[0]][column] = const.BLANK_SPACE
                    self.keysOnPocket = self.keysOnPocket + 1
                elif piece == player2.name and player2.keysOnPocket > 0 and self.keysOnPocket < self.keysLimit:
                    player2.keysOnPocket = player2.keysOnPocket - 1
                    self.keysOnPocket = self.keysOnPocket + 1

        if endPlay == self.baseName:
            chessEngine.board[move[0]][move[1]] = self.baseName
            self.onBase = True
            if self.keysOnPocket > 0:
                self.keysSaved = self.keysSaved + self.keysOnPocket
                self.keysOnPocket = 0

        self.position = move
        self.yourTurn = False
        chessEngine.endGame(self)




