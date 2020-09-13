# Created by Lee, Jun Seok <lego3410@gmail.com> at Sep 6, 2020

_directions_1 = [(1, 1), (1, 0), (1, -1), (0, -1), (-1, -1), (-1, 0), (-1, 1), (0, 1)]
_directions_2 = [(2, 2), (2, 1), (2, 0), (2, -1), (2, -2), (1, -2), (0, -2), (-1, -2), (-2, -2), (-2, -1), (-2, 0),
                 (-2, 1), (-2, 2), (-1, 2), (0, 2), (1, 2)]


class Board:
    def __init__(self, n=7):
        self.n = n
        self.pieces = [[0] * self.n for _ in range(self.n)]

        self.pieces[0][0] = 1
        self.pieces[0][-1] = -1
        self.pieces[-1][0] = -1
        self.pieces[-1][-1] = 1

    def __getitem__(self, index):
        return self.pieces[index]

    def countDiff(self, color):
        """Counts the # pieces of the given color
        (1 for white, -1 for black, 0 for empty spaces)"""
        count = 0
        for y in range(self.n):
            for x in range(self.n):
                if self[x][y] == color:
                    count += 1
                if self[x][y] == -color:
                    count -= 1
        return count

    def get_legal_moves(self, color):
        moves = []
        for x0 in range(self.n):
            for y0 in range(self.n):
                for x1 in range(self.n):
                    for y1 in range(self.n):
                        dx = x1 - x0
                        dy = y1 - y0
                        if self[x0][y0] == color and self[x1][y1] == 0:
                            if (dx, dy) in _directions_1:
                                moves.append((None, None, x1, y1))
                            elif (dx, dy) in _directions_2:
                                moves.append((x0, y0, x1, y1))
        return moves

    def has_legal_moves(self, color):
        for x0 in range(self.n):
            for y0 in range(self.n):
                for x1 in range(self.n):
                    for y1 in range(self.n):
                        dx = x1 - x0
                        dy = y1 - y0
                        if (dx, dy) in _directions_1 or (dx, dy) in _directions_2:
                            if self[x0][y0] == color and self[x1][y1] == 0:
                                return True

        return False

    def execute_move(self, move, color):
        x0, y0, x1, y1 = move

        if x1 == y1 == None:
            return

        assert self[x1][y1] == 0
        if x0 == y0 == None:
            assert len([0 for _dx, _dy in _directions_1 if
                        {x1 + _dx, y1 + _dy} <= set(range(7)) and self[x1 + _dx][y1 + _dy] == color]) > 0

        else:
            dx, dy = x1 - x0, y1 - y0
            assert (-2 <= dx <= 2 and -2 <= dy <= 2)
            assert self[x0][y0] == color
            assert (dx, dy) in _directions_2
            self[x0][y0] = 0

        self[x1][y1] = color

        for _dx, _dy in _directions_1:
            if {x1 + _dx, y1 + _dy} <= set(range(7)):
                if self[x1 + _dx][y1 + _dy] == -color:
                    self[x1 + _dx][y1 + _dy] = color
