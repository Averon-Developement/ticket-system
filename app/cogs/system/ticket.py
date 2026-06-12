from discord.ext import commands
from discord import app_commands, Interaction, Member

from core.commands import (
    run_ticket_setup,
    run_ticket_rename,
    run_ticket_add
)


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
    @app_commands.checks.has_permissions(administrator=True)
    async def setup(self, interaction: Interaction):
        await interaction.response.defer(ephemeral=True)
        await run_ticket_setup(interaction)


    @ticket.command(
        name="rename",
        description="Rename the current ticket."
    )
    @app_commands.describe(name="The new ticket name.")
    async def rename(self, interaction: Interaction, name: str):
        await interaction.response.defer(ephemeral=True)
        await run_ticket_rename(interaction, name)


    @ticket.command(
        name="add",
        description="Add a member to the ticket."
    )
    @app_commands.describe(member="The member you want to add.")
    async def add(self, interaction: Interaction, member: Member):
        await interaction.response.defer(ephemeral=True)
        await run_ticket_add(interaction, member)


async def setup(client: commands.Bot) -> None:
    await client.add_cog(Ticket(client)) 