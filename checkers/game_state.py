from itertools import chain
from functools import reduce


class GameState:
    def __init__(self, board, parent=None, max_player=True):
        self.board = board
        self.max_player = max_player
        self.parent = parent

    def __eq__(self, other):
        return (self.board == other.board and
                self.max_player == other.max_player)

    def heuristic(self):
        return reduce(
            lambda x, y: x + y.value(),
            chain.from_iterable(zip(*self.board.board)),
            0)

    def get_children(self):
        if not hasattr(self, 'children'):
            self.children = self._generate_children()

        return self.children

    def _generate_children(self):
        # print("GET CHILDREN CALLED: ", self.board.board)
        next_player = False if self.max_player else True
        return [GameState(board, self, next_player)
                for board in self.board.generate_child_boards(self.max_player)]
