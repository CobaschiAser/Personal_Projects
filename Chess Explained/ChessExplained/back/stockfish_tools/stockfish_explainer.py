from back.detectors import OpeningsDetector
from back.detectors import TechniquesDetector
from back.stockfish_tools.explanation_builder import ExplanationBuilder
from back.OpenAI import OpenAI
from back.utils import BoardUtils


class StockfishExplainer:
    """
    Class used to provide explanations for moves suggested by Stockfish
    """

    def __init__(self, stockfish):
        """
        Constructor for StockfishExplainer class

        :param stockfish: Instance of Stockfish class
        """

        self.stockfish = stockfish
        self.openings_detector = OpeningsDetector(stockfish)
        self.techniques_detector = TechniquesDetector(stockfish)
        self.piece_value = {
            'K': 10,
            'Q': 9,
            'R': 5,
            'B': 3,
            'N': 3,
            'P': 1,
        }

    def explain(self):
        """
        Explain the next best move

        :return: Explanation as a string
        """
        if self.stockfish.board.outcome():
            return "The game is already over!"

        # Get the best move
        best_move = self.stockfish.best_move()
        explanation = f"The best move is {best_move}. "

        # Make the move
        self.stockfish.move(best_move)

        # Print the board
        print("Board after move: ")
        self.stockfish.display()

        # Undo the move
        self.stockfish.undo()

        # Get the opening and the techniques
        opening = self.openings_detector.get_opening(best_move)
        techniques = self.techniques_detector.get_techniques(best_move)

        print("is_pin: ", techniques['pin']['enable'])
        print("is_fork: ", techniques['fork']['enable'])
        print("is_checkmate: ", techniques['checkmate']['enable'])
        print("is_check: ", techniques['check']['enable'])
        print("is_check_forced: ", techniques['check_forced']['enable'])
        print("is_capture: ", techniques['capture']['enable'])
        print("is_en_passant: ", techniques['en_passant']['enable'])
        print("is_stalemate: ", techniques['stalemate']['enable'])
        print("is_insufficient_material: ", techniques['insufficient_material']['enable'])
        print("is_battery: ", techniques['battery']['enable'])
        print("is_sacrifice: ", techniques['sacrifice']['enable'])
        print("is_discovered_attack: ", techniques['discovered_attack']['enable'])
        print("is_castling: ", techniques['castling']['enable'])
        print("is_pawn_promotion: ", techniques['pawn_promotion']['enable'])
        print("is_skewer: ", techniques['skewer']['enable'])
        print("is_forced_checkmate: ", techniques['forced_checkmate']['enable'])

        #  EXPLANATIONS
        """ 
            in some cases, key 'piece' exists only if 'enable' is True and corresponds to an explicit piece
            (type of promoted pawn, the piece who delivers checkmates, etc). In other cases, key 'piece' corresponds to
            a list of pieces(discovered_attack, fork , etc): first piece is always the attacker, followings are attacked 
            pieces
            
            pawn_promotion    : dict['piece']    - piece that the pawn was promoted to
            
            discovered_attack : dict['piece'][0] - piece that was moved ; 
                                dict['piece'][0] - piece that was discovered_attacked 
            
            forced_checkmate  : dict['piece']    - piece that was moved
            
            check             : dict['piece']    - piece that generated the check
        """

        if techniques['castling']['enable']:
            explanation += f"{techniques['castling']['side']} castling happens. "
        if techniques['pawn_promotion']['enable']:
            explanation += f"Pawn promoted to {techniques['pawn_promotion']['piece']}. "

        if techniques['forced_checkmate']['enable']:
            explanation += f"{techniques['forced_checkmate']['piece']} move generated a safe way that follows to win. "

        if opening:
            explanation += f"This move is a book move from the {opening}. "

        print("---------------------------------------------------")
        advantage_color, probability = self._calculate_winning_prob()
        print("WAt")
        # check checkmate, forced checkmate
        if techniques['checkmate']['enable'] or techniques['forced_checkmate']['enable']:
            probability = 1
        elif techniques['stalemate']['enable'] or techniques['insufficient_material']['enable']:
            probability = 0

        advantage_color = "white" if advantage_color else "black"
        probability = round(probability, 2)

        print("Player that has advantage: " + str(advantage_color))
        print("Winning probability: " + str(probability * 100) + "%.")

        print("HEEEEEEERE2")
        explainer = ExplanationBuilder(techniques)
        explanation += explainer.build_explanation()

        explanation += f" The current player has a winning probability of {probability * 100}%"
        explanation += "The player that has advantage is " + advantage_color + ". "
        print("HEEEEEEERE")

        if not any(techniques.values()):
            explanation += "This move improves the position of the current player."

        print("HEEEEEEERE")
        # OpenAI
        openai = OpenAI()
        explanation = openai.reword(explanation)

        print("EXPLANATION: ", explanation)
        return self.stockfish.board, explanation

    def _calculate_winning_prob(self):
        eval_first_item = self.stockfish.first_item_evaluation()
        score_cp = BoardUtils.get_evaluation_score(eval_first_item)
        color = self.stockfish.get_color_eval_score(eval_first_item)
        probability = self.stockfish.winning_probability(score_cp)

        return color, probability
