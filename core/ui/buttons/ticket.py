from discord.ui import Button, View
from discord import ButtonStyle, Interaction

from core.database.handlers import TicketTypeHandler 


class PersistentTicketPanel(View):
    def __init__(self):
        super().__init__(timeout=None)

        for type in TicketTypeHandler.get_all_types():
            self.add_item(
                CreateTicketButton(
                    type_id=type.type_id,
                    name=type.name,
                    style=ButtonStyle(type.button_style),
                    emoji=type.emoji
                )
            )


class CreateTicketButton(Button):
    def __init__(
        self,
        type_id: int,
        name: str,
        style: ButtonStyle,
        emoji: str | None = None
    ):
        super().__init__(
            label=name,
            style=style,
            emoji=emoji,
            custom_id=f"ticket_type:{type_id}"
        )

        self.type_id = type_id

    async def callback(self, interaction: Interaction):
        await interaction.response.send_message(
            f"Creating ticket for type {self.type_id}",
            ephemeral=True
        )