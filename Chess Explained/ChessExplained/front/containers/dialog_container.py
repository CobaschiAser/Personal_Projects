import customtkinter
from chatterbot import ChatBot
from customtkinter import *

from back.utils import Util


class DialogContainer(customtkinter.CTkFrame):
    def __init__(self, master, width, height, **kwargs):
        super().__init__(master, width=width, height=height, **kwargs)
        self.chatbot = ChatBot("back",
                               preprocessors=['chatterbot.preprocessors.convert_to_ascii',
                                              'chatterbot.preprocessors.unescape_html',
                                              'chatterbot.preprocessors.clean_whitespace'],
                               logic_adapters=[
                                   {
                                       'import_path': 'chatterbot.logic.BestMatch',
                                       'default_response': 'Sorry, I am unable to process your request.',
                                       'maximum_similarity_threshold': 0.90
                                   }
                               ]
                               )
        self.responses = ResponsesContainer(self, **kwargs)
        self.responses.grid(row=0, column=0,
                            columnspan=2,
                            sticky="nsew",
                            padx=10, pady=10)

        self.entryBox = CTkTextbox(master=self, width=350, height=80)
        self.entryBox.grid(row=1, column=0,
                           columnspan=1, rowspan=1,
                           sticky="nsew",
                           padx=10, pady=10)

        # Enter key sends the message
        self.entryBox.bind("<Return>", self.add_question_answer)
        self.entryBox.focus()

    def add_question_answer(self, _):
        text = self.entryBox.get("1.0", "end-1c")
        # Add the texts to the dialog, 0 is for the bot, 1 for the user
        self.responses.add_text(text, 1)
        response = self.get_response(text)
        self.responses.add_text(response, 0)

        # Clear the text in the CTkTextbox
        self.entryBox.delete("1.0", "end-1c")
        self.responses.update()

        return "break"

    def add_text(self, text, turn=0):
        self.responses.add_text(text, turn)
        self.responses.update()

    def get_response(self, msg):
        response = Util.process_question(msg)
        if response is None:
            response = str(self.chatbot.get_response(msg.lower()))
        return response


class ResponsesContainer(customtkinter.CTkScrollableFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, width=350, height=500, **kwargs)
        # Background color for the text bubble, 0 is for the bot, 1 for user
        self.textbox_bg = ["#33cccc", "#3399ff"]
        # Text color for the text bubble, 0 is for the bot, 1 for user
        self.text_color = ["#ffffff", "#ffffff"]

        self.messages = ["Hi, how can I help you?"]
        self.turn = [0]
        self.textBox = []
        for i, message in enumerate(self.messages):
            self.create_conversation(i, message)

    def add_text(self, message, turn):
        self.messages.append(message)
        self.turn.append(turn)
        self.create_conversation(len(self.messages) - 1, message)

    def create_conversation(self, index, message):
        # maximum number of columns, will be used to float the user's input to the right
        max_column = 280 // 2 + 1
        font_size = 8
        offset=20
        message_width = len(message) * font_size + offset
        message_height = (message_width // 280 + 1) * 25
        message_width = min(280, message_width)
        columnspan = message_width // 2 + 1

        # either 0 or the position of the user's input in columns
        column = self.turn[index] * (max_column - columnspan)
        print(column,columnspan)

        self.textBox.append(CTkTextbox(master=self,
                                       height=message_height, width=message_width,
                                       fg_color=self.textbox_bg[self.turn[index]],
                                       text_color=self.text_color[self.turn[index]]))

        self.textBox[index].insert("1.0", message)
        # self.textBox[index].grid(row=index, column=column, columnspan=columnspan, sticky="nsew", padx=10, pady=10)
        self.textBox[index].grid(row=index, column=column, columnspan=max_column, sticky="nsew",
                                 padx=(10+(self.turn[index])*20, 10+(1-self.turn[index])*20), pady=10)
        self.textBox[index].configure(state=DISABLED)
