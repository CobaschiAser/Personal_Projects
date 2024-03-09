from back.utils.board_utils import BoardUtils
import chess


class TechniquesDetector:
    def __init__(self, stockfish):
        self.stockfish = stockfish

        self.piece_value = {
            'K': 10,
            'Q': 9,
            'R': 5,
            'B': 3,
            'N': 3,
            'P': 1,
        }

    def get_techniques(self, move_san):
        dictionary = {'check': self._is_check(move_san), 'checkmate': self._is_checkmate(move_san),
                      'capture': self._is_capture(move_san), 'en_passant': self._is_en_passant(move_san),
                      'fork': self._is_fork(move_san), 'battery': self._is_battery(move_san),
                      'sacrifice': self._is_sacrifice(move_san), 'stalemate': self._is_stalemate(move_san),
                      'insufficient_material': self._is_insufficient_material(move_san),
                      'discovered_attack': self._is_a_discovered_attack(move_san),
                      'castling': self._is_a_castling(move_san), 'pawn_promotion': self._is_pawn_promotion(move_san),
                      'skewer': self._is_skewer(move_san), 'forced_checkmate': self._is_forced_checkmate(move_san),
                      'pin': self._is_pin(move_san), 'check_forced': self._is_move_check_forced(move_san)}

        return dictionary

    def _is_capture(self, move_san):
        """
        Determine if the move results in a capture.

        :param move_san: Move in standard algebraic notation
        :return: Dictionary with key 'enable' that is True if the move results in a capture, False otherwise
        """
        start_end_move = self.stockfish.start_end_from_san(move_san)
        captured_piece = self.stockfish.piece_at_san(start_end_move[1])

        # If the move is an en passant, the captured piece is a pawn
        if captured_piece is None:
            captured_piece = "Pawn"

        enable = self.stockfish.is_capture(move_san)

        return dict({"enable": enable, "captured": captured_piece})

    def _is_en_passant(self, move_san):
        """
        Determine if the move results in an en passant

        :param move_san: Move in standard algebraic notation
        :return: Dictionary with key 'enable' that is True if the move results in an en passant, False otherwise
        """
        return {'enable': self.stockfish.is_en_passant(move_san)}

    def _is_fork(self, move_san):
        """
        Determine if the move results in a fork

        :param move_san: Move in standard algebraic notation
        :return: True if the move results in a fork, False otherwise
        """

        dictionary = {"enable": False, "forked": []}

        # get (start, end) square of the move
        start_end_move = self.stockfish.start_end_from_san(move_san)

        # check that piece is not a pawn
        if self.stockfish.piece_at_san(start_end_move[0]) == 'P':
            return dict({"enable": False})

        # initialize the valuable pieces count
        valuable_pieces_count = 0

        # make the move
        self.stockfish.move(move_san)

        # get all captures by the moved piece
        captures = self.stockfish.capture_pieces_by_san(start_end_move[1])

        # loop through all captures
        for capture in captures:
            # get captured piece
            captured_piece = capture[0]

            if captured_piece in ['K', 'Q', 'R', 'B', 'N']:
                valuable_pieces_count += 1
                dictionary['forked'].append(BoardUtils.expand_piece_name(captured_piece))

        # undo the move
        self.stockfish.undo()

        if valuable_pieces_count > 1:
            dictionary['enable'] = True

        return dictionary

    def _is_checkmate(self, move_san):
        """
        Determine if the move results in a checkmate

        :param move_san: Move in standard algebraic notation
        :return: dictionary with key 'enable' that is True if the move results in a checkmate, False otherwise
                and key 'piece' that is the piece that delivers checkmate
        """

        dictionary = {}

        self.stockfish.move(move_san)
        is_checkmate = self.stockfish.board.is_checkmate()
        self.stockfish.undo()

        # get piece that delivers checkmate
        if is_checkmate:
            start_end_move = self.stockfish.start_end_from_san(move_san)
            index = self.stockfish.index_from_san(start_end_move[0])
            piece = BoardUtils.piece_at_index_str(self.stockfish.board, index)
            piece = BoardUtils.expand_piece_name(piece)
            dictionary['piece'] = piece
        dictionary['enable'] = is_checkmate
        return dictionary

    def _is_battery(self, move_san):
        """
        Determine if the move results in a battery.

        :param move_san: Move in standard algebraic notation
        :return: True if the move results in a battery, False otherwise
        """
        # Get the index of the moved piece
        move_index = chess.parse_square(self.stockfish.start_end_from_san(move_san)[1])

        self.stockfish.move(move_san)

        # Get the moved piece
        move_piece = self.stockfish.board.piece_at(move_index)

        # Get the pieces that are attacking the moved piece (the same color as the moved piece)
        self.stockfish.switch_turn()
        attackers = BoardUtils.get_attackers_at_square(self.stockfish.board, move_index)
        self.stockfish.switch_turn()

        is_battery = False

        attacker_piece = None

        # Check if there is a battery
        for attacker in attackers:
            # Get the piece that is attacking the moved piece
            attacker_piece = self.stockfish.board.piece_at(attacker)

            # Check if the attacker piece attacks on the same direction as the moved piece
            if BoardUtils.is_battery_compatible(move_piece, attacker_piece):
                is_battery = True
                move_piece = BoardUtils.expand_piece_name(str(move_piece))
                attacker_piece = BoardUtils.expand_piece_name(str(attacker_piece))
                break

        # Undo the move
        self.stockfish.undo()

        if is_battery:
            return dict({"enable": is_battery, "moved": move_piece, "attacker": attacker_piece})
        return dict({"enable": is_battery})

    def _is_sacrifice(self, move_san):

        enable = False
        capture = False
        start_end_move = self.stockfish.start_end_from_san(move_san)

        # type of the piece that was captured
        index = self.stockfish.index_from_san(start_end_move[1])
        old_piece = self.stockfish.board.piece_at(index)

        self.stockfish.move(move_san)
        # type of the piece that was moved
        new_piece = BoardUtils.piece_at_index_str(self.stockfish.board, index)
        # all the squares (as integers) that attack the moved piece
        attackers = BoardUtils.get_attackers_at_index(self.stockfish.board, self.stockfish.board.turn, index)
        # all the squares that protect the moved piece
        protectors = BoardUtils.get_attackers_at_index(self.stockfish.board, not self.stockfish.board.turn, index)

        # undo the move
        self.stockfish.undo()

        # the piece was moved to a square that is under attack and there are no protectors
        if old_piece is None:
            if len(attackers) > 0 and len(protectors) == 0:
                enable = True

            else:
                # the piece is protected but is attacked and can be taken by a weaker piece
                for attacker in attackers:
                    piece = BoardUtils.piece_at_index_str(self.stockfish.board, attacker)
                    if self.piece_value[piece] < self.piece_value[new_piece]:
                        enable = True
                if enable:
                    new_piece = BoardUtils.expand_piece_name(new_piece)
                    return dict({"enable": enable, "capture": capture, "sacrificed": new_piece})
                else:
                    return dict({"enable": enable})

        capture = True
        old_piece = str(old_piece).upper()

        # the piece was traded for a lower value piece
        if self.piece_value[old_piece] < self.piece_value[new_piece]:
            enable = True

        if enable:
            old_piece = BoardUtils.expand_piece_name(old_piece)
            new_piece = BoardUtils.expand_piece_name(new_piece)
            return dict({"enable": enable, "capture": capture, "captured": old_piece, "sacrificed": new_piece})

        return dict({"enable": enable})

    def _is_stalemate(self, move_san):
        """
        Determine if the move results in a stalemate.

        :param move_san: Move in standard algebraic notation
        :return: Dictionary with key 'enable' that is True if the move results in a stalemate, False otherwise
        """

        self.stockfish.move(move_san)
        dictionary = {"enable": self.stockfish.board.is_stalemate()}
        self.stockfish.undo()
        return dictionary

    def _is_insufficient_material(self, move_san):
        """
        Determine if the move results in a stalemate.

        :param move_san: Move in standard algebraic notation
        :return: Dictionary with key 'enable' that is True if the move results in a stalemate, False otherwise
        """
        self.stockfish.move(move_san)
        dictionary = {"enable": self.stockfish.board.is_insufficient_material()}
        self.stockfish.undo()
        return dictionary

    def _is_a_discovered_attack(self, move_san):
        """
            Determine if the move results in a discovered attack.

            :param move_san: Move in standard algebraic notation
            :return: True if the move results in a discovered attack, False otherwise
        """

        dictionary = {}
        from_square = self.stockfish.board.parse_san(move_san).from_square
        to_square = self.stockfish.board.parse_san(move_san).to_square

        moved_piece_type = BoardUtils.piece_at_index_str(self.stockfish.board, from_square)
        moved_piece = BoardUtils.expand_piece_name(moved_piece_type)

        squares_before_move = self.stockfish.captures_except_square_allowing_duplicates(from_square)

        self.stockfish.move(move_san)
        self.stockfish.board.turn = not self.stockfish.board.turn

        squares_after_move = self.stockfish.captures_except_square_allowing_duplicates(to_square)

        self.stockfish.undo()

        for attacked_square in squares_after_move:
            if squares_after_move.count(attacked_square) > squares_before_move.count(attacked_square):
                dictionary['enable'] = True
                attacked_piece_type = self.stockfish.piece_at_san(attacked_square)
                print(attacked_piece_type)
                attacked_piece = BoardUtils.expand_piece_name(str(attacked_piece_type))
                dictionary['piece'] = [moved_piece, attacked_piece]
                return dictionary

        dictionary['enable'] = False
        return dictionary

    def _is_a_castling(self, move_san):
        enable = self.stockfish.board.is_castling(self.stockfish.board.parse_san(move_san))
        from_square = self.stockfish.board.parse_san(move_san).from_square
        to_square = self.stockfish.board.parse_san(move_san).to_square
        if chess.square_rank(from_square) < chess.square_rank(to_square):
            side = "QueenSide"
        else:
            side = "KingSide"

        return dict({"enable": enable, "side": side})

    def _is_pawn_promotion(self, move_san):
        enable = False
        piece_type = ""
        start_end_move = self.stockfish.start_end_from_san(move_san)
        start_index = self.stockfish.index_from_san(start_end_move[0])
        end_index = self.stockfish.index_from_san(start_end_move[1])
        start_piece = BoardUtils.piece_at_index_str(self.stockfish.board, start_index)
        if start_piece == 'P':
            self.stockfish.move(move_san)
            end_piece = BoardUtils.piece_at_index_str(self.stockfish.board, end_index)
            if end_piece != 'P':
                piece_type = end_piece
                self.stockfish.undo()
                enable = True
            self.stockfish.undo()

        if enable:
            piece = BoardUtils.expand_piece_name(piece_type)
            return dict({"enable": enable, "piece": piece})
        else:
            return dict({"enable": enable})

    def _is_skewer(self, move_san):

        enable = False
        start_end_move = self.stockfish.start_end_from_san(move_san)

        # index of best move
        index = self.stockfish.index_from_san(start_end_move[1])

        self.stockfish.move(move_san)

        # all the squares attacked be the moved piece
        previously_attacked_pieces = self.stockfish.board.attacks(index)

        # a skewer requires two extra moves for completion
        best_moves = self.stockfish.best_move_sequence(2)

        if len(best_moves) < 2:
            self.stockfish.undo()
            return dict({"enable": enable})

        # indexes for the starting and ending position of the first move in the sequence
        start_first_move, end_first_move = self.stockfish.start_end_from_san(best_moves[0])
        start_first_move = self.stockfish.index_from_san(start_first_move)
        end_first_move = self.stockfish.index_from_san(end_first_move)

        # type of the attacked and attacking piece to be compared
        attacked_piece = BoardUtils.piece_at_index_str(self.stockfish.board, start_first_move)
        attacking_piece = BoardUtils.piece_at_index_str(self.stockfish.board, index)

        # get all the attacked squares after the opponent played an optimal move
        self.stockfish.move(best_moves[0])
        attacked_pieces = self.stockfish.board.attacks(index)

        # indexes for the second move in the sequence
        start_second_move, end_second_move = self.stockfish.start_end_from_san(best_moves[1])
        start_second_move = self.stockfish.index_from_san(start_second_move)
        end_second_move = self.stockfish.index_from_san(end_second_move)

        captured_piece = BoardUtils.piece_at_index_str(self.stockfish.board, end_second_move)

        # undo the moves
        self.stockfish.undo()
        self.stockfish.undo()

        # a skewer requires to attack a higher value piece
        if self.piece_value[attacking_piece] >= self.piece_value[attacked_piece]:
            return dict({"enable": enable})

        # the opponent move must move an attacked piece to be a skewer
        if start_first_move not in previously_attacked_pieces:
            return dict({"enable": enable})

        # the opponent must take the higher piece to safety
        if end_first_move in attacked_pieces:
            return dict({"enable": enable})

        # the attacking piece must capture a piece in the next move that was defended previously
        if start_second_move == index and end_second_move not in previously_attacked_pieces and "x" in best_moves[1]:
            enable = True
            attacking_piece = BoardUtils.expand_piece_name(attacking_piece)
            attacked_piece = BoardUtils.expand_piece_name(attacked_piece)
            captured_piece = BoardUtils.expand_piece_name(captured_piece)
            return dict(
                {"enable": enable, "attacker": attacking_piece, "captured": captured_piece, "attacked": attacked_piece})

        return dict({"enable": enable})

    def _is_forced_checkmate(self, move_san):

        start_end_move = self.stockfish.start_end_from_san(move_san)
        start_index = self.stockfish.index_from_san(start_end_move[0])
        start_piece = BoardUtils.piece_at_index_str(self.stockfish.board, start_index)
        piece = BoardUtils.expand_piece_name(start_piece)
        self.stockfish.move(move_san)
        eval_first_item = self.stockfish.first_item_evaluation()
        self.stockfish.undo()

        if eval_first_item[0] == 'M':
            return dict({"enable": True, "piece": piece})
        return dict({"enable": False})

    def _is_check(self, move_san):
        """
        Determine if the move results in a check.

        :param move_san: Move in standard algebraic notation
        :return: Dictionary with key 'enable' that is True if the move results in a check, False otherwise
                and key 'piece' that is the piece that delivers check
        """

        start_end_move = self.stockfish.start_end_from_san(move_san)
        index = self.stockfish.index_from_san(start_end_move[0])
        piece_type = BoardUtils.piece_at_index_str(self.stockfish.board, index)
        piece = BoardUtils.expand_piece_name(piece_type)
        self.stockfish.move(move_san)
        is_check = self.stockfish.board.is_check()
        self.stockfish.undo()
        if is_check:
            return dict({"enable": is_check, "piece": piece})
        else:
            return dict({"enable": is_check})

    def _is_move_check_forced(self, move_san):
        """
        Determine if the move is forced by a check

        :return: Dictionary with key 'enable' that is True if the move is forced by a check, False otherwise
                and key 'piece' that is the piece that makes the player not to be in check anymore
        """

        start_end_move = self.stockfish.start_end_from_san(move_san)
        is_check = self.stockfish.board.is_check()
        is_checkmate = self.stockfish.board.is_checkmate()
        piece = BoardUtils.piece_at_index_str(self.stockfish.board, self.stockfish.index_from_san(start_end_move[0]))

        if is_check and not is_checkmate:
            return dict({"enable": True, "piece": piece})
        return dict({"enable": False})

    def _is_pin(self, move_san):
        """
        Determine if the move results in a pin.

        :param move_san: Move in standard algebraic notation
        :return: True if the move results in a pin, False otherwise
        """
        # Get the square name of the moved piece
        moved_square = self.stockfish.start_end_from_san(move_san)[1]

        # Make the move
        self.stockfish.move(move_san)

        # Get the piece that is moved
        moved_piece = self.stockfish.piece_at_san(moved_square)

        # Check if the moved piece is a pawn, knight or king
        if moved_piece == 'P' or moved_piece == 'N' or moved_piece == 'K':
            # Undo the move
            self.stockfish.undo()

            # Return False if the moved piece is a pawn, knight or king
            return dict({"enable": False})

        # Get all the pieces that are attacked by the moved piece
        attacked_pieces = set(self.stockfish.captures_by(moved_square))

        # Make backup of board
        board_backup = self.stockfish.board.copy()

        for attacked_piece_square in attacked_pieces:
            # Convert the attacked piece to a chess.Piece object
            attacked_piece = self.stockfish.piece_at_san(attacked_piece_square)

            # Remove the attacked piece from the board
            self.stockfish.board.remove_piece_at(self.stockfish.index_from_san(attacked_piece_square))

            # Get all the pieces that are attacked by the moved piece after the attacked piece is removed
            attacked_pieces_after = set(self.stockfish.captures_by(moved_square))

            # Add the attacked piece back to the board
            self.stockfish.add_piece_at(chess.Piece(attacked_piece.piece_type, self.stockfish.board.turn),
                                        self.stockfish.index_from_san(attacked_piece_square))

            # Check if another piece is attacked by the moved piece after the attacked piece is removed
            if len(attacked_pieces_after) > 0:
                # Get the other attacked piece from behind the removed attacked piece
                other_attacked_pieces = attacked_pieces_after.difference(attacked_pieces)

                # Get the first other attacked piece
                if len(other_attacked_pieces) > 0:
                    other_attacked_piece = other_attacked_pieces.pop()
                else:
                    continue

                # Convert the other attacked piece to a chess.Piece object
                other_attacked_piece = self.stockfish.piece_at_san(other_attacked_piece)

                # Check if there is a pin
                if BoardUtils.is_pin_compatible(moved_piece, attacked_piece, other_attacked_piece):
                    # Restore the board
                    self.stockfish.board = board_backup

                    # Undo the move
                    self.stockfish.undo()
                    pinned = BoardUtils.expand_piece_name(str(attacked_piece))
                    defended = BoardUtils.expand_piece_name(str(other_attacked_piece))

                    # Return absolute or relative pin
                    if other_attacked_piece.piece_type == 6:
                        # Return absolute pin if the attacked piece is a king
                        return dict({"enable": True, "type": "absolute", "pinned": pinned, "defended": defended})
                    else:
                        # Return relative pin if the attacked piece is not a king
                        return dict({"enable": True, "type": "relative", "pinned": pinned, "defended": defended})

        # Restore the board
        self.stockfish.board = board_backup

        # Undo the move
        self.stockfish.undo()

        # Return False if there is no pin
        return dict({"enable": False})
