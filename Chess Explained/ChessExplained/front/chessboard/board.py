import customtkinter

from back.stockfish_tools import StockfishExplainer
from front.chessboard import Square
from front.chessboard import Piece
import chess


class Board(customtkinter.CTkFrame):

    def __init__(self, master, stockfish, **kwargs):

        super().__init__(master, **kwargs)
        # self.grid_columnconfigure((0, 1, 2, 3, 4, 5, 6, 7), weight=1)
        # self.grid_rowconfigure((0, 1, 2, 3, 4, 5, 6, 7), weight=1)

        self.squares = []
        self.create_squares()
        self.menu = None
        self.stockfish = stockfish
        self.selected_piece = None
        self.legal_moves = []
        self.fen = None

    def create_squares(self):
        """
        Create the squares of the chess board.
        """
        for rank in range(8):
            squares_file = []
            for file in range(8):
                square_color = "white" if (rank + file) % 2 == 0 else "gray"
                square = Square(self, 60, 60, square_color, file, rank)
                square.grid(row=rank, column=file, sticky="nsew")
                squares_file.append(square)
                square.bind("<Button-1>", lambda event, f=file, r=rank: self.on_board_click(event, f, r))
            self.squares.append(squares_file)

    def load_from_fen(self, fen):
        """
        Load the board from a fen.
        :param fen:
        :return:
        """
        self.fen = fen
        # Clean the board
        self.clean_board()

        # Set up the board with the fen
        self.stockfish.setup(fen)

        for piece, square_rank, square_file in self.stockfish.get_occupied_squares():
            # Get the piece type and color
            piece_color = piece.color
            piece_type = piece.symbol()

            # Get the square
            square = self.squares[7 - square_rank][square_file]

            # Place the piece on the square
            piece = Piece(color=piece_color, piece_type=piece_type, position=(square_rank, square_file))
            square.place_piece(piece)
        self.print_board()

    def initial_board(self):
        """
        Create the initial board.

        """
        starting_fen = chess.STARTING_FEN
        self.load_from_fen(starting_fen)

    def add_menu(self, menu):
        self.menu = menu

    def clean_board(self):
        """
        Clean the board.
        """
        for piece, square_rank, square_file in self.stockfish.get_occupied_squares():
            # Get the square
            square = self.squares[7 - square_rank][square_file]

            # Delete the piece on the square
            square.place_piece(None)
            for widget in square.winfo_children():
                widget.destroy()

    def print_board(self):
        for squares_file in self.squares:
            for square in squares_file:
                if square.piece is not None:
                    piece_image = customtkinter.CTkLabel(master=square, image=square.piece, text="")
                    piece_image.grid(row=square.rank, column=square.file,
                                     sticky="nsew")
                    piece_image.bind("<Button-1>", lambda event, f=square.file, r=square.rank: self.on_board_click(event, f, r))

    def on_board_click(self, _, file, rank):
        rank = 7 - rank
        position = chess.square_name(chess.square(file, rank))
        print(f"Clicked position: {position}")
        if self.selected_piece is None:
            self.selected_piece = position
            self.legal_moves = self.stockfish.moves_by(self.selected_piece)
            print(f"Legal moves: {self.legal_moves}")

            if not self.legal_moves:
                self.selected_piece = None
                self.legal_moves = []
        else:
            # check if the move is in the legal moves
            # get second of tuple

            for move in self.legal_moves:
                if position in move:
                    print(f"Move: {move}")
                    self.stockfish.move(move)
                    fen = self.stockfish.get_fen()
                    self.stockfish.undo()
                    self.load_from_fen(fen)
                    break

                # check for castling
                if (
                    position == "g1" and "O-O" in self.legal_moves
                   or position == "g8" and "O-O" in self.legal_moves
                ):
                    print(f"Move: O-O")
                    self.stockfish.move("O-O")
                    fen = self.stockfish.get_fen()
                    self.stockfish.undo()
                    self.load_from_fen(fen)
                    break

                if (
                    position == "c1" and "O-O-O" in self.legal_moves
                   or position == "c8" and "O-O-O" in self.legal_moves
                ):
                    print(f"Move: O-O-O")
                    self.stockfish.move("O-O-O")
                    fen = self.stockfish.get_fen()
                    self.stockfish.undo()
                    self.load_from_fen(fen)
                    break


            self.selected_piece = None
            self.legal_moves = []

    def get_best_move(self, fen):
        explainer = StockfishExplainer(self.stockfish)
        if fen is None:
            starting_fen = chess.STARTING_FEN
            self.stockfish.setup(starting_fen)
        else:
            self.stockfish.setup(fen)
        board, explain = explainer.explain()
        # print(explain)
        return board, explain
