import sys
from .field import Field


class CheckersBoard:
    """
    This class contains a board with the available fields only
    (only black fields are available to play)
    """
    def __init__(self, table=[]):
        fields = [
            [field
             for col_index, field
             in enumerate(row)
             if (row_index + col_index) % 2 == 1]
            for row_index, row in enumerate(table)]
        self.board = [[Field(i, j, symbol)
                       for j, symbol in enumerate(row)]
                      for i, row in enumerate(fields)]

    def __eq__(self, other):
        return self.board == other.board

    def get_field(self, row, col):
        return self.board[row][col]

    def delete_field(self, row, col):
        self.get_field(row, col).remove()

    def swap(self, field1, field2):
        temp = field1.symbol
        field1.symbol = field2.symbol
        field2.symbol = temp

    def print_board(self):
        for index, row in enumerate(self.board):
            for field in row:
                if index % 2 == 0:
                    sys.stdout.write('#,')
                if field.is_empty():
                    sys.stdout.write('_')
                else:
                    sys.stdout.write(field.symbol)
                if index % 2 == 1:
                    sys.stdout.write(',#')
                sys.stdout.write(',')
            sys.stdout.write('\n')

    def generate_child_boards(self, is_max_player):
        result = []
        for row in self.board:
            for field in row:
                if is_max_player and field.is_max_players():
                    result.extend(self.generate_boards_for_field(field))
                elif not is_max_player and field.is_min_players():
                    result.extend(self.generate_boards_for_field(field))
        return result

    """
    Generates all posible moves for a field.
    If enemy pulls can be taken, other moves are ignored and the max is taken.
    """
    def generate_boards_for_field(self, field):
        moves = field.get_available_moves()
        max_player = field.is_max_players()
        result = []
        max_jumped_over = 0
        best_jump_board = None
        for row, col in moves:
            location = self.get_field(row, col)
            if any([max_player and location.is_min_players(),
                   not max_player and location.is_max_players()]):
                jump_field, jumped_over = self.get_jump_location(
                    field, location, max_player)
                if jump_field is None:
                    continue
                if len(jumped_over) > max_jumped_over:
                    max_jumped_over = len(jumped_over)
                    new_generated = self.get_new(
                        field, jump_field.row, jump_field.col, jumped_over)
                    best_jump_board = new_generated
            elif location.is_empty() and not best_jump_board:
                result.append(self.get_new(field, row, col))

        if best_jump_board:
            return [best_jump_board]
        return result

    """
    Recursive function that finds the next available field to jump to.
    Returns a tuple with the location of the jump and the fields jumped over.
    If no jump is available the location is None.
    """
    def get_jump_location(self, start, _next, is_max_player, jumped_over=[]):
        row, col = start.row, start.col
        if row > _next.row:
            jump_row = _next.row - 1
        else:
            jump_row = _next.row + 1

        if jump_row < 0 or jump_row >= 8:
            return (None, jumped_over)
        if row % 2 == 0:
            jump_col = col + 1 if _next.col > col else col - 1
        else:
            jump_col = col - 1 if _next.col < col else col + 1

        if jump_col < 0 or jump_col >= 4:
            return (None, jumped_over)

        jump_field = self.get_field(jump_row, jump_col)
        if jump_field.is_empty():
            jumped_over.append(_next)
            return (jump_field, jumped_over)
        if any([is_max_player and jump_field.is_min_players(),
               not is_max_player and jump_field.is_max_players()]):
            jumped_over.append(_next)
            return self.get_jump_location(_next, jump_field,
                                          is_max_player, jumped_over)

    """
    Creates a new board with swapped fields and
    elements of delete_list deleted
    """
    def get_new(self, field, row, col, delete_list=[]):
        new_board = self.copy()
        new_field = new_board.get_field(field.row, field.col)
        new_location = new_board.get_field(row, col)
        new_board.swap(new_field, new_location)
        if (new_location.is_max_players() and new_location.row == 0 or
                new_location.is_min_players() and new_location.row == 7):
            new_location.crown()

        for field in delete_list:
            new_board.delete_field(field.row, field.col)
        return new_board

    def copy(self):
        new_checkboard = CheckersBoard([])
        new_checkboard.board = [[field.copy()
                                 for field in row]
                                for row in self.board]
        return new_checkboard

    #  .  1  .  2  .  3  .  4
    #  5  .  6  .  7  .  8  .
    #  .  9  . 10  . 11  . 12
    # 13  . 14  . 15  . 16  .
    #  . 17  . 18  . 19  . 20
    # 21  . 22  . 23  . 24  .
    #  . 25  . 26  . 27  . 28
    # 29  . 30  . 31  . 32  .
