import tkinter as tki
import tkinter.messagebox
import sys
import pygame
import time
from datetime import datetime
import tkinter.scrolledtext as st

BG_X_SIZE = 1008
BG_Y_SIZE = 586

EXIT = "EXIT"
CHECK = "CHECK"
CORRECT = "CORRECT"
WRONG = "WRONG"
NEW_CHOICE = "NEW_CHOICE"
UNDO = "UNDO"
INVALID_CHOICE = "INVALID_CHOICE"
BOARD_SIZE_STR = "1008x586"
STANDBY_TIME = 3500
GAME_ROUND_TIME = 179
FINISH_MESSAGE = 'Do you want to play another game?'
DEFAULT_COLOR = 'orange'
CHOSEN_COLOR = 'goldenrod3'
ON_ENTER_COLOR = 'LightGoldenRod1'
INVALID_CHOICE_COLOR = 'red3'


class GUIMenu:

    def __init__(self, board, game_loop_func, get_current_word_func,
                 get_guessed_func, get_score_func, set_new_game_func):

        # Create object
        root = tki.Tk()
        self._main_window = root
        root.title("Boggle")
        pygame.mixer.init()
        self.board = board
        self.game_loop = game_loop_func
        self.current_word = get_current_word_func
        self.guessed_words = get_guessed_func
        self.current_score = get_score_func
        self.time_over = False
        self.init_func = set_new_game_func
        self.mat_button = [[None, None, None, None], [None, None, None, None],
                           [None, None, None, None], [None, None, None, None]]
        # Adjust size
        root.geometry(BOARD_SIZE_STR)
        root.resizable(False, False)
        self.gui_menu(root)

    def init_new_game_param(self, board, game_loop_func, get_current_word_func,
                            get_guessed_func, get_score_func):
        """
        this method changes the appearance of the game, due to a new initialized
        game model. it also resets a new countdown clock
        """
        self.board = board
        self.game_loop = game_loop_func
        self.current_word = get_current_word_func
        self.guessed_words = get_guessed_func
        self.current_score = get_score_func
        self.time_over = False

    def gui_menu(self, root):
        """
        this method defines the menu window of the game (background and buttons)
        """
        self.bg_image = tki.PhotoImage(file="Main_Pic.gif")
        self.start_image = tki.PhotoImage(file="play_button.gif")
        self.exit_image = tki.PhotoImage(file="exit_button.gif")

        # Create Canvas
        self.menu_canvas = tki.Canvas(root, width=BG_X_SIZE, height=BG_Y_SIZE)
        self.menu_canvas.pack(fill="both", expand=True)
        # Display image
        self.menu_canvas.create_image(0, 0, image=self.bg_image,
                                      anchor="nw")
        # Create Buttons
        exit_button = tki.Button(root, image=self.exit_image, borderwidth=0,
                                 command=self.end_game)
        play_button = tki.Button(root, image=self.start_image, borderwidth=0,
                                 command=self.start_game, )
        # Display Buttons
        button1_canvas = self.menu_canvas.create_window(10, 10,
                                                        anchor="nw",
                                                        window=exit_button)
        button2_canvas = self.menu_canvas.create_window(410, 235,
                                                        anchor="nw",
                                                        window=play_button)

    def start_game(self):
        """
        this method starts the 'countdown_music' while erasing the start menu
        """
        pygame.mixer.music.load("countdown_music.mp3")
        pygame.mixer.music.play()
        self.menu_canvas.pack_forget()
        self.count_down_menu()

    def count_down_menu(self):
        """
        this method shows the stand-by window for 3.5 seconds
        """
        self.countdown_image = tki.PhotoImage(file="count_down_image.gif")
        self.countdown_canvas = tki.Canvas(self._main_window, width=BG_X_SIZE,
                                           height=BG_Y_SIZE)
        self.countdown_canvas.pack(fill="both", expand=True)
        self.countdown_canvas.create_image(0, 0, image=self.countdown_image,
                                           anchor="nw")
        self._main_window.after(STANDBY_TIME, self.gui_game)

    def gui_game(self):
        """
        this method defines the game window
        """
        # playing the 'game_music' in channel 0 to allow other sounds to be played
        pygame.mixer.Channel(0).play(pygame.mixer.Sound('game_music.mp3'))

        self.countdown_canvas.pack_forget()
        self.game_bg = tki.PhotoImage(file="game_bg.gif")
        self.game_canvas = tki.Canvas(self._main_window, width=BG_X_SIZE,
                                      height=BG_Y_SIZE)
        self.game_canvas.pack(fill="both", expand=True)
        self.game_canvas.create_image(0, 0, image=self.game_bg, anchor="nw")

        ###

        self.check_image = tki.PhotoImage(file="check_button.gif")
        check_button = tki.Button(self._main_window, image=self.check_image,
                                  borderwidth=0, command=self.check_clicked)
        button2_canvas = self.game_canvas.create_window(470, 40,
                                                        anchor="nw",
                                                        window=check_button)

        ###

        exit_button = tki.Button(self._main_window, image=self.exit_image,
                                 borderwidth=0,
                                 command=self.end_game)
        # Display Buttons
        button1_canvas = self.game_canvas.create_window(10, 10,
                                                        anchor="nw",
                                                        window=exit_button)

        ###

        self.create_grid(self._main_window, self.board)

        ###

        self.current_combination = tki.Label(self.game_canvas,
                                             font="Ariel 32 bold", height=1,
                                             width=13, borderwidth=10,
                                             anchor='w', bg='peach puff',
                                             highlightthickness=2,
                                             highlightbackground="black",
                                             foreground="black",
                                             relief="ridge")
        self.current_combination.place(x=82, y=37)

        ###

        self.guessed_frame = tki.Frame(relief="ridge")
        self.guessed_frame.place(x=234, y=120)
        self.guessed = st.ScrolledText(self.guessed_frame,
                                       width=12,
                                       height=11,
                                       font="Ariel 20 bold", bg='sandy brown',
                                       highlightthickness=2, borderwidth=13,
                                       highlightbackground="black",
                                       foreground="white", relief="ridge")
        self.guessed.grid(column=0)

        ###

        self.score = tki.Label(self.game_canvas,
                               font="Ariel 20 bold", height=3,
                               width=7, borderwidth=10,
                               bg='orange',
                               highlightthickness=2,
                               highlightbackground="black",
                               foreground="orange red", relief="ridge")
        self.score['text'] = "Score:\n0"
        self.score.place(x=82, y=120)

        ###

        self.clock = tki.Label(self.game_canvas, anchor='w',
                               font="Ariel 20 bold", height=1,
                               width=11, borderwidth=10,
                               bg='black',
                               highlightthickness=2,
                               highlightbackground="white",
                               foreground="white", relief="ridge")
        self.clock.place(x=234, y=510)

        self.initialize_clock()

    def initialize_clock(self):
        """
        this method sets the starting time for the clock animation
        """
        self.start_time = datetime.now()
        self.clock_animation()

    def clock_animation(self):
        """
        this method calculates the remaining time the player has, displays it
        on the screen and checks if 3 minutes passed since the game started
        """
        current_time = datetime.now()
        delta_time = current_time - self.start_time
        # to create a 'countdown'
        current_clock = GAME_ROUND_TIME - int(delta_time.seconds)
        current_minutes = current_clock // 60
        current_seconds = current_clock % 60
        if current_seconds // 10 == 0:
            current_seconds = "0" + str(current_seconds)
        # we take the 2 first digits which represent the current time,
        # in microseconds
        current_mil_seconds = 99 - delta_time.microseconds // 10000
        if current_mil_seconds // 10 == 0:
            current_mil_seconds = "0" + str(current_mil_seconds)

        self.clock["text"] = "    0" + str(current_minutes) + ":" + str(
            current_seconds) + ":" + str(current_mil_seconds)
        # in case the game runs for over 179 seconds
        if delta_time.seconds >= GAME_ROUND_TIME:
            self.clock["text"] = "00:00:00"
            self.time_over = True
            self._main_window.after_cancel(self.clock_id)
            self.is_finished()
            return
        self.clock_id = self._main_window.after(50, self.clock_animation)

    def is_finished(self):
        """
        this method asks the player (after the tim is over) if he wants to quit
        or play another game
        """
        if self.time_over:
            msg_box = tkinter.messagebox.askquestion('Game Ended',
                                                    FINISH_MESSAGE,
                                                    icon='question')
            if msg_box == 'yes':
                self.game_canvas.pack_forget()
                # initializes a new model (outside function)
                self.init_func()
                self.gui_menu(self._main_window)
            else:
                self.end_game()
            return

    def create_grid(self, root, board):
        """
        this method initializes all the buttons in the grid frame
        """
        self.grid_frame = tki.Frame(root, bg="blue")
        self.grid_frame.pack(expand=True)
        tki.Grid.columnconfigure(self.grid_frame, 4, weight=22)
        tki.Grid.rowconfigure(self.grid_frame, 4, weight=22)
        for i in range(len(board)):
            for j in range(len(board[0])):
                self.create_button(i, j, board[i][j])
        frame_canvas = self.game_canvas.create_window(470, 150, anchor="nw",
                                                      window=self.grid_frame)

    def create_button(self, i, j, letter):
        """
        this method creates a new button, according to a given position and
        text
        """
        bt1 = tki.Button(self.grid_frame, text=letter,
                         font="Ariel 32 bold", borderwidth=10, width=4,
                         height=1,
                         highlightbackground='goldenrod1',
                         command=lambda: self.curr_button(i, j))
        bt1['bg'] = DEFAULT_COLOR
        bt1.grid(row=i, column=j, sticky=tki.NSEW)
        self.mat_button[i][j] = bt1

        def _on_enter(event):
            if bt1['background'] == DEFAULT_COLOR:
                bt1['background'] = ON_ENTER_COLOR

        def _on_leave(event):
            if bt1['background'] == ON_ENTER_COLOR:
                bt1['background'] = DEFAULT_COLOR

        bt1.bind("<Enter>", _on_enter)
        bt1.bind("<Leave>", _on_leave)

    def curr_button(self, i, j):
        """
        this method calls the game loop function (a game model function)
        """
        event = self.game_loop((i, j))
        self.click_result(event, i, j)
        # we update the current combination according to the current_word, which
        # is a part of the game model (self.current_word() is a getter)
        self.current_combination['text'] = self.current_word()

    def check_clicked(self):
        """
        this method checks if the current combination is a valid word or not,
        using the game loop function of the model
        """
        event = self.game_loop(CHECK)
        self.click_result(event)
        self.current_combination['text'] = self.current_word()
        self.undo_all_colors()

    def click_result(self, event, i=None, j=None):
        """
        this method updates the game according to the result given from
        the game loop function of the model
        """
        if event == NEW_CHOICE:
            pygame.mixer.music.load("single_click.mp3")
            pygame.mixer.music.play()
            self.mat_button[i][j]['background'] = CHOSEN_COLOR
        elif event == INVALID_CHOICE:
            pygame.mixer.music.load("error_sound.mp3")
            pygame.mixer.music.play()
            self.flash_incorrect(i, j)
        elif event == UNDO:
            pygame.mixer.music.load("erase_sound.mp3")
            pygame.mixer.music.play()
            self.mat_button[i][j]['background'] = DEFAULT_COLOR
        elif event == CORRECT:
            pygame.mixer.music.load("ta_da_sound.mp3")
            pygame.mixer.music.play()
            new_str = " " + self.guessed_words()[-1] + '\n'
            self.guessed.insert(tki.INSERT, new_str)
            self.score['text'] = 'Score:\n' + str(self.current_score())
        elif event == WRONG:
            pygame.mixer.music.load("fail_sound.mp3")
            pygame.mixer.music.play()

    def undo_all_colors(self):
        """
        this method changes all buttons color to orange
        """
        for i in range(len(self.mat_button)):
            for j in range(len(self.mat_button[0])):
                self.mat_button[i][j]['background'] = DEFAULT_COLOR

    def flash_incorrect(self, i, j):
        """
        this method changes the color of the button (in the i,j place) to red
        for 150 microseconds
        """
        if self.mat_button[i][j]['background'] != CHOSEN_COLOR:
            self.mat_button[i][j]['background'] = INVALID_CHOICE_COLOR
            self._main_window.after(150, lambda: self.return_to_default_color(i, j))
        else:
            self.mat_button[i][j]['background'] = INVALID_CHOICE_COLOR
            self._main_window.after(150, lambda: self.return_to_chosen_color(i, j))

    def return_to_default_color(self, i, j):
        self.mat_button[i][j]['background'] = DEFAULT_COLOR

    def return_to_chosen_color(self, i, j):
        self.mat_button[i][j]['background'] = CHOSEN_COLOR

    def end_game(self):
        """
        this method play "ending_sound" sound and ends the program (after 0.4 microseconds)
        """
        pygame.mixer.Channel(0).pause()
        pygame.mixer.music.load("ending_sound.mp3")
        pygame.mixer.music.play()
        time.sleep(0.4)
        sys.exit()

    def run(self):
        self._main_window.mainloop()
