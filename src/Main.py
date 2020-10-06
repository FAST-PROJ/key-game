import pygame
import pprint
pp = pprint.PrettyPrinter(indent=1, width=160)

import constant as const
import GameEngine

from IAPlay import IAPlay
from Player import Player

class Main():
    def __init__(self):
        pygame.init()
        pygame.font.init()

        self.screen = pygame.display.set_mode((const.WIDTH, const.HEIGHT))
        self.screen.fill(pygame.Color(const.BOARD_COLOR_WHITE))
        self.clock = pygame.time.Clock()
        self.gameState = GameEngine.GameState(pygame, self.screen)
        self.squareSize = const.HEIGHT // len(self.gameState.board)
        self.running = True
        self.squareSelected = []
        self.movementsPossibles = []

    '''
        Init pygame
    '''
    def init(self):
        self.__createPlayers()
        self.__loadImages()

        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    location = pygame.mouse.get_pos()
                    col = location[0] // self.squareSize
                    row = location[1] // self.squareSize
                    playerMove = self.playerOne if self.playerOne.yourTurn else self.playerTwo

                    if self.squareSelected == [row, col]:
                        self.squareSelected = []
                        self.gameState.clearMovements()
                    else:
                        self.squareSelected = [row, col]
                    if self.squareSelected == playerMove.position or (row == playerMove.position[0] and playerMove.onBase):
                        movementsPossibles = playerMove.possibleMovements(self.gameState.board, col)
                        self.gameState.clearMovements()
                        self.gameState.showMovements(movementsPossibles)
                    elif self.gameState.board[row][col] == const.HIGHLIGHT_MOVEMENT or self.gameState.board[row][col] == const.IS_KEY_SELECTED or self.gameState.board[row][col] == playerMove.baseName:
                            if [row, col] in movementsPossibles:
                                self.makeMove([row, col])
                                movementsPossibles = []

                # IA Parts
                elif self.playerTwo.yourTurn:
                    ia = IAPlay(
                        self.gameState,
                        self.playerTwo,
                        self.gameState.board,
                        game.gameState.getKeyList()
                    )
                    movement = ia.makeMove()
                    self.playerTwo.yourTurn = False
                    self.makeMove(movement)

            self.__drawGameState([self.playerOne, self.playerTwo])
            self.clock.tick(const.MAX_FPS)
            pygame.display.flip()

    '''
        Move a peça no tabuleiro
    '''
    def makeMove(self, movement):
        playerMove = self.playerOne if self.playerOne.yourTurn else self.playerTwo
        nextPlayer = self.playerOne if playerMove != self.playerOne else self.playerTwo
        nextPlayer.yourTurn = True
        playerMove.makeMove(movement, self.gameState, nextPlayer)
        self.gameState.clearMovements()

    '''
        Create the players pieces
    '''
    def __createPlayers(self):
        self.playerOne = Player(
            [0, 0],
            pygame.Color(const.PLAYER_ONE_COLOR),
            const.PLAYER_ONE_NAME,
            const.PLAYER_ONE_PIECE
        )
        self.playerOne.yourTurn = True

        self.playerTwo = Player(
            [len(self.gameState.board)-1, 0],
            pygame.Color(const.PLAYER_TWO_COLOR),
            const.PLAYER_TWO_NAME,
            const.PLAYER_TWO_PIECE
        )
        self.playerTwo.yourTurn = False

    '''
        Load game images
    '''
    def __loadImages(self):
        pieces = [
            const.PLAYER_ONE_PIECE,
            const.PLAYER_TWO_PIECE,
            const.KEY,
            const.IS_KEY_SELECTED
        ]

        for piece in pieces:
            const.IMAGES[piece] = pygame.transform.scale(
                pygame.image.load("images/{piece}.png".format(piece=piece)),
                (self.squareSize, self.squareSize)
            )

    '''
        Draw board and pieces
    '''
    def __drawGameState(self, players):
        self.__drawBoard(players)
        self.__drawPieces(players)

    '''
        Draw the board
    '''
    def __drawBoard(self, players):
        colors = [pygame.Color("white"), pygame.Color("gray")]
        for row in range(len(self.gameState.board)):
            for col in range(len(self.gameState.board[0])):
                color = colors[((row + col) % 2)]
                piece = self.gameState.board[row][col]
                playerToDraw = None
                for player in players:
                    if player.position == [row, col]:
                        playerToDraw = player
                        break

                if playerToDraw != None:
                    pygame.draw.rect(
                        self.screen,
                        playerToDraw.color,
                        pygame.Rect(col * self.squareSize, row * self.squareSize, self.squareSize, self.squareSize)
                    )
                elif piece == const.HIGHLIGHT_MOVEMENT:
                    pygame.draw.rect(
                        self.screen,
                        pygame.Color("orange"),
                        pygame.Rect(col * self.squareSize, row * self.squareSize, self.squareSize, self.squareSize)
                    )
                else:
                    pygame.draw.rect(
                        self.screen,
                        color,
                        pygame.Rect(col * self.squareSize, row * self.squareSize, self.squareSize, self.squareSize)
                    )

    '''
        Draw the pieces
    '''
    def __drawPieces(self, players):
        for row in range(len(self.gameState.board)):
            for col in range(len(self.gameState.board[0])):
                piece = self.gameState.board[row][col]
                playerToDraw = None
                for player in players:
                    if player.position == [row, col]:
                        playerToDraw = player
                        break

                if playerToDraw == None or piece == playerToDraw.baseName:
                    if piece != const.BLANK_SPACE and piece != const.HIGHLIGHT_MOVEMENT:
                        self.screen.blit(
                            const.IMAGES[piece],
                            pygame.Rect(col * self.squareSize, row * self.squareSize, self.squareSize, self.squareSize)
                        )


'''
    Iniciando o jogo
'''
if __name__ == "__main__":
    game = Main()
    game.init()

    '''
        Testando o movimento do bispo
        Bishop = Player(
                [len(game.gameState.board)-1, 0],
                pygame.Color(const.PLAYER_ONE_COLOR),
                const.PLAYER_ONE_NAME,
                const.PLAYER_ONE_PIECE
            )
        Bishop.possibleMovements(game.gameState.board, 6)

        Testando o movimento do cavalo
        Knight = Player(
            [0, 0],
            pygame.Color(const.PLAYER_ONE_COLOR),
            const.PLAYER_ONE_NAME,
            const.PLAYER_ONE_PIECE
        )
        Knight.possibleMovements(game.gameState.board, 6)
    '''
