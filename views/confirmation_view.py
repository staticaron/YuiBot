from discord import ButtonStyle
from discord.ui import View, Button

class ConfirmationView(View):

    def __init__(self, yes_callback:callable, no_callback:callable):
        super().__init__(timeout=60)

        yes_btn = Button(label="CONFIRM", style=ButtonStyle.green)
        no_btn = Button(label="REJECT", style=ButtonStyle.gray)

        yes_btn.callback = yes_callback
        no_btn.callback = no_callback

        self.add_item(yes_btn)
        self.add_item(no_btn)

