import customtkinter
from customtkinter import CTk, set_appearance_mode

from back.stockfish_tools import Stockfish
from front.containers import DialogContainer
from front.containers import MenuContainer
from front.containers import BoardContainer


class App(CTk):
    def __init__(self, engine_path, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.engine_path = engine_path
        self.stockfish = Stockfish(engine_path=self.engine_path)
        self.title("Chess Explained")
        self.geometry("680x680")
        self.minsize(1080, 680)
        self.resizable(True, True)

        # Center the content
        self.grid_rowconfigure(1, weight=1)
        self.grid_columnconfigure((0, 1, 2), weight=1)

        self.menu = MenuContainer(master=self, dialog_event=self.dialog_event, add_dialog=self.add_dialog)
        self.menu.grid(row=0, column=1,
                       sticky="nsew",
                       padx=10, pady=10)

        self.board_container = BoardContainer(master=self, stockfish=self.stockfish)
        self.board_container.grid(row=1, column=1,
                                  sticky="nsew",
                                  padx=10, pady=10)

        self.dialog = DialogContainer(master=self, width=50, height=680)

        # self.dialog.grid(row=0, column=2,
        #                  columnspan=10, rowspan=10,
        #                  sticky="nsew",
        #                  padx=10, pady=10)
        # self.dialog.grid_remove()

        # self.board.add_menu(self.menu)
        # self.menu.add_board(self.board)

        self.board_container.board.add_menu(self.menu)
        self.menu.add_board(self.board_container.board)

        # Set the theme
        set_appearance_mode("dark")
        customtkinter.set_default_color_theme("dark-blue")

        self.mainloop()

    def dialog_event(self, event):
        if event == "show":
            self.dialog.grid(row=0, column=2,
                             columnspan=10, rowspan=10,
                             sticky="nsew",
                             padx=10, pady=10)
        elif event == "hide":
            self.dialog.grid_remove()
        else:
            raise ValueError(f"Unknown event {event}")

    def add_dialog(self, text,turn=0):
        self.dialog.add_text(text,turn)
