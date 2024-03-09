import customtkinter
from front.chessboard import Piece


class Square(customtkinter.CTkFrame):
    """
    A square on the chess board.

    Parameters:
        master (Tk): The master window.
        square_color (str): The color of the square.
        **kwargs: Additional keyword arguments.

    Attributes:
        square_color (str): The color of the square.
    """

    def __init__(self, master, width, height, square_color, file, rank, **kwargs):
        """
        Initialize the Square.

        Parameters:
            master (Tk): The master window.
            square_color (str): The color of the square.
            **kwargs: Additional keyword arguments.
        """
        super().__init__(master, width=width, height=height, **kwargs)

        self.square_color = square_color
        self.configure(fg_color=square_color)

        self.piece = None
        self.rank = rank
        self.file = file
        # self.bind("<Enter>", self.on_enter)
        # self.bind("<Leave>", self.on_leave)

    def on_enter(self):
        """
        Event handler for the mouse entering the square. Highlights the square.
        """
        self.configure(bg="lightblue")

    def on_leave(self):
        """
        Event handler for the mouse leaving the square. Un-highlights the square.
        """
        self.configure(bg=self.square_color)

    def place_piece(self, piece):
        """
        Place a piece on the square.

        Parameters:
            piece (Piece): The piece to be placed on the square.
        """
        self.piece = piece
