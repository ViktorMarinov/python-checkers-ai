import unittest

import sys
checkers_path = sys.path.insert(0, '..')
from checkers.checkers import *

FILE_NAME = "test_file.csv"


class ShashkiTests(unittest.TestCase):

    def setUp(self):
        self.file_name = FILE_NAME
        parser = CsvFileParser(self.file_name)
        self.board = parser.get_as_list()
        self.checkers = CheckersBoard(self.board)

    def test_file_can_be_read(self):
        self.assertNotEqual(self.board, [])

    def test_board_has_right_number_of_rows_and_cols(self):
        self.assertEqual(len(self.board), 8)

        for row in self.board:
            self.assertEqual(len(row), 8)

    def test_game_state_eq(self):
        game_state = GameState(self.board)
        game_state2 = GameState(self.board)
        self.assertTrue(game_state == game_state2)

    def test_game_state_heuristic(self):
        game_state = GameState(self.checkers)
        expected = 9 - 10
        self.assertEqual(expected, game_state.heuristic())

    def test_field_get_available_moves(self):
        board = [['O', 'O', 'O', 'O'],
                 ['O', 'O', 'O', 'O'],
                 ['O', 'O', 'O', 'Oo'],
                 ['', '', '', ''],
                 ['', '', '', ''],
                 ['X', 'X', 'X', 'X'],
                 ['X', 'X', 'X', 'X'],
                 ['X', 'X', 'X', 'X']]
        self.checkers = CheckersBoard(board)
        expected = [(3, 0), (3, 1)]
        field = self.checkers.get_field(2, 0)
        field2 = self.checkers.get_field(7, 2)
        self.assertEqual(expected, field.get_available_moves())
        self.assertEqual([(6, 1), (6, 2)], field2.get_available_moves())

    def test_field_get_available_moves_crowned(self):
        field = self.checkers.get_field(2, 3)
        expected = [(1, 3), (3, 3)]
        self.assertEqual(expected, field.get_available_moves())

    def test_checkboard_copy(self):
        new_one = copy(self.checkers)
        print("OLD ONE: ", self.checkers)
        for field in self.checkers.board:
            print(field)
        row1 = new_one.board[0]
        new_one.board[1] = row1
        print("NEW ONE: ", new_one)
        for field in new_one.board:
            print(field)
        self.assertNotEqual(new_one, self.checkers)


if __name__ == '__main__':
    unittest.main()
