# import chess
# import chess.svg
# import customtkinter
# from customtkinter import *
# from PIL import Image
# from chatterbot import ChatBot
# import back.stockfish_tools as sf
# from back.utils import BoardUtils
# from back.utils import Util
# from svglib.svglib import svg2rlg
# from reportlab.graphics import renderPDF
# from pdf2image import convert_from_path
#
# from front.chessboard import Board
# from front.containers import MenuContainer, Dialog
#
#
# class App(CTk):
#
#     def __init__(self, engine_path, *args, **kwargs):
#
#         super().__init__(*args, **kwargs)
#         self.engine_path = engine_path
#         self.stockfish = sf.Stockfish(engine_path=self.engine_path)
#         self.title("Chess Explained")
#         self.geometry("680x680")
#         self.minsize(1080, 680)
#         self.resizable(True, True)
#         self.chatbot = ChatBot("back",
#                                preprocessors=['chatterbot.preprocessors.convert_to_ascii',
#                                               'chatterbot.preprocessors.unescape_html',
#                                               'chatterbot.preprocessors.clean_whitespace'],
#                                logic_adapters=[
#                                    {
#                                        'import_path': 'chatterbot.logic.BestMatch',
#                                        'default_response': 'Sorry, I am unable to process your request.',
#                                        'maximum_similarity_threshold': 0.90
#                                    }
#                                ]
#                                )
#
#         # Center the content
#         self.grid_rowconfigure(1, weight=1)
#         self.grid_columnconfigure((0, 1, 2), weight=1)
#         self.dialog = Dialog(master=self, width=50, height=680)
#         self.menu = Menu(master=self, dialog=self.dialog)
#         self.menu.grid(row=0, column=1,
#                        sticky="nsew",
#                        padx=10, pady=10)
#
#         self.board = Board(master=self, stockfish=self.stockfish)
#         self.board.grid(row=1, column=1,
#                         sticky="nsew",
#                         padx=10, pady=10)
#
#         # self.dialog.grid(row=0, column=2,
#         #                  columnspan=10, rowspan=10,
#         #                  sticky="nsew",
#         #                  padx=10, pady=10)
#         # self.dialog.grid_remove()
#
#         self.board.add_menu(self.menu)
#         self.menu.add_board(self.board)
#
#         # self.grid_rowconfigure((0, 1, 2, 3, 4, 5), weight=1)
#         # self.grid_columnconfigure(0, weight=1)
#         #
#         # self.img = CTkImage(light_image=Image.open("front/assets/label.png"),
#         #                     dark_image=Image.open("front/assets/label.png"),
#         #                     size=(680, 90))
#         # self.label = CTkLabel(master=self, image=self.img, text="")
#         # self.label.grid(row=0, column=0,
#         #                 columnspan=5,
#         #                 sticky="nsew")
#         #
#         # self.textBox = CTkTextbox(master=self)
#         # self.textBox.grid(row=1, column=0,
#         #                   rowspan=3, columnspan=5,
#         #                   sticky="nsew",
#         #                   padx=10, pady=10)
#         # self.textBox.configure(state=DISABLED)
#         #
#         # self.entryBox = CTkTextbox(master=self)
#         # self.entryBox.grid(row=4, column=0,
#         #                    columnspan=4, rowspan=2,
#         #                    sticky="nsew",
#         #                    padx=10, pady=10)
#         # self.entryBox.focus()
#         #
#         # self.button1 = CTkButton(master=self, text="Send",
#         #                          command=lambda: self._on_enter_pressed())
#         # self.button1.grid(row=4, column=4, sticky="nsew", padx=10, pady=10)
#         #
#         # self.button2 = CTkButton(master=self, text="Best Move", command=lambda: self.input())
#         # self.button2.grid(row=5, column=4, sticky="nsew", padx=10, pady=10)
#
#         # Set the theme
#         set_appearance_mode("dark")
#         customtkinter.set_default_color_theme("dark-blue")
#
#         self.mainloop()
#
#     def set_new_game(self):
#         self.new_game = True
#
#     def _on_enter_pressed(self):
#         msg = self.entryBox.get("1.0", END)
#         msg = msg.rstrip()
#         msg = msg.lstrip()
#         if not msg or msg == "":
#             return
#         else:
#             self.entryBox.delete("1.0", END)
#             self._insert_message(msg, "You")
#
#     def input(self):
#         fen_input = CTkInputDialog(text="Insert chess board FEN", title="Chess Explained")
#         fen = fen_input.get_input()
#         if fen is None:
#             return
#         fen = fen.lstrip()
#         fen = fen.rstrip()
#         if fen:
#             if BoardUtils.is_valid_fen(fen):
#                 self._get_best_move(fen)
#             else:
#                 self.textBox.configure(state=NORMAL)
#                 self.textBox.insert(END, "ChessBot: The provided fen is not a valid one\n\n")
#                 self.textBox.configure(state=DISABLED)
#
#     def _insert_message(self, msg, sender):
#         print(msg)
#         msg1 = f"{sender}: {msg}\n"
#         self.textBox.configure(state=NORMAL)
#         self.textBox.insert(END, msg1)
#         self.textBox.configure(state=DISABLED)
#         response = Util.process_question(msg)
#         if response is None:
#             response = self.chatbot.get_response(msg.lower())
#         msg2 = f"ChessBot: {response}\n\n"
#         self.textBox.configure(state=NORMAL)
#         self.textBox.insert(END, msg2)
#         self.textBox.configure(state=DISABLED)
#
#         return 0
#
#     @staticmethod
#     def reformat_board(board_string):
#         reformatted_board = ""
#         for char in board_string:
#             if char == '.':
#                 reformatted_board += char + ' '
#             else:
#                 reformatted_board += char + ' '
#         return reformatted_board.strip()
#
#     @staticmethod
#     def render_chess_position(fen):
#         board = chess.Board(fen)
#         svg_content = chess.svg.board(board=board)
#
#         with open("front/assets/board.svg", "w") as svg_file:
#             svg_file.write(svg_content)
#
#         return "front/assets/board.svg"
#
#     @staticmethod
#     def convert_svg_to_png(svg_file_path):
#         # Convert SVG to PDF
#         drawing = svg2rlg(svg_file_path)
#         renderPDF.drawToFile(drawing, "front/assets/out.pdf")
#
#         # Convert PDF to PNG
#         pages = convert_from_path('front/assets/out.pdf', poppler_path='resources/poppler-23.11.0/Library/bin')
#         pages[0].save('front/assets/board.png', 'PNG')
#
#         # Delete PDF
#         os.remove("front/assets/out.pdf")
#
#         # Delete SVG
#         os.remove(svg_file_path)
#
#         return 'front/assets/board.png'
#
#     def _get_best_move(self, fen):
#         self.textBox.configure(state=NORMAL)
#         self.textBox.insert(END, f"You: What`s the best move for this board : {fen}\n")
#         stockfish = sf.Stockfish(engine_path=self.engine_path)
#         stockfish.setup(fen)
#         explainer = sf.StockfishExplainer(stockfish)
#         board, explain = explainer.explain()
#         self.textBox.configure(state=NORMAL)
#         self.textBox.insert(END, "Chatbot: ")
#         self.textBox.insert(END, explain)
#         self.textBox.insert(END, "\n\n")
#         self.textBox.configure(state=DISABLED)
#
#         # Get svg file path
#         svg_file_path = self.render_chess_position(fen)
#
#         # Convert SVG to PNG
#         png_file_path = self.convert_svg_to_png(svg_file_path)
#
#         popup = PopupWindow(self, "Board display", png_file_path)
#         popup.wait_window()
#
#         # Delete PNG
#         os.remove(png_file_path)
#
#
# class PopupWindow(customtkinter.CTkToplevel):
#     """
#     Popup window for displaying a message with an 'Ok' button.
#
#     Parameters:
#         master (Tk): The master window.
#         title (str): The title of the popup window.
#         image (str): The path to the image to be displayed in the popup.
#         **kwargs: Additional keyword arguments.
#
#     Attributes:
#         img (ImageTk.PhotoImage): The image to be displayed in the popup.
#         ok_button (customtkinter.CTkButton): Button to acknowledge and close the popup.
#     """
#
#     def __init__(self, master, title, image, **kwargs):
#         """
#         Initialize the PopupWindow.
#
#         Parameters:
#             master (Tk): The master window.
#             title (str): The title of the popup window.
#             message (str): The message to be displayed in the popup.
#             **kwargs: Additional keyword arguments.
#         """
#         super().__init__(master, **kwargs)
#
#         self.title(title)
#         self.geometry(f"{450}x{450}")
#         self.resizable(False, False)
#         self.grid_columnconfigure(0, weight=1)
#
#         with Image.open(image) as img:
#             # Image
#             self.img = CTkImage(light_image=img,
#                                 dark_image=img,
#                                 size=(390, 390))
#             self.label = customtkinter.CTkLabel(master=self, image=self.img, text="")
#             self.label.grid(row=0, column=0,
#                             sticky="nsew")
#
#             # Ok Button
#             self.ok_button = customtkinter.CTkButton(master=self,
#                                                      text="Ok",
#                                                      command=self.ok_button_event)
#             self.ok_button.grid(row=1, column=0,
#                                 padx=20, pady=20,
#                                 sticky="ew")
#
#         # Deactivate the main window
#         self.grab_set()
#
#     def ok_button_event(self):
#         """
#         Event handler for the 'Ok' button. Destroys the popup window.
#         """
#         self.destroy()
