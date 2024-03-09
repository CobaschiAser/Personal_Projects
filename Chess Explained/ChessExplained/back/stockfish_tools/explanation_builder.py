class ExplanationBuilder:
    def __init__(self, dictionary):
        self.dictionary = dictionary
        self.build_explanation()

    def build_explanation(self):
        explanation = ""
        explanation += self.en_passant_explanation(self.dictionary['en_passant'])
        explanation += self.capture_explanation(self.dictionary['capture'])
        explanation += self.checkmate_explanation(self.dictionary['checkmate'])
        explanation += self.insufficient_material_explanation(self.dictionary['insufficient_material'])
        explanation += self.stalemate_explanation(self.dictionary['stalemate'])
        explanation += self.check_explanation(self.dictionary['check'])
        explanation += self.check_forced_explanation(self.dictionary['check_forced'])
        explanation += self.battery_explanation(self.dictionary['battery'])
        explanation += self.castling_explanation(self.dictionary['castling'])
        explanation += self.sacrifice_explanation(self.dictionary['sacrifice'])
        explanation += self.pawn_promotion_explanation(self.dictionary['pawn_promotion'])
        explanation += self.discovered_attack_explanation(self.dictionary['discovered_attack'])
        explanation += self.forced_checkmate_explanation(self.dictionary['forced_checkmate'])
        explanation += self.skewer_explanation(self.dictionary['skewer'])
        explanation += self.pin_explanation(self.dictionary['pin'])
        explanation += self.fork_explanation(self.dictionary['fork'])

        return explanation

    @staticmethod
    def fork_explanation(info):
        if info['enable'] is False:
            return ""
        text = f" It forks the following pieces: "
        for piece in info['forked']:
            text += f"{piece}, "
        text = text[:-2]
        text += "."
        return text

    @staticmethod
    def forced_checkmate_explanation(info):
        if info['enable'] is False:
            return ""

        return f"The piece {info['piece']} sets up a forced checkmate."

    @staticmethod
    def checkmate_explanation(info):
        if info['enable'] is False:
            return ""

        return f"The piece {info['piece']} checkmates the opponent."

    @staticmethod
    def check_explanation(info):
        if info['enable'] is False:
            return ""

        return f"The piece {info['piece']} checks the opponent king."

    @staticmethod
    def check_forced_explanation(info):
        if info['enable'] is False:
            return ""

        return f"The {info['piece']} had to be moved to break the check."

    @staticmethod
    def en_passant_explanation(info):
        if info['enable'] is False:
            return ""

        return "En passant was played."

    @staticmethod
    def castling_explanation(info):
        if info['enable'] is False:
            return ""

        if info['side'] == "KingSide":
            return "It moves your king to safety."

        return "It moves your king to safety while putting the rook on a more active square."

    @staticmethod
    def pawn_promotion_explanation(info):
        if info['enable'] is False:
            return ""

        return f"It promotes the pawn to a {info['piece']}."

    @staticmethod
    def sacrifice_explanation(info):
        if info['enable'] is False:
            return ""

        if info['capture'] is False:
            return f"It sacrifices the {info['sacrificed']} to gain an advantage."

        return f"It sacrifices the {info['sacrificed']} for a {info['captured']} to gain an advantage."

    @staticmethod
    def stalemate_explanation(info):
        if info['enable'] is False:
            return ""

        return "The move results in a stalemate."

    @staticmethod
    def insufficient_material_explanation(info):
        if info['enable'] is False:
            return ""

        return "The move results in a draw due to insufficient material, no checkmate is possible."

    @staticmethod
    def capture_explanation(info):
        if info['enable'] is False:
            return ""

        return f"It captures the {info['captured']}."

    @staticmethod
    def skewer_explanation(info):
        if info['enable'] is False:
            return ""
        return (f"The {info['attacker']} skewers the opponent's {info['attacked']} "
                f"and threatens to take the {info['captured']} on the next move.")

    @staticmethod
    def pin_explanation(info):
        if info['enable'] is False:
            return ""
        return f"This is a {info['type']} pin. It pins the {info['pinned']} to the {info['defended']}."

    @staticmethod
    def battery_explanation(info):
        if info['enable'] is False:
            return ""
        return f"It creates a battery formed by the {info['moved']} and the {info['attacker']}."

    @staticmethod
    def discovered_attack_explanation(info):
        if info['enable'] is False:
            return ""
        return (f"The {info['piece'][0]} moved and facilitates "
                f"a discovered attack to {info['piece'][1]}. ")
