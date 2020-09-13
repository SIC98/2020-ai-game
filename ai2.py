import sys
import random
import numpy as np
from AtaxxGame import AtaxxGame
from NNet import NNetWrapper as NNet
from MCTS import MCTS
from utils import *

_directions_1 = [(1, 1), (1, 0), (1, -1), (0, -1), (-1, -1), (-1, 0), (-1, 1), (0, 1)]


def find_any_close_position(board, x, y):
    for dx, dy in _directions_1:
        if 0 <= x + dx < 7 and 0 <= y + dy <= 7 and board[x+dx][y+dy] == 1:
            return x+dx, y+dy
    yield 'error'


if __name__ == "__main__":

    input_str = sys.stdin.read()

    # 입력 예시
    # READY 1234567890.1234567 (입력시간)
    # "OK" 를 출력하세요.
    if input_str.startswith("READY"):
        # 출력
        sys.stdout.write("OK")

    # 입력 예시
    # PLAY
    # 2 0 0 0 0 0 1
    # 0 0 0 0 0 0 0
    # 0 0 0 0 0 0 0
    # 0 0 0 0 0 0 0
    # 0 0 0 0 0 0 0
    # 0 0 0 0 0 0 0
    # 1 0 0 0 0 0 2
    # 1234567890.1234567 (입력시간)

    # AI의 액션을 출력하세요.
    # 출력 예시 : "0 0 2 2"
    elif input_str.startswith("PLAY"):

        action2move = []
        _directions_2 = [(2, 2), (2, 1), (2, 0), (2, -1), (2, -2), (1, -2), (0, -2), (-1, -2), (-2, -2), (-2, -1),
                         (-2, 0), (-2, 1), (-2, 2), (-1, 2), (0, 2), (1, 2)]

        for x in range(7):
            for y in range(7):
                action2move.append((None, None, x, y))

        for x in range(7):
            for y in range(7):
                for dx, dy in _directions_2:
                    if {x, y, x + dx, y + dy} <= set(range(7)):
                        action2move.append((x, y, x + dx, y + dy))

        action2move.append((None, None, None, None))

        g = AtaxxGame()
        args1 = dotdict({'numMCTSSims': 2000, 'cpuct': 1.0})
        n1 = NNet(g)
        n1.load_checkpoint('.', 'best.pth.tar')
        mcts1 = MCTS(g, n1, args1)
        n1p = lambda x: np.argmax(mcts1.getActionProb(x, temp=0))

        player = __file__[2]
        board = []
        actions = {}  # { key: piece(start position), value: list of position(destination position) }

        # make board
        input_lines = input_str.split("\n")
        for i in range(7):
            line = input_lines[i+1].split(" ")
            dic = {1: -1, 2: 1, 0: 0}
            line = [dic.get(n, n) for n in line]
            board.append(line)

        action = n1p(np.array(board))

        move = action2move[action]

        if move[0] is None:
            a, b = find_any_close_position(board, move[2], move[3])
            sys.stdout.write(f"{a} {b} {move[2]} {move[3]}")
        else:
            sys.stdout.write(f"{move[0]} {move[1]} {move[2]} {move[3]}")

        # for row in range(7):
        #     for col in range(7):
        #         if board[row][col] == player:
        #             moveable_positions = []
        #             for i in range(max(row-2, 0), min(row+3, 7)):
        #                 for j in range(max(col-2, 0), min(col+3, 7)):
        #                     if board[i][j] == "0":
        #                         moveable_positions.append((i, j))
        #             if moveable_positions:
        #                 actions[(row, col)] = moveable_positions
        #
        # piece, positions = random.choice(list(actions.items()))
        # position = random.choice(positions)
