import customtkinter

from front.chessboard import Board


class BoardContainer(customtkinter.CTkFrame):
    def __init__(self, master, stockfish, **kwargs):
        super().__init__(master, **kwargs)

        # self.grid_rowconfigure(0, weight=1)
        # self.grid_columnconfigure(0, weight=1)

        self.board = Board(master=self, width=480, height=480, stockfish=stockfish)
        self.board.grid(row=0, column=0,
                        sticky="nsew",
                        padx=10, pady=10)
