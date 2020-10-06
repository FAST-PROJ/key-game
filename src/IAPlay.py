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

        pp.pprint(f"localizacao das chaves {self.keyList}")


    '''
        IA procura o melhor movimento
    '''
    def makeMove(self):
        # test
        # IAMoves = self.findBestMoveToBase(self.testBoard, [9, 9], [len(self.board) -1, 0])
        # print(f" move to base {IAMoves}")

        possibleMoves = [[[6, 8], [6, 10], [12, 8], [12, 10], [8, 6], [8, 12], [10, 6], [10, 12]], [[10, 10], [11, 11], [12, 12], [8, 10], [7, 11], [6, 12], [8, 8], [7, 7], [6, 6], [10, 8], [11, 7], [12, 6]], [[6, 9], [7, 9], [9, 6], [9, 7], [9, 8], [9, 10], [9, 11], [9, 12], [10, 9], [11, 9], [12, 9]]]

        paths = [[(9, 9), (12, 8)]]

        self.getIANearMovement(possibleMoves, paths, goal=(len(self.board) -1, self.player.position[1]))
        return


        print(f"chaves no bolso {self.player.keysOnPocket}")
        # se tem chave no bolso busca um caminho para a base
        if self.player.keysOnPocket > 0 :
            IAMoves = self.findBestMoveToBase(self.testBoard, self.player.position, [len(self.board) -1, 0])
            print(f" move to base {IAMoves}")
        else:
            IAMoves = self.findBestMove(self.testBoard, [len(self.board)-1, 0], self.keyList)


        paths = []
        for path in IAMoves:
            paths.append([path['path'][0], path['path'][1]])

        possibleMoves = []
        for piece in [const.KNIGHT_PIECE, const.BISHOP_PIECE, const.ROOK_PIECE]:
            if self.player.onBase:
                for i in range(len(self.board)-1):
                    moves = self.player.possibleMovements(self.board, i, pieceInUse=piece)
                    possibleMoves.append(moves)
                    self.gameState.showMovements(moves)
            else:
                moves = self.player.possibleMovements(self.board, self.player.position[1], pieceInUse=piece)
                possibleMoves.append(moves)
                self.gameState.showMovements(moves)


        pp.pprint(f" possiveis movimentacoes IA - {possibleMoves}")

        foundMovement = self.getIABestMovement(possibleMoves, paths)
        print(foundMovement)

        if foundMovement is None:
            foundMovement = self.getIANearMovement(possibleMoves, paths)

        pp.pprint(f"melhor movimento encontrado {foundMovement}")

        print(f"visitados {self.player.IAvisitedNodes}")
        return foundMovement

    def findPathToKeys(self, board, base, keyLocation, pathToBase=False):

        # Cria o nó da base e o nó da localização da chave
        base_node = Node(None, base)
        base_node.g = base_node.h = base_node.f = 0
        key_node = Node(None, keyLocation)
        key_node.g = key_node.h = key_node.f = 0

        # Initialize both open and closed list
        open_list = []
        closed_list = []

        # Adiciona o nó da base na lista
        open_list.append(base_node)

        # Roda até encontrar a chave
        while len(open_list) > 0:

            # Get the current node
            current_node = open_list[0]
            current_index = 0
            for index, item in enumerate(open_list):
                if item.f < current_node.f:
                    current_node = item
                    current_index = index

            # Remove o nó corrente da lista aberta e adiciona a lista de nós próximos
            open_list.pop(current_index)
            closed_list.append(current_node)

            # Encontrou a chave
            if current_node == key_node:
                path = []
                current = current_node
                while current is not None:
                    path.append(current.position)
                    current = current.parent

                pp.pprint(f"path {path}\n")
                return path[::-1] # Retorna o caminho até a chave

            # Generate children
            children = []
            for new_position in [(1,1), (-1,1), (-1,-1), (1,-1), (-3, -1), (-3, +1), (+3, -1), (+3, +1), (-1, -3), (-1, +3), (+1, -3), (+1, +3), (0, -1), (0, 1), (-1, 0), (1, 0), (-1, -1), (-1, 1), (1, -1), (1, 1)]: # Adjacent squares
            # for new_position in [(-3, -1), (-3, +1), (+3, -1), (+3, +1), (-1, -3), (-1, +3), (+1, -3), (+1, +3)]: # Adjacent squares
            # for new_position in [(1,1), (-1,1), (-1,-1), (1,-1)]: # Adjacent squares
            # for new_position in [(1, 0)]: # Adjacent squares



                # Get node position
                node_position = (current_node.position[0] + new_position[0], current_node.position[1] + new_position[1])

                # Make sure within range
                if node_position[0] > (len(board) - 1) or node_position[0] < 0 or node_position[1] > (len(board[len(board)-1]) -1) or node_position[1] < 0:
                    continue

                # Make sure walkable terrain
                if board[node_position[0]][node_position[1]] != 0 and not pathToBase:
                    continue

                # Create new node
                new_node = Node(current_node, node_position)

                # Append
                children.append(new_node)

            # Loop through children
            for child in children:

                # Child is on the closed list
                for closed_child in closed_list:
                    if child == closed_child:
                        continue

                # Create the f, g, and h values
                child.g = current_node.g + 1
                child.h = ((child.position[0] - key_node.position[0]) ** 2) + ((child.position[1] - key_node.position[1]) ** 2)
                child.f = child.g + child.h

                # Child is already in the open list
                for open_node in open_list:
                    if child == open_node and child.g > open_node.g:
                        continue

                # Add the child to the open list
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

    def findBestMoveToBase(self, board, position, base):
        IAMoves = [0, 0]

        paths = []

        print((position[0], position[1]))
        print((base[0], position[1]))

        # pos = (9, 9)
        # base = (12, 9)
        pos = (position[0], position[1])
        base = (base[0], position[1])

        path = self.findPathToKeys(board, pos, base, pathToBase=True)

        paths.append({"path" : path, "len" : len(path)})
        IAMoves = sorted(paths, key = lambda i: i['len'])
        return IAMoves

    def getIABestMovement(self, possibleMoves, paths):
        for pieceMoves in possibleMoves:
            for move in pieceMoves:
                if move in self.player.IAvisitedNodes:
                    continue

                if move in paths:
                    if abs(self.player.position[0] - move[0]) > const.ROOK_MAX_MOVEMENT:
                        continue

                    if abs(self.player.position[1] - move[1]) > const.ROOK_MAX_MOVEMENT:
                        continue

                    pp.pprint(f"ia best move - {move}")
                    self.player.IAvisitedNodes.append(move)
                    return move

    def getIANearMovement(self, possibleMoves, paths, goal=None):

        print(f"possibleMoves {possibleMoves}")
        print(f"paths {paths}")
        print(f"goal {goal}")
        for pieceMoves in possibleMoves:
            for move in pieceMoves:
                if move in self.player.IAvisitedNodes:
                    continue

                if abs(self.player.position[0] - move[0]) > const.ROOK_MAX_MOVEMENT:
                    continue

                if abs(self.player.position[1] - move[1]) > const.ROOK_MAX_MOVEMENT:
                    continue

                pp.pprint(f"near move - {move}")
                self.player.IAvisitedNodes.append(move)
                return move
