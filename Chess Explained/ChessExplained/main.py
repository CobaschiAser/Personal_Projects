from back.stockfish_tools import Stockfish
# from back.stockfish_tools import StockfishExplainer
from front.containers import App

engine_path = "./resources/stockfish/stockfish-windows-x86-64-modern.exe"
stockfish = Stockfish(engine_path)

new_game = "8/6r1/5n2/8/8/4B3/1k6/7K w - - 0 1"

# stockfish.setup(new_game)

# stockfish_explainer = StockfishExplainer(stockfish)
# print(stockfish_explainer.explain())

App(engine_path=engine_path)
