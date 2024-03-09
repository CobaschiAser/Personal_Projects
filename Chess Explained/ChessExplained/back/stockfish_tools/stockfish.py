import math

import chess
import chess.engine


class Stockfish:
    """
    Class used to interact with Stockfish engine

    """

    def __init__(self, engine_path):
        """
        Constructor for Stockfish class
        Initializes board and engine path

        :param engine_path: path to Stockfish engine on personal computer
        """

        self.engine_path = engine_path
        self.board = chess.Board()

    def setup(self, fen):
        """
        Set the board to the given FEN

        :param fen: FEN to set the board to
        :return: True if FEN is valid, False otherwise
        """

        try:
            # set the board to the given FEN
            self.board.set_fen(fen)
            return True
        except ValueError:
            print(f"Invalid FEN: {fen}")
            return False

    def move(self, move):
        """
        Make a move on the current board

        :param move: move in SAN notation to be made
        :return: True if move is valid, False otherwise
        """

        try:
            # make the move on the board
            self.board.push_san(move)
            return True
        except ValueError:
            print(f"Invalid move: {move}")
            return False

    def undo(self):
        """
        Undo the last move made on the board

        :return: True if move was undone, False otherwise
        """

        # if there are moves on the stack, pop the last move
        if len(self.board.move_stack) > 0:
            self.board.pop()
            return True
        return False

    def turn(self):
        """
        Get the turn of the board

        :return: turn of the board ('White' or 'Black')
        """

        # return the string representation of the turn
        return "White" if self.board.turn == chess.WHITE else "Black"

    def switch_turn(self):
        """
        Change the turn of the board

        :return: None
        """

        # change the turn of the board
        self.board.turn = not self.board.turn

    def display(self):
        """
        Display the current board

        :return: None
        """

        # print the board
        print(self.board)

    def attacked_pieces(self):
        """
        List squares of pieces that are under attack by the opponent of the current player

        :return: List of squares as strings
        """

        attacked_pieces = []

        # get the color of the opponent
        opponent_color = not self.board.turn

        # loop through all the squares on the board
        for square in chess.SQUARES:

            # get the piece at the square
            piece_at = self.board.piece_at(square)

            # get the color of the piece at the square
            color_at = self.board.color_at(square)

            # check if the square has a piece and it is not the opponent's piece
            if not piece_at or color_at == opponent_color:
                continue

            # check if the square is attacked by the opponent
            if self.board.is_attacked_by(opponent_color, square):
                attacked_pieces.append(chess.square_name(square))

        # return the list of attacked pieces by the opponent
        return attacked_pieces

    def moves(self):
        """
        List all legal moves for the current board

        :return: list of legal moves for the current board in SAN notation
        """

        return [self.board.san(move) for move in self.board.legal_moves]

    def squares(self):
        """
        Tuple of (start_square, end_square) for all legal moves for the current board

        :return: (start_square, end_square) for all legal moves for the current board
        """
        return [(chess.square_name(move.from_square), chess.square_name(move.to_square)) for move in
                self.board.legal_moves]

    def start_end_from_san(self, move):
        """
        Tuple of (start_square, end_square) for the specified move

        :return: (start_square, end_square) for the specified move
        """
        move = self.board.parse_san(move)
        return chess.square_name(move.from_square), chess.square_name(move.to_square)

    def moves_by(self, position):
        """
        List all legal moves for the piece on the specified square index

        :param position: position in SAN notation
        :return: list of legal moves for the piece on the specified position
        """

        # convert the position to square index
        position_index = self.index_from_san(position)

        # get the piece at the specified index
        piece = self.board.piece_at(position_index)

        if piece is None:
            return []

        # get the color of the piece
        piece_color = self.board.color_at(position_index)

        # get all the legal moves for the piece
        legal_moves = self.board.generate_legal_moves(from_mask=chess.BB_SQUARES[position_index])

        # initialize the list of legal moves
        legal_moves_san = []

        # iterate through all the legal moves
        for move in legal_moves:
            # if the move is valid, add it to the list of legal moves
            if self.board.color_at(move.to_square) != piece_color:
                legal_moves_san.append(self.board.san(move))

        # return the list of legal moves
        return legal_moves_san

    def squares_by(self, position):
        """
        List all legal moves for the piece on the specified square index

        :param position: position in SAN notation
        :return: list of legal squares for the piece on the specified position
        """

        # convert the position to square index
        position_index = self.index_from_san(position)

        # get the piece at the specified index
        piece = self.board.piece_at(position_index)

        if piece is None:
            return []

        # get the color of the piece
        piece_color = self.board.color_at(position_index)

        # get all the legal moves for the piece
        legal_moves = self.board.generate_legal_moves(from_mask=chess.BB_SQUARES[position_index])

        # initialize the list of legal moves
        legal_squares = []

        # iterate through all the legal moves
        for move in legal_moves:
            # if the move is valid, add it to the list of legal moves
            if self.board.color_at(move.to_square) != piece_color:
                legal_squares.append((chess.square_name(move.from_square), chess.square_name(move.to_square)))

        # return the list of legal moves
        return legal_squares

    def captures_san(self):
        """
        List all captures for the current board

        :return: list of captures for the current board in SAN notation
        """

        return [self.board.san(move) for move in self.board.generate_legal_captures()]

    def captures(self):
        """
        List all captures for the current board

        :return: list of captures for the current board in SAN notation
        """

        return [(chess.square_name(move.from_square), chess.square_name(move.to_square)) for move in
                self.board.generate_legal_captures()]

    def captures_by(self, position):
        """
        List all pieces attacked by the piece on the specified position

        :param position: position in SAN notation
        :return: List of square names
        """

        # convert the position to square index
        position_index = self.index_from_san(position)

        return self.captures_by_index_position(position_index)

    def captures_by_index_position(self, position_index):
        # get the color of the piece
        piece_color = self.board.color_at(position_index)

        # get all the squares attacked by the piece
        attacked_squares = self.board.attacks(position_index)

        # initialize the list of captures
        captures = []

        # iterate through all the attacked squares
        for square in attacked_squares:
            # if the square is occupied by an opponent's piece, add the move to the list of captures
            if self.board.piece_at(square) and self.board.color_at(square) != piece_color:
                captures.append(chess.square_name(square))

        # return the list of captures
        return captures

    def captures_by_san(self, position):
        """
        List all pieces attacked by the piece on the specified position

        :param position: position in SAN notation
        :return: List of SAN moves
        """

        # convert the position to square index
        position_index = self.index_from_san(position)

        # get the color of the piece
        piece_color = self.board.color_at(position_index)

        # get all the squares attacked by the piece
        attacked_squares = self.board.attacks(position_index)

        # initialize the list of captures
        captures = []

        # iterate through all the attacked squares
        for square in attacked_squares:
            # if the square is occupied by an opponent's piece, add the move to the list of captures
            if self.board.piece_at(square) and self.board.color_at(square) != piece_color:
                captures.append(self.board.san(chess.Move(position_index, square)))

        # return the list of captures
        return captures

    def capture_pieces(self):
        """
        List all pieces that could be captured for the current board

        :return: tuple of (piece, start_square, end_square) for all captures for the current board
        """

        return [
            (
                str(self.board.piece_at(move.to_square)).upper(),
                chess.square_name(move.from_square),
                chess.square_name(move.to_square)
            )
            for move in self.board.generate_legal_captures()
        ]

    def capture_pieces_san(self):
        """
        List all pieces that could be captured for the current board

        :return: tuple of (piece, start_square, end_square) for all captures for the current board
        """

        return [
            (
                str(self.board.piece_at(move.to_square)).upper(),
                self.board.san(move)
            )
            for move in self.board.generate_legal_captures()
        ]

    def capture_pieces_by(self, position):
        """
        List all pieces that could be captured by the piece on the specified position

        :param position: position in SAN notation
        :return: List of tuples (piece, start_square, end_square)
        """

        # convert the position to square index
        position_index = self.index_from_san(position)

        # get the color of the piece
        piece_color = self.board.color_at(position_index)

        # get all the squares attacked by the piece
        attacked_squares = self.board.attacks(position_index)

        # initialize the list of captures
        captures = []

        # iterate through all the attacked squares
        for square in attacked_squares:

            piece_at = self.board.piece_at(square)
            if piece_at is None:
                continue

            # if the square is occupied by an opponent's piece, add the move to the list of captures
            if self.board.color_at(square) != piece_color:
                captures.append((
                    str(piece_at).upper(),
                    chess.square_name(position_index),
                    chess.square_name(square)
                ))

        # return the list of captures
        return captures

    def capture_pieces_by_san(self, position):
        """
        List all pieces that could be captured by the piece on the specified position

        :param position: position in SAN notation
        :return: List of tuples (piece, start_square, end_square)
        """

        # convert the position to square index
        position_index = self.index_from_san(position)

        # get the color of the piece
        piece_color = self.board.color_at(position_index)

        # get all the squares attacked by the piece
        attacked_squares = self.board.attacks(position_index)

        # initialize the list of captures
        captures = []

        # iterate through all the attacked squares
        for square in attacked_squares:

            piece_at = self.board.piece_at(square)
            if piece_at is None:
                continue

            # if the square is occupied by an opponent's piece, add the move to the list of captures
            if self.board.color_at(square) != piece_color:
                captures.append((
                    str(piece_at).upper(),
                    self.board.san(chess.Move(position_index, square))
                ))

        # return the list of captures
        return captures

    def captures_except_square_allowing_duplicates(self, square):
        """
            List squares of pieces that are under attack by the current player, allowing duplicates, except those
            which are attacked by square

            :param square: The square to avoid counting attacked pieces by.
            :return: List of squares as strings
        """
        attacked_squares = []
        for current_square in chess.SQUARES:
            if current_square == square:
                continue
            if self.board.piece_at(current_square) and self.board.color_at(current_square) == self.board.turn:
                attacked_squares += self.captures_by_index_position(current_square)
        return attacked_squares

    def best_move(self, time_limit=2.0):
        """
        Get the best move for the current board

        :param time_limit: time limit for the engine to find the best move. Default is 2 seconds
        :return: best move for the current board
        """

        with chess.engine.SimpleEngine.popen_uci(self.engine_path) as engine:

            # check if the game is over
            if self.board.is_game_over():
                return None

            # get the best move for the current board
            result = engine.play(self.board, chess.engine.Limit(time=time_limit))

            # convert the move to SAN notation and return it
            return self.board.san(result.move)

    def best_move_sequence(self, num_moves, time_limit=2.0):
        """
        Get the best sequence of moves for the current board

        :param num_moves: Number of moves to be returned
        :param time_limit: time limit for the engine to find the best move. Default is 2 seconds
        :return: best sequence of moves for the current board
        """

        # initialize the sequence of moves
        sequence = []

        # make a copy of the board, so we don't modify the original board
        temp_board = self.board.copy()

        if self.board.outcome():
            return sequence

        with chess.engine.SimpleEngine.popen_uci(self.engine_path) as engine:
            for _ in range(num_moves):
                # get the best move for the current board
                result = engine.play(temp_board, chess.engine.Limit(time=time_limit))

                # check if the game is over
                if temp_board.is_game_over():
                    break

                # convert the move to SAN notation
                move = temp_board.san(result.move)

                # add the move to the sequence
                sequence.append(move)

                # make the move on the board
                temp_board.push(result.move)

        # return the sequence of moves
        return sequence

    def evaluation(self):
        """
        Evaluate the current board

        :return: evaluation of the current board
        """
        with chess.engine.SimpleEngine.popen_uci(self.engine_path) as engine:
            info = engine.analyse(self.board, chess.engine.Limit(time=0.1))
            return info["score"]

    def first_item_evaluation(self):
        """
           Evaluate the current board

           :return: first item of evaluation
        """
        eval_result = str(self.evaluation())
        eval_result = eval_result[eval_result.find('('):]
        eval_result = eval_result.strip('()')
        eval_result = eval_result[:eval_result.find(',')]

        return eval_result

    def get_color_eval_score(self, eval_first_item):
        """
            Evaluate the current board

           :return: color of player in advantage
        """
        eval_first_item = eval_first_item[eval_first_item.find('('):]
        eval_first_item = eval_first_item.strip('()')
        if eval_first_item[0] == '+':
            return self.board.turn
        else:
            return not self.board.turn

    def piece_at_index(self, index):
        """
        Get the piece at the specified index

        :param index: index of the piece.
        :return: piece at the specified index
        """

        return self.board.piece_at(index)

    def piece_at_index_str(self, index):
        return str(self.piece_at_index(index)).upper()

    def piece_at_san(self, position):
        """
        Get the piece at the specified position

        :param position: position in SAN notation
        :return: piece at the specified position
        """

        return self.board.piece_at(chess.parse_square(position))

    def position_from_move(self, move):
        """
        Get the position from the specified move

        :param move: move string in SAN notation
        :return: position from the specified move
        """

        return self.board.piece_at(chess.parse_square(move))

    @staticmethod
    def index_from_san(position):
        """
        Get the index from the specified position

        :param position: position in SAN notation
        :return: index from the specified position
        """

        return chess.parse_square(position)

    def is_capture(self, move):
        """
        Check if the specified move is a capture

        :param move: move in SAN notation
        :return: True if the move is a capture, False otherwise
        """

        # convert the move to UCI notation and check if it is a capture
        return self.board.is_capture(chess.Move.from_uci(str(self.board.parse_san(move))))

    def is_en_passant(self, move):
        """
        Check if the specified move is an en passant

        :param move: move in SAN notation
        :return: True if the move is an en passant, False otherwise
        """

        # convert the move to UCI notation and check if it is an en passant
        return self.board.is_en_passant(chess.Move.from_uci(str(self.board.parse_san(move))))

    def is_check(self):
        """
        Check if the current board is in check

        :return: True if the board is in check, False otherwise
        """

        return self.board.is_check()

    def get_attackers_at(self, color, poz):

        attackers = self.board.attackers(color, poz)
        return attackers

    def remove_piece_at(self, poz):
        self.board.remove_piece_at(poz)

    def add_piece_at(self, piece, poz):
        self.board.set_piece_at(poz, piece)

    def make_reverse_san_move(self, move):
        """
        Make the reverse of the specified move

        :param move: move in SAN notation to be reversed
        :return: True if reversed move is valid, False otherwise
        """

        pass

    def get_number_of_pieces(self):
        pieces = 0
        for square in chess.SQUARES:
            if self.board.piece_at(square):
                pieces += 1

        return pieces

    def winning_probability(self, score_cp):
        """
            Compute the winning probability based on the chess engine's score

            :param score_cp: The engine's score in centipawns
            :return: Probability of winning.
        """
        coefficient = 0.1
        score_cp /= 100
        if self.get_number_of_pieces() <= 7 and score_cp == 0.00:
            probability = 0
        else:
            probability = 1 / (1 + math.exp(-coefficient * score_cp))

        if (1 - probability) < 0.0001:
            probability = 1

        if probability < 0.0001:
            probability = 0

        return probability

    def get_occupied_squares(self):
        for square in chess.SQUARES:
            if self.board.piece_at(square):
                yield (self.board.piece_at(square),
                       chess.square_rank(square),
                       chess.square_file(square))

    def get_fen(self):
        return self.board.fen()