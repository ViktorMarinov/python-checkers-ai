import sys

from .csv_file_parser import CsvFileParser
from .checkers_board import CheckersBoard
from .game_state import GameState

from functools import total_ordering


@total_ordering
class ValueStatePair:
    def __init__(self, value, state):
        self.value = value
        self.state = state

    def __eq__(self, other):
        return self.value == other.value

    def __lt__(self, other):
        return self.value < other.value


def find_best_move(
        state, depth=3, alpha=float('-inf'),
        beta=float('inf'), max_player=True):
    if depth is 0:
        return ValueStatePair(state.heuristic(), state)

    children = state.get_children()
    if max_player:
        if not children:
            return ValueStatePair(-30, state)
        value = float('-inf')
        for child in children:
            pair = max(
                ValueStatePair(value, state),
                find_best_move(child, depth - 1, alpha, beta, False))
            alpha = max(alpha, value)
            if beta < alpha:
                break
    else:
        if not children:
            return ValueStatePair(30, state)
        value = float('inf')
        for child in children:
            pair = min(
                ValueStatePair(value, state),
                find_best_move(child, depth - 1, alpha, beta, True))
            beta = min(beta, value)
            if beta < alpha:
                break

    return pair


def trace_parents(state, root):
    if state.parent is root:
        print("======== BEST MOVE ========")
        state.board.print_board()
    else:
        trace_parents(state.parent, root)


if __name__ == '__main__':
    file_name = sys.argv[1]
    parser = CsvFileParser(file_name)
    game_board = CheckersBoard(parser.get_as_list())
    game_state = GameState(game_board)
    pair = find_best_move(game_state)
    value, state = pair.value, pair.state
    trace_parents(state, root=game_state)
