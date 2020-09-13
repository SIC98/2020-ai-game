import sys

from AtaxxLogic import Board, _directions_2
import numpy as np

action2move = []
action90rot = []
actionflip = []

for x in range(7):
    for y in range(7):
        action2move.append((None, None, x, y))

for x in range(7):
    for y in range(7):
        for dx, dy in _directions_2:
            if {x, y, x + dx, y + dy} <= set(range(7)):
                action2move.append((x, y, x + dx, y + dy))

action2move.append((None, None, None, None))

move2action = {e: i for i, e in enumerate(action2move)}

for x0, y0, x1, y1 in action2move:
    actionflip.append(move2action[(x0, (6 - y0) if (y0 != None) else None, x1, (6 - y1) if (y1 != None) else None)])
    if not (x0 == y0 == None):
        x0, y0 = x0 - 3, y0 - 3
        x0, y0 = -y0, x0
        x0, y0 = x0 + 3, y0 + 3
    if not (x1 == y1 == None):
        x1, y1 = x1 - 3, y1 - 3
        x1, y1 = -y1, x1
        x1, y1 = x1 + 3, y1 + 3
    action90rot.append(move2action[(x0, y0, x1, y1)])


class AtaxxGame:
    square_content = {
        -1: "X",
        +0: "-",
        +1: "O"
    }

    @staticmethod
    def getSquarePiece(piece):
        return AtaxxGame.square_content[piece]

    def __init__(self):
        pass

    def getInitBoard(self):
        b = Board()
        return np.array(b.pieces)

    def getBoardSize(self):
        return (7, 7)

    def getActionSize(self):
        # 49 for clone actions
        # 4 * (35 + 30 + 25 + 30) for move actions
        return 530

    def getNextState(self, board, player, action, turns):
        # if player takes action on board, return next (baord, player)
        # action must be a valid move
        b = Board()
        b.pieces = np.copy(board)
        move = action2move[action]
        b.execute_move(move, player)
        return b.pieces, -player, turns + 1

    def getValidMoves(self, board, player):
        valids = [0] * self.getActionSize()
        b = Board()
        b.pieces = np.copy(board)
        legalMoves = b.get_legal_moves(player)
        if len(legalMoves) == 0:
            valids[-1] = 1
            return np.array(valids)
        for x0, y0, x1, y1 in legalMoves:
            valids[move2action[x0, y0, x1, y1]] = 1
        return np.array(valids)

    def getGameEnded(self, board, player, turns):
        # return 0 if not ended, 1 if given player won, -1 if given player lost
        b = Board()
        b.pieces = np.copy(board)
        if turns >= 256:
            return 1 if b.countDiff(player) > 0 else -1
        if b.has_legal_moves(player) and b.has_legal_moves(-player):
            return 0
        if b.countDiff(player) > 0:
            return 1
        return -1

    def getCanonicalForm(self, board, player):
        return player * board

    # TODO: implement symmetries
    def getSymmetries(self, board, pi):
        assert (len(pi) == self.getActionSize())
        l = []
        pi = pi[:]

        for i in range(4):
            flipedBoard = np.fliplr(board)
            flipedPi = [(actionflip[i], e) for i, e in enumerate(pi)]
            flipedPi.sort()
            flipedPi = [e for _, e in flipedPi]

            l.append((flipedBoard, flipedPi))

            board = np.rot90(board, i)
            pi = [(action90rot[i], e) for i, e in enumerate(pi)]
            pi.sort()
            pi = [e for _, e in pi]

            l.append((board, pi))
        return l

    def stringRepresentation(self, board):
        return board.tostring()

    def stringRepresentationReadable(self, board):
        board_s = "".join(self.square_content[square] for row in board for square in row)
        return board_s

    def getScore(self, board, player):
        b = Board()
        b.pieces = np.copy(board)
        return b.countDiff(player)

    @staticmethod
    def display(board):
        n = board.shape[0]
        print("   ", end="")
        for y in range(n):
            print(y, end=" ")
        print("")
        print("-----------------------")
        for y in range(n):
            print(y, "|", end="")  # print the row #
            for x in range(n):
                piece = board[y][x]  # get the piece to print
                print(AtaxxGame.square_content[piece], end=" ")
            print("|")

        print("-----------------------")
