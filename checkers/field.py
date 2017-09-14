class Field:
    def __init__(self, row, col, symbol):
        self.row = row
        self.col = col
        self.symbol = symbol

    def __eq__(self, other):
        return self.row == other.row and self.col == other.col

    def copy(self):
        return Field(self.row, self.col, self.symbol)

    def is_max_players(self):
        return 'X' in self.symbol

    def is_min_players(self):
        return 'O' in self.symbol

    def is_crowned(self):
        return self.symbol == 'Xx' or self.symbol == 'Oo'

    def is_empty(self):
        return self.symbol == ''

    def crown(self):
        if self.is_max_players():
            self.symbol = 'Xx'
        elif self.is_min_players():
            self.symbol = 'Oo'

    def remove(self):
        self.symbol = ''

    def get_available_moves(self):
        rows = []
        if self.is_crowned():
            rows = [self.row - 1, self.row + 1]
        elif self.is_max_players():
            rows = [self.row - 1]
        elif self.is_min_players():
            rows = [self.row + 1]

        if self.row % 2 == 0:
            cols = [self.col, self.col + 1]
        else:
            cols = [self.col - 1, self.col]

        rows = filter(lambda i: i >= 0 and i < 8, rows)
        cols = filter(lambda i: i >= 0 and i < 4, cols)
        return [(x, y) for x in rows for y in cols]

    def value(self):
        s = self.symbol
        if s == 'X':
            return 1
        elif s == 'Xx':
            return 2
        elif s == 'O':
            return -1
        elif s == 'Oo':
            return -2
        return 0
