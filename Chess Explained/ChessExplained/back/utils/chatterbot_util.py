import string
import re


class Util:
    @staticmethod
    def import_data(path):
        with open(path, "r") as file:
            games = file.read().split(sep="#\n")
            games = games[0:(len(games) - 1)]
        return games

    @staticmethod
    def get_frequent_last_three(games):
        repeated = []
        counts = []

        games = [game.replace("+", "").split(" ") for game in games]
        games = [tuple(game[-5:len(game):2]) for game in games]

        for last_three in games:
            if len(last_three) > 2:
                count = games.count(last_three)
                if count >= 2:
                    if last_three not in repeated:
                        repeated.append(last_three)
                        counts.append(count)
        return repeated, counts

    @staticmethod
    def extract_chess_notations(input_string):
        # check for castling
        if "O-O-O" in input_string:
            queenSide = True
            input_string = input_string.replace("O-O-O", "")
            print(input_string)
        else:
            queenSide = False

        if "O-O" in input_string:
            kingSide = True
        else:
            kingSide = False

        # Define the regex pattern for chess algebraic notation
        for punctuation in string.punctuation:
            if punctuation != '+' and punctuation != '#':  # Exclude both + and #
                input_string = input_string.replace(punctuation, ' ')
        pattern = r'\s[PNBRQK]?[a-h]?[1-8]?[x]?[a-h][1-8][\+#]?\s'  # Include # in the pattern

        # Use re.findall to find all matches in the input string
        matches = re.findall(pattern, input_string)
        clean_matches = [i.strip() for i in matches]

        if queenSide:
            clean_matches += ["O-O-O"]
        if kingSide:
            clean_matches += ["O-O"]

        print(clean_matches)
        return clean_matches

    @staticmethod
    def get_name_piece(p):
        if p == 'Q':
            return "White Queen"
        if p == 'q':
            return "Black Queen"
        if p == 'K':
            return "White King"
        if p == 'k':
            return "Black King"
        if p == 'B':
            return "White Bishop"
        if p == 'b':
            return "Black Bishop"
        if p == 'R':
            return "White Rock"
        if p == 'r':
            return "Black Rock"
        if p == 'N':
            return "White Knight"
        if p == 'n':
            return "Black Knight"
        return ""

    @staticmethod
    def get_rank(pos):
        if pos == 'a':
            return "first"
        if pos == 'b':
            return "second"
        if pos == 'c':
            return "third"
        if pos == 'd':
            return "fourth"
        if pos == 'e':
            return "fifth"
        if pos == 'f':
            return "sixth"
        if pos == 'g':
            return "seventh"
        if pos == 'h':
            return "eighth"

    @staticmethod
    def get_file(pos):
        if pos == '1':
            return "first"
        if pos == '2':
            return "second"
        if pos == '3':
            return "third"
        if pos == '4':
            return "fourth"
        if pos == '5':
            return "fifth"
        if pos == '6':
            return "sixth"
        if pos == '7':
            return "seventh"
        if pos == '8':
            return "eighth"

    @staticmethod
    def preprocess_san(result):
        if result == "O-O-O":
            return "O-O-O represents QueenSide Castling"
        if result == "O-O":
            return "O-O represents KingSide Castling"
        capture = None
        column_attack = None
        if result[0] not in "KkQqNnRrBb":
            piece = "Pawn"
            if result[0] == 'x':
                capture = "capture"
                rank = Util.get_rank(result[1])
                file = Util.get_file(result[2])
            elif result[0] != 'x' and result[1] == 'x':
                capture = "capture"
                column_attack = Util.get_rank(result[0])
                rank = Util.get_rank(result[2])
                file = Util.get_file(result[3])
            else:
                rank = Util.get_rank(result[0])
                file = Util.get_file(result[1])
        else:
            piece = Util.get_name_piece(result[0])
            if result[1] == 'x':
                capture = "capture"
                rank = Util.get_rank(result[2])
                file = Util.get_file(result[3])
            else:
                rank = Util.get_rank(result[1])
                file = Util.get_file(result[2])

        last_ch = result[len(result) - 1]
        action = None
        if last_ch == '+':
            action = "check"
        elif last_ch == '#':
            action = "checkmate"

        if capture is not None and action is not None:
            if column_attack is not None:
                message = (f"{piece} is moved from column {column_attack} to {file} "
                           f"line and {rank} column and generates {capture} and {action}.")
            else:
                message = (f"{piece} is moved to {file} line and {rank} column "
                           f"and generates {capture} and {action}. ")
        elif capture is not None and action is None:
            if column_attack is not None:
                message = (f"{piece} is moved from column {column_attack} to {file} line "
                           f"and {rank} column and generates {capture}. ")
            else:
                message = f"{piece} is moved to {file} line and {rank} column and generates {capture}. "
        elif capture is None and action is not None:
            message = f"{piece} is moved to {file} line and {rank} column and generates {action}. "
        else:
            message = f"{piece} is moved to {file} line and {rank} column. "

        return message

    @staticmethod
    def process_question(question):
        results = Util.extract_chess_notations(question)
        if len(results) == 0:
            return None
        answer = "".join(Util.preprocess_san(result) for result in results)
        return answer
