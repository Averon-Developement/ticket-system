from discord.ext import commands
from discord import app_commands, Interaction

from core.ui.components import SettingsMenu
from core import Icons


class Ticket(commands.Cog):
    def __init__(self, client):
        self.client: commands.Bot = client

    ticket = app_commands.Group(
        name="ticket", 
        description="Ticket related commands"
    )

    @ticket.command(
        name="setup",
        description="Configure the ticket system settings"
    )
    async def setup(
        self, interaction: Interaction
    ):
        await interaction.response.defer(ephemeral=True)

        if not interaction.user.guild_permissions.administrator:
            return await interaction.edit_original_response(
                content=f"{Icons.error} You do not have the permissions to execute this command."
            )


        # if no config is found add some basic logic.




        await interaction.edit_original_response(
            view=SettingsMenu(interaction.guild)
        )


async def setup(client: commands.Bot) -> None:
    await client.add_cog(Ticket(client)) 