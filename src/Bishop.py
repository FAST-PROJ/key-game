class Bishop:
    def __init__(self, x, y):
        self.x = x # instance variable unique to each instance
        self.y = y

    def getDiagonalCoordinates(self):
        directions = [[1,1],[-1,1],[-1,-1],[1,-1]]
        moves = []
        for direction in directions: #search for squares in every direction diagonally around the piece
            possible_x = self.x #set the starting point back to the piece's actual location
            possible_y = self.y
            for counter in range(0,8):
                possible_x = possible_x+direction[0]
                possible_y = possible_y+direction[1]
                # if self.gameEngine.isInsideBoard(possible_x, possible_y): #creates an instance, but it immediately dissapears. This IS NOT the main board used for the game, we're only using it for the helper method
                moves.append([possible_x,possible_y])
                # else: #the move isn't on the board. Don't add it to the moves list, and quit this loop
                    # break
        return moves

    def getPossibleMoves(self):
        possibleMoves = self.getDiagonalCoordinates()
        return possibleMoves

    def setPosition(self,x,y):
        self.x = x
        self.y = y