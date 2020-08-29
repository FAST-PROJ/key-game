import pygame as p
import ChessEngine
from ChessPlayer import ChessPlayer

WIDTH = HEIGHT = 640
MAX_FPS = 15
IMAGES = {}

def loadImages(size):
    pieces = ["bV", "bA", "key", "key_selected"]
    for piece in pieces:
        IMAGES[piece] = p.transform.scale(p.image.load("images/{piece}.png".format(piece=piece)), (size, size))

def main():
    p.init()
    p.font.init()
    screen = p.display.set_mode((WIDTH, HEIGHT))
    clock = p.time.Clock()
    screen.fill(p.Color("white"))
    gs = ChessEngine.GameState(p)
    player1 = ChessPlayer([0, 0], p.Color("red"), "Player Vermelho", "bV")
    player1.yourTurn = True
    player2 = ChessPlayer([len(gs.board)-1, 0], p.Color("blue"), "Player Azul", "bA")
    player2.yourTurn = False
    sq_size = HEIGHT // len(gs.board)
    loadImages(sq_size)
    running = True
    sqSelected = []
    movimentsPossibles = []
    while running:
        for e in p.event.get():
            if e.type == p.QUIT:
                running = False
            elif e.type == p.MOUSEBUTTONDOWN:
                location = p.mouse.get_pos()
                col = location[0]//sq_size
                row = location[1]//sq_size
                playerMove = player1 if player1.yourTurn else player2

                if sqSelected == [row, col]:
                    sqSelected = []
                    gs.clearMoviments()
                else:                       
                    sqSelected = [row, col]

                if sqSelected == playerMove.position or (row == playerMove.position[0] and playerMove.onBase):
                    movimentsPossibles = playerMove.possibleMoviments(gs.board, col)
                    gs.clearMoviments()
                    gs.showMoviments(movimentsPossibles)
                elif gs.board[row][col] == "PP" or gs.board[row][col] == "key_selected" or gs.board[row][col] == playerMove.baseName:
                    if [row, col] in movimentsPossibles:
                        nextPlayer = player1 if playerMove != player1 else player2
                        playerMove.makeMove([row, col], gs, nextPlayer)
                        nextPlayer.yourTurn = True
                        gs.clearMoviments()
                        movimentsPossibles = []

        drawGameState(screen, gs, [player1, player2], sq_size)
        clock.tick(MAX_FPS)
        p.display.flip()

def drawGameState(screen, gs, players, size):
    drawBoard(screen, gs, players, size)
    drawPieces(screen, gs.board, players, size)

def drawBoard(screen, gs, players, size):
    colors = [p.Color("white"), p.Color("gray")]
    for r in range(len(gs.board)):
        for c in range(len(gs.board[0])):
            color = colors[((r+c) % 2)]
            piece = gs.board[r][c]
            playerToDraw = None
            for player in players:
                if player.position == [r, c]:
                    playerToDraw = player
                    break

            if playerToDraw != None:
                p.draw.rect(screen, playerToDraw.color, p.Rect(c * size, r * size, size, size))
            elif piece == "PP":
                p.draw.rect(screen, p.Color("orange"), p.Rect(c * size, r * size, size, size))
            else:
                p.draw.rect(screen, color, p.Rect(c * size, r * size, size, size))

def drawPieces(screen, board, players, size):
    for r in range(len(board)):
        for c in range(len(board[0])):
            piece = board[r][c]
            playerToDraw = None
            for player in players:
                if player.position == [r, c]:
                    playerToDraw = player
                    break

            if playerToDraw == None or piece == playerToDraw.baseName:
                if piece != "--" and piece != "PP":
                    screen.blit(IMAGES[piece], p.Rect(c*size, r*size, size, size))

if __name__ == "__main__":
    main()
