import customtkinter


class PopupWindow(customtkinter.CTkToplevel):
    """
    Popup window for displaying a message with an 'Ok' button.

    Parameters:
        master (Tk): The master window.
        title (str): The title of the popup window.
        message (str): The message to be displayed in the popup.
        **kwargs: Additional keyword arguments.

    Attributes:
        message_label (customtkinter.CTkLabel): Label displaying the message.
        ok_button (customtkinter.CTkButton): Button to acknowledge and close the popup.
    """

    def __init__(self, master, title, message, **kwargs):
        """
        Initialize the PopupWindow.

        Parameters:
            master (Tk): The master window.
            title (str): The title of the popup window.
            message (str): The message to be displayed in the popup.
            **kwargs: Additional keyword arguments.
        """
        super().__init__(master, **kwargs)

        self.title(title)
        self.geometry(f"{400}x{200}")
        self.resizable(False, False)
        self.grid_columnconfigure(0, weight=1)

        # Message Label
        self.message_label = customtkinter.CTkLabel(master=self,
                                                    text=message)
        self.message_label.grid(row=0, column=0,
                                padx=20, pady=20,
                                sticky="ew")

        # Ok Button
        self.ok_button = customtkinter.CTkButton(master=self,
                                                 text="Ok",
                                                 command=self.ok_button_event)
        self.ok_button.grid(row=1, column=0,
                            padx=20, pady=20,
                            sticky="ew")

        # Deactivate the main window
        self.grab_set()

    def ok_button_event(self):
        """
        Event handler for the 'Ok' button. Destroys the popup window.
        """
        self.destroy()
