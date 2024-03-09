import chess
import customtkinter
from front.popup_windows import PopupWindow
from back.utils import BoardUtils


class MenuContainer(customtkinter.CTkFrame):
    def __init__(self, master, dialog_event, add_dialog, **kwargs):
        super().__init__(master, **kwargs)
        self.board = None

        self.fen_text = None

        self.best_move_button = None
        self.new_game_button = None
        self.chat_button = None
        self.insert_fen_button = None
        self.insert_fen_text = None
        self.create_buttons()
        self.dialog_event = dialog_event
        self.add_dialog = add_dialog
        self.dialog_is_displayed = False

    def add_board(self, board):
        self.board = board

    def set_new_game(self):
        if self.board is not None:
            self.board.initial_board()
        else:
            raise "None Board"

    def load_from_fen(self):
        fen_text = self.insert_fen_text.get("1.0", "end-1c").strip()
        fen_text = fen_text.lstrip()
        fen_text = fen_text.rstrip()
        if not fen_text:
            empty_fen = PopupWindow(self.master, "Empty Fen", "You cannot insert an empty Fen!")
        elif not BoardUtils.is_valid_fen(fen_text):
            invalid_fen = PopupWindow(self.master, "Invalid Fen", "This Fen is invalid, please insert another one!")
        else:
            self.fen_text = fen_text
            self.board.load_from_fen(self.fen_text)

    def show_chat_window(self):
        if self.dialog_is_displayed:
            self.dialog_event("hide")
            self.chat_button.configure(text="Start chat with Bot")
        else:
            self.dialog_event("show")
            self.chat_button.configure(text="End chat with Bot")

        # Set the dialog_is_displayed flag
        self.dialog_is_displayed = not self.dialog_is_displayed

    def get_best_move(self):
        if not self.dialog_is_displayed:
            self.show_chat_window()
        print("before")
        print(self.board.fen)
        _, explain = self.board.get_best_move(self.board.fen)
        print(explain)
        self.add_dialog("What's the best move?", 1)
        self.add_dialog(explain)

    def create_buttons(self):
        """
        Create the buttons of the menu.
        """
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)
        self.grid_columnconfigure(2, weight=1)
        self.grid_columnconfigure(3, weight=1)
        self.grid_columnconfigure(4, weight=1)

        self.grid_rowconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)

        best_move_button = customtkinter.CTkButton(self, 50, 30, text=f"Get Best Move", command=self.get_best_move)
        best_move_button.grid(row=0, column=0, sticky="nsew", pady=10)

        new_game_button = customtkinter.CTkButton(self, 50, 30, text=f"New Game", command=self.set_new_game)
        new_game_button.grid(row=0, column=2, sticky="nsew", pady=10)

        chat_button = customtkinter.CTkButton(self, 50, 30, text=f"Start chat with Bot", command=self.show_chat_window)
        chat_button.grid(row=0, column=4, sticky="nswe", pady=10)

        insert_fen_button = customtkinter.CTkButton(self, 50, 30, text="Insert Fen", command=self.load_from_fen)
        insert_fen_button.grid(row=1, column=2, sticky="nswe", pady=10)

        insert_fen_text = customtkinter.CTkTextbox(self, 100, 30)
        insert_fen_text.grid(row=1, column=4, sticky="nswe", pady=10)

        self.best_move_button = best_move_button
        self.new_game_button = new_game_button
        self.chat_button = chat_button
        self.insert_fen_button = insert_fen_button
        self.insert_fen_text = insert_fen_text
