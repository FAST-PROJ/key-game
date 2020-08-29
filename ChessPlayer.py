import pygame as pygame

POSSIBLE_MOVIMENT = 3
class ChessPlayer():
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

    def possibleMoviments(self, board, column):
        possiblePositions = []

        if self.onBase:
            self.position = [self.position[0], column]

        #faz um loop pelas posicoes permitidas verificando se a mesma pode ser feita
        for line in range(self.position[0] - POSSIBLE_MOVIMENT, (self.position[0] + POSSIBLE_MOVIMENT) + 1):
            for column in range(self.position[1] - POSSIBLE_MOVIMENT, (self.position[1] + POSSIBLE_MOVIMENT) + 1):
                if self.movimentPossibleTower([line, column], board):
                    possiblePositions.append([line, column])
                else:
                    continue

        return possiblePositions

    def movimentPossibleTower(self, move, board):
        if move[0] >= 0 and move[0] < len(board) and move[1] >= 0 and move[1] < len(board[0]):
            piece = board[move[0]][move[1]]
            if self.position[0] == move[0] or self.position[1] == move[1]:
                if piece == "--" or piece == "PP" or piece == self.baseName or (piece == "key" and self.keysOnPocket < self.keysLimit):
                    return True

        return False

    def makeMove(self, move, chessEngine, player2):

        #pega o nome das posicoes iniciais e finais
        startPlay = chessEngine.board[self.position[0]][self.position[1]]
        endPlay = chessEngine.board[move[0]][move[1]]

        #seta os nomes das posicoes depois do movimento
        if startPlay != self.baseName:
            chessEngine.board[self.position[0]][self.position[1]] = "--"
        chessEngine.board[move[0]][move[1]] = self.name

        #seta que saimos da base
        self.onBase = False

        if endPlay == "key_selected":
            chessEngine.board[move[0]][move[1]] = "--"
            self.keysOnPocket = self.keysOnPocket + 1
        elif move[0] != self.position[0]:
            startline = self.position[0] if self.position[0] < move[0] else move[0]
            endLine = move[0] if move[0] > self.position[0] else self.position[0]
            for line in range(startline, endLine):
                piece = chessEngine.board[line][move[1]]
                if piece == "key_selected" and self.keysOnPocket < self.keysLimit:
                    chessEngine.board[line][move[1]] = "--"
                    self.keysOnPocket = self.keysOnPocket + 1
                elif piece == player2.name and player2.keysOnPocket > 0 and self.keysOnPocket < self.keysLimit:
                    player2.keysOnPocket = player2.keysOnPocket - 1
                    self.keysOnPocket = self.keysOnPocket + 1
        elif move[1] != self.position[1]:
            startColumn = self.position[1] if self.position[1] < move[1] else move[1]
            endColumn = move[1] if move[1] > self.position[1] else self.position[1]
            for column in range(startColumn, endColumn):
                piece = chessEngine.board[move[0]][column]
                if piece == "key_selected" and self.keysOnPocket < self.keysLimit:
                    chessEngine.board[move[0]][column] = "--"
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




