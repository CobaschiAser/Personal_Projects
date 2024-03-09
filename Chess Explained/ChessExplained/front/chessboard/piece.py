import customtkinter
from PIL import Image

from back.utils import BoardUtils


class Piece(customtkinter.CTkImage):
    def __init__(self, color, piece_type, position):
        self.color = color
        self.piece_type = piece_type
        self.position = position

        super().__init__(light_image=Image.open(self.get_image()), dark_image=Image.open(self.get_image()),
                         size=(60, 60))

    def get_image(self):
        icon = ('w' if self.color else 'b') + str.lower(BoardUtils.expand_piece_name(self.piece_type)) + ".png"

        return f"front/assets/pieces_icons/{icon}"
