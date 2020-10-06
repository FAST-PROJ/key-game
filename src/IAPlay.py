import pprint
import constant as const
pp = pprint.PrettyPrinter(indent=1, width=160)

class Node():
    def __init__(self, parent=None, position=None):
        self.parent = parent
        self.position = position

        self.g = 0
        self.h = 0
        self.f = 0

    def __eq__(self, other):
        return self.position == other.position

class IAPlay():
    def __init__(self, gameState, player, board, keyList):
        self.gameState = gameState
        self.player = player
        self.board = board
        self.keyList = keyList
        self.IAvisitedNodes = []
        self.testBoard = [[1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
                        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                        [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]]


    '''
        IA procura o melhor movimento
    '''
    def makeMove(self):
        IAMoves = self.findBestMove(self.testBoard, [len(self.board)-1, 0], self.keyList)

        paths = []
        for path in IAMoves:
            paths.append([path['path'][0], path['path'][1]])

        possibleMoves = []
        for piece in [const.KNIGHT_PIECE, const.BISHOP_PIECE, const.ROOK_PIECE]:
            moves = self.player.possibleMovements(self.board, self.player.position[1], pieceInUse=piece)
            possibleMoves.append(moves)
            self.gameState.showMovements(moves)

        foundMovement = self.getIABestMovement(possibleMoves, paths)

        if foundMovement is None:
            foundMovement = self.getIANearMovement(possibleMoves, paths)

        return foundMovement

    def findPathToKeys(self, board, base, keyLocation):
        base_node = Node(None, base)
        base_node.g = base_node.h = base_node.f = 0

        key_node = Node(None, keyLocation)
        key_node.g = key_node.h = key_node.f = 0

        open_list = []
        closed_list = []
        open_list.append(base_node)

        while len(open_list) > 0:
            current_node = open_list[0]
            current_index = 0
            for index, item in enumerate(open_list):
                if item.f < current_node.f:
                    current_node = item
                    current_index = index

            open_list.pop(current_index)
            closed_list.append(current_node)

            if current_node == key_node:
                path = []
                current = current_node
                while current is not None:
                    path.append(current.position)
                    current = current.parent
                return path[::-1]

            children = []
            for new_position in [(0, -1), (0, 1), (-1, 0), (1, 0), (-1, -1), (-1, 1), (1, -1), (1, 1)]:

                node_position = (current_node.position[0] + new_position[0], current_node.position[1] + new_position[1])
                if node_position[0] > (len(board) - 1) or node_position[0] < 0 or node_position[1] > (len(board[len(board)-1]) -1) or node_position[1] < 0:
                    continue

                if board[node_position[0]][node_position[1]] != 0:
                    continue

                new_node = Node(current_node, node_position)
                children.append(new_node)

            for child in children:
                for closed_child in closed_list:
                    if child == closed_child:
                        continue

                child.g = current_node.g + 1
                child.h = ((child.position[0] - key_node.position[0]) ** 2) + ((child.position[1] - key_node.position[1]) ** 2)
                child.f = child.g + child.h

                for open_node in open_list:
                    if child == open_node and child.g > open_node.g:
                        continue

                open_list.append(child)

    def findBestMove(self, board, base, keysLocation):
        base = (12, 6)
        IAMoves = [0, 0]

        paths = []
        for key in keysLocation:
            keyLocation = (key[0], key[1])
            path = self.findPathToKeys(board, base, keyLocation)
            paths.append({"path" : keyLocation, "len" : len(path)})

        IAMoves = sorted(paths, key = lambda i: i['len'])
        return IAMoves

    def getIABestMovement(self, possibleMoves, paths):
        for pieceMoves in possibleMoves:
            for move in pieceMoves:
                if move in self.IAvisitedNodes:
                    continue

                if move in paths:
                    if abs(self.player.position[0] - move[0]) > const.ROOK_MAX_MOVEMENT:
                        continue

                    if abs(self.player.position[1] - move[1]) > const.ROOK_MAX_MOVEMENT:
                        continue

                    self.IAvisitedNodes.append(move)
                    return move

    def getIANearMovement(self, possibleMoves, paths):
        for pieceMoves in possibleMoves:
            for move in pieceMoves:
                print(move)
                if move in self.IAvisitedNodes:
                    continue

                if abs(self.player.position[0] - move[0]) > const.ROOK_MAX_MOVEMENT:
                    continue

                if abs(self.player.position[1] - move[1]) > const.ROOK_MAX_MOVEMENT:
                    continue

                return move

