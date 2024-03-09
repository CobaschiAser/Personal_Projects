class OpeningsDetector:
    def __init__(self, stockfish):
        self.stockfish = stockfish

    def get_opening(self, move_san):
        opening = None

        if self._is_sicilian_defense(move_san):
            opening = "Sicilian Defense"
        elif self._is_french_defense(move_san):
            opening = "French Defense"
        elif self._is_ruy_lopez_opening(move_san):
            opening = "Ruy Lopez Opening"
        elif self._is_caro_kann_defense(move_san):
            opening = "Caro-Kann Defense"
        elif self._is_italian_game(move_san):
            opening = "Italian Game"
        elif self._is_scandinavian_defense(move_san):
            opening = "Scandinavian Defense"
        elif self._is_pirc_defense(move_san):
            opening = "Pirc Defense"
        elif self._is_alekhine_defense(move_san):
            opening = "Alekhine Defense"
        elif self._is_kings_gambit(move_san):
            opening = "King's Gambit"
        elif self._is_scotch_game(move_san):
            opening = "Scotch Game"
        elif self._is_vienna_game(move_san):
            opening = "Vienna Game"
        elif self._is_queens_gambit(move_san):
            opening = "Queen's Gambit"
        elif self._is_slav_defense(move_san):
            opening = "Slav Defense"
        elif self._is_king_indian_defense(move_san):
            opening = "King's Indian Defense"
        elif self._is_nimzo_indian_defense(move_san):
            opening = "Nimzo-Indian Defense"
        elif self._is_queens_indian_defense(move_san):
            opening = "Queen's Indian Defense"
        elif self._is_catalan_opening(move_san):
            opening = "Catalan Opening"
        elif self._is_bogo_indian_defense(move_san):
            opening = "Bogo-Indian Defense"
        elif self._is_grunfeld_defense(move_san):
            opening = "Grunfeld Defense"
        elif self._is_dutch_defense(move_san):
            opening = "Dutch Defense"
        elif self._is_trompowsky_attack(move_san):
            opening = "Trompowsky Attack"
        elif self._is_benko_gambit(move_san):
            opening = "Benko Gambit"
        elif self._is_london_system(move_san):
            opening = "London System"
        elif self._is_benoni_defense(move_san):
            opening = "Benoni Defense"
        elif self._is_reti_opening(move_san):
            opening = "Reti Opening"
        elif self._is_english_opening(move_san):
            opening = "English Opening"
        elif self._is_birds_opening(move_san):
            opening = "Bird's Opening"
        elif self._is_kings_indian_attack(move_san):
            opening = "King's Indian Attack"
        elif self._is_kings_fianchetto_opening(move_san):
            opening = "King's Fianchetto Opening"
        elif self._is_nimzowitsch_larsen_attack(move_san):
            opening = "Nimzowitsch-Larsen Attack"
        elif self._is_polish_opening(move_san):
            opening = "Polish Opening"
        elif self._is_grob_opening(move_san):
            opening = "Grob Opening"

        return opening

    def _is_sicilian_defense(self, move_san):
        self.stockfish.move(move_san)
        if self.stockfish.board.fen().startswith("rnbqkbnr/pp1ppppp/8/2p5/4P3/8/PPPP1PPP/RNBQKBNR"):
            self.stockfish.undo()
            return True
        self.stockfish.undo()
        return False

    def _is_french_defense(self, move_san):
        self.stockfish.move(move_san)
        if self.stockfish.board.fen().startswith("rnbqkbnr/pppp1ppp/4p3/8/4P3/8/PPPP1PPP/RNBQKBNR"):
            self.stockfish.undo()
            return True
        self.stockfish.undo()
        return False

    def _is_ruy_lopez_opening(self, move_san):
        self.stockfish.move(move_san)
        if self.stockfish.board.fen().startswith("r1bqkbnr/pppp1ppp/2n5/1B2p3/4P3/5N2/PPPP1PPP/RNBQK2R"):
            self.stockfish.undo()
            return True
        self.stockfish.undo()
        return False

    def _is_caro_kann_defense(self, move_san):
        self.stockfish.move(move_san)
        if self.stockfish.board.fen().startswith("rnbqkbnr/pp1ppppp/2p5/8/4P3/8/PPPP1PPP/RNBQKBNR"):
            self.stockfish.undo()
            return True
        self.stockfish.undo()
        return False

    def _is_italian_game(self, move_san):
        self.stockfish.move(move_san)
        if self.stockfish.board.fen().startswith("r1bqkbnr/pppp1ppp/2n5/4p3/2B1P3/5N2/PPPP1PPP/RNBQK2R"):
            self.stockfish.undo()
            return True
        self.stockfish.undo()
        return False

    def _is_scandinavian_defense(self, move_san):
        self.stockfish.move(move_san)
        if self.stockfish.board.fen().startswith("rnbqkbnr/ppp1pppp/8/3p4/4P3/8/PPPP1PPP/RNBQKBNR"):
            self.stockfish.undo()
            return True
        self.stockfish.undo()
        return False

    def _is_pirc_defense(self, move_san):
        self.stockfish.move(move_san)
        if self.stockfish.board.fen().startswith("rnbqkb1r/ppp1pppp/3p1n2/8/3PP3/8/PPP2PPP/RNBQKBNR"):
            self.stockfish.undo()
            return True
        self.stockfish.undo()
        return False

    def _is_alekhine_defense(self, move_san):
        self.stockfish.move(move_san)
        if self.stockfish.board.fen().startswith("rnbqkb1r/pppppppp/5n2/8/4P3/8/PPPP1PPP/RNBQKBNR"):
            self.stockfish.undo()
            return True
        self.stockfish.undo()
        return False

    def _is_kings_gambit(self, move_san):
        self.stockfish.move(move_san)
        if self.stockfish.board.fen().startswith("rnbqkbnr/pppp1ppp/8/4p3/4PP2/8/PPPP2PP/RNBQKBNR"):
            self.stockfish.undo()
            return True
        self.stockfish.undo()
        return False

    def _is_scotch_game(self, move_san):
        self.stockfish.move(move_san)
        if self.stockfish.board.fen().startswith("r1bqkbnr/pppp1ppp/2n5/4p3/3PP3/5N2/PPP2PPP/RNBQKB1R"):
            self.stockfish.undo()
            return True
        self.stockfish.undo()
        return False

    def _is_vienna_game(self, move_san):
        self.stockfish.move(move_san)
        if self.stockfish.board.fen().startswith("rnbqkbnr/pppp1ppp/8/4p3/4P3/2N5/PPPP1PPP/R1BQKBNR"):
            self.stockfish.undo()
            return True
        self.stockfish.undo()
        return False

    def _is_queens_gambit(self, move_san):
        self.stockfish.move(move_san)
        if self.stockfish.board.fen().startswith("rnbqkbnr/ppp1pppp/8/3p4/2PP4/8/PP2PPPP/RNBQKBNR"):
            self.stockfish.undo()
            return True
        self.stockfish.undo()
        return False

    def _is_slav_defense(self, move_san):
        self.stockfish.move(move_san)
        if self.stockfish.board.fen().startswith("rnbqkbnr/pp2pppp/2p5/3p4/2PP4/8/PP2PPPP/RNBQKBNR"):
            self.stockfish.undo()
            return True
        self.stockfish.undo()
        return False

    def _is_king_indian_defense(self, move_san):
        self.stockfish.move(move_san)
        if self.stockfish.board.fen().startswith("rnbqkb1r/pppppp1p/5np1/8/2PP4/8/PP2PPPP/RNBQKBNR"):
            self.stockfish.undo()
            return True
        self.stockfish.undo()
        return False

    def _is_nimzo_indian_defense(self, move_san):
        self.stockfish.move(move_san)
        if self.stockfish.board.fen().startswith("rnbqk2r/pppp1ppp/4pn2/8/1bPP4/2N5/PP2PPPP/R1BQKBNR"):
            self.stockfish.undo()
            return True
        self.stockfish.undo()
        return False

    def _is_queens_indian_defense(self, move_san):
        self.stockfish.move(move_san)
        if self.stockfish.board.fen().startswith("rnbqkb1r/p1pp1ppp/1p2pn2/8/2PP4/5N2/PP2PPPP/RNBQKB1R"):
            self.stockfish.undo()
            return True
        self.stockfish.undo()
        return False

    def _is_catalan_opening(self, move_san):
        self.stockfish.move(move_san)
        if self.stockfish.board.fen().startswith("rnbqkb1r/pppp1ppp/4pn2/8/2PP4/6P1/PP2PP1P/RNBQKBNR"):
            self.stockfish.undo()
            return True
        self.stockfish.undo()
        return False

    def _is_bogo_indian_defense(self, move_san):
        self.stockfish.move(move_san)
        if self.stockfish.board.fen().startswith("rnbqk2r/pppp1ppp/4pn2/8/1bPP4/5N2/PP2PPPP/RNBQKB1R"):
            self.stockfish.undo()
            return True
        self.stockfish.undo()
        return False

    def _is_grunfeld_defense(self, move_san):
        self.stockfish.move(move_san)
        if self.stockfish.board.fen().startswith("rnbqkb1r/ppp1pp1p/5np1/3p4/2PP4/2N5/PP2PPPP/R1BQKBNR"):
            self.stockfish.undo()
            return True
        self.stockfish.undo()
        return False

    def _is_dutch_defense(self, move_san):
        self.stockfish.move(move_san)
        if self.stockfish.board.fen().startswith("rnbqkbnr/ppppp1pp/8/5p2/3P4/8/PPP1PPPP/RNBQKBNR"):
            self.stockfish.undo()
            return True
        self.stockfish.undo()
        return False

    def _is_trompowsky_attack(self, move_san):
        self.stockfish.move(move_san)
        if self.stockfish.board.fen().startswith("rnbqkb1r/pppppppp/5n2/6B1/3P4/8/PPP1PPPP/RN1QKBNR"):
            self.stockfish.undo()
            return True
        self.stockfish.undo()
        return False

    def _is_benko_gambit(self, move_san):
        self.stockfish.move(move_san)
        if self.stockfish.board.fen().startswith("rnbqkb1r/p2ppppp/5n2/1ppP4/2P5/8/PP2PPPP/RNBQKBNR"):
            self.stockfish.undo()
            return True
        self.stockfish.undo()
        return False

    def _is_london_system(self, move_san):
        self.stockfish.move(move_san)
        if self.stockfish.board.fen().startswith("rnbqkb1r/ppp1pppp/5n2/3p4/3P1B2/5N2/PPP1PPPP/RN1QKB1R"):
            self.stockfish.undo()
            return True
        self.stockfish.undo()
        return False

    def _is_benoni_defense(self, move_san):
        self.stockfish.move(move_san)
        if self.stockfish.board.fen().startswith("rnbqkb1r/pp3ppp/3p1n2/2pP4/8/2N5/PP2PPPP/R1BQKBNR"):
            self.stockfish.undo()
            return True
        self.stockfish.undo()
        return False

    def _is_reti_opening(self, move_san):
        self.stockfish.move(move_san)
        if self.stockfish.board.fen().startswith("rnbqkbnr/pppppppp/8/8/8/5N2/PPPPPPPP/RNBQKB1R"):
            self.stockfish.undo()
            return True
        self.stockfish.undo()
        return False

    def _is_english_opening(self, move_san):
        self.stockfish.move(move_san)
        if self.stockfish.board.fen().startswith("rnbqkbnr/pppppppp/8/8/2P5/8/PP1PPPPP/RNBQKBNR"):
            self.stockfish.undo()
            return True
        self.stockfish.undo()
        return False

    def _is_birds_opening(self, move_san):
        self.stockfish.move(move_san)
        if self.stockfish.board.fen().startswith("rnbqkbnr/pppppppp/8/8/5P2/8/PPPPP1PP/RNBQKBNR"):
            self.stockfish.undo()
            return True
        self.stockfish.undo()
        return False

    def _is_kings_indian_attack(self, move_san):
        self.stockfish.move(move_san)
        if self.stockfish.board.fen().startswith("rnbqkbnr/ppp1pppp/8/3p4/8/5NP1/PPPPPP1P/RNBQKB1R"):
            self.stockfish.undo()
            return True
        self.stockfish.undo()
        return False

    def _is_kings_fianchetto_opening(self, move_san):
        self.stockfish.move(move_san)
        if self.stockfish.board.fen().startswith("rnbqkbnr/pppppppp/8/8/8/6P1/PPPPPP1P/RNBQKBNR"):
            self.stockfish.undo()
            return True
        self.stockfish.undo()
        return False

    def _is_nimzowitsch_larsen_attack(self, move_san):
        self.stockfish.move(move_san)
        if self.stockfish.board.fen().startswith("rnbqkbnr/pppppppp/8/8/8/1P6/P1PPPPPP/RNBQKBNR"):
            self.stockfish.undo()
            return True
        self.stockfish.undo()
        return False

    def _is_polish_opening(self, move_san):
        self.stockfish.move(move_san)
        if self.stockfish.board.fen().startswith("rnbqkbnr/pppppppp/8/8/1P6/8/P1PPPPPP/RNBQKBNR"):
            self.stockfish.undo()
            return True
        self.stockfish.undo()
        return False

    def _is_grob_opening(self, move_san):
        self.stockfish.move(move_san)
        if self.stockfish.board.fen().startswith("rnbqkbnr/pppppppp/8/8/6P1/8/PPPPPP1P/RNBQKBNR"):
            self.stockfish.undo()
            return True
        self.stockfish.undo()
        return False
