from discord import Interaction
from discord.ui import Modal, TextInput

from core import Icons
from core.database.handlers import GuildSettingsHandler


class SetMaxTicketsModal(Modal, title="Set max tickets"):
    def __init__(self, org_interaction: Interaction):
        super().__init__()

        self.org_interaction = org_interaction

    max_tickets = TextInput(
        label="Set max tickets",
        placeholder="default is 1",
        required=True
    )

    async def on_submit(self, interaction: Interaction):
        await interaction.response.defer(ephemeral=True)

        settings = GuildSettingsHandler(interaction.guild.id)

        try:
            max_tickets = int(self.max_tickets.value)

            if max_tickets < 1:
                return await interaction.followup.send(
                    content=f"{Icons.error} Max tickets must be 1 or greater.",
                    ephemeral=True
                )
            
        except ValueError:
            return await interaction.followup.send(
                content=f"{Icons.error} Max tickets must be a valid number.",
                ephemeral=True
            )   
            
        settings.set_max_tickets(max_tickets)

        from core.ui.components import SettingsMenu
        await self.org_interaction.edit_original_response(
            view=SettingsMenu(interaction.guild)
        )      



