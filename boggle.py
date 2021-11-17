from boggle_model import GameModel
from boggle_GUI import GUIMenu


class Controller:

    def __init__(self, boggle_dict):
        """
        this method sets a new game model, create pointers for essential methods in
        the model, and then initialize the GUI with those pointers
        """
        self.boggle_dict = boggle_dict
        self._game_model = GameModel(boggle_dict)
        self.board = self._game_model.get_board()
        self.current_word = self._game_model.get_current_word
        self.guessed_words = self._game_model.get_words_guessed
        self.my_score = self._game_model.get_score
        self._game_gui = GUIMenu(self.board, self._game_model.game_loop, self.current_word, self.guessed_words, self.my_score, self.set_new_game)

    def set_new_game(self):
        """
        this function resets the GUI with a new game model
        """
        self._game_model = GameModel(self.boggle_dict)
        self.board = self._game_model.get_board()
        self.current_word = self._game_model.get_current_word
        self.guessed_words = self._game_model.get_words_guessed
        self.my_score = self._game_model.get_score
        self._game_gui.init_new_game_param(self.board, self._game_model.game_loop, self.current_word, self.guessed_words, self.my_score)

    def run(self):
        self._game_gui.run()


if __name__ == '__main__':
    x = Controller("boggle_dict.txt")
    x.run()
