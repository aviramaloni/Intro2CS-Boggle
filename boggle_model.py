from boggle_board_randomizer import *
from ex12_utils import *
from datetime import datetime

EXIT = "EXIT"
CHECK = "CHECK"
CORRECT = "CORRECT"
WRONG = "WRONG"
NEW_CHOICE = "NEW_CHOICE"
UNDO = "UNDO"
INVALID_CHOICE = "INVALID_CHOICE"


class GameModel:

    def __init__(self, boggle_dict):
        self._board = randomize_board()
        self._time = datetime.now()
        self._words_guessed = []
        self._current_word = ""
        self._current_path = []
        words = load_words_dict(boggle_dict)
        self._words = words
        self._score = 0

    def game_loop(self, player_input):
        """
        this method returns an informative message according to the users input
        """
        if player_input == EXIT:
            return EXIT
        elif player_input == CHECK:
            return self.input_is_check()
        else:
            return self.input_is_coordinate(player_input)

    def input_is_check(self):
        """
        in case player_input is CHECK
        """
        if is_valid_path(self._board, self._current_path,
                        self._words) and not is_guessed(
                self._words_guessed, self._current_word):
            self._words_guessed.append(self._current_word)
            length = len(self._current_word)
            self._score += length ** 2
            self._current_word = ""
            self._current_path = []
            return CORRECT
        else:
            self._current_word = ""
            self._current_path = []
            return WRONG

    def input_is_coordinate(self, player_input):
        """
        in case player_input is coordinates
        """
        if player_input in self._current_path[:-1]:
            return INVALID_CHOICE
        elif not len(self._current_path) or are_neighbors(player_input,
                                                          self._current_path[
                                                              -1]):
            self._current_word += self._board[player_input[0]][
                player_input[1]]
            self._current_path.append(player_input)
            return NEW_CHOICE
        elif player_input == self._current_path[-1]:
            self._current_path.pop()
            word_added = self._board[player_input[0]][player_input[1]]
            i = len(word_added)
            self._current_word = self._current_word[:-i]
            return UNDO
        else:
            return INVALID_CHOICE

    def get_current_word(self):
        return self._current_word

    def get_words_guessed(self):
        return self._words_guessed

    def get_score(self):
        return self._score

    def get_board(self):
        return self._board
