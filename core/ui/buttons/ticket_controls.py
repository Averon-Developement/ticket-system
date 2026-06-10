from discord.ui import Button, View
from discord import ButtonStyle

class TicketActionsView(View):
    def __init__(self):
        super().__init__(timeout=None)

        self.add_item(TicketCloseButton())
        self.add_item(TicketClaimButton())

class TicketCloseButton(Button):
    def __init__(self):
        super().__init__(
            label="Close",
            style=ButtonStyle.danger,
            custom_id="ticket_close",
            emoji="🔒"
        )

    async def callback(self, interaction):
        pass


class TicketClaimButton(Button):
    def __init__(self):
        super().__init__(
            label="Claim",
            style=ButtonStyle.gray,
            custom_id="ticket_claim",
            emoji="📌"
        )

    async def callback(self, interaction):
        pass