from discord.ext import commands
from discord import app_commands, Interaction, Member, CategoryChannel

from core.commands import (
    run_ticket_setup,
    run_ticket_rename,
    run_ticket_add,
    run_ticket_remove,
    run_ticket_move,
    run_ticket_close
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
    @app_commands.checks.has_permissions(manage_messages=True)
    @app_commands.describe(name="The new ticket name.")
    async def rename(self, interaction: Interaction, name: str):
        await run_ticket_rename(interaction, name)


    @ticket.command(
        name="add",
        description="Add a member to the ticket."
    )
    @app_commands.checks.has_permissions(manage_messages=True)
    @app_commands.describe(member="The member you want to add.")
    async def add(self, interaction: Interaction, member: Member):
        await run_ticket_add(interaction, member)


    @ticket.command(
        name="remove",
        description="Remove a member from the ticket."
    )
    @app_commands.checks.has_permissions(manage_messages=True)
    @app_commands.describe(member="The member you want to remove.")
    async def add(self, interaction: Interaction, member: Member):
        await run_ticket_remove(interaction, member)


    @ticket.command(
        name="move",
        description="Move the current ticket to another category."
    )
    @app_commands.checks.has_permissions(manage_messages=True)
    @app_commands.describe(category="The category to move this ticket to.")
    async def move(
        self,
        interaction: Interaction,
        category: CategoryChannel
    ):
        await run_ticket_move(interaction, category)

    @ticket.command(
        name="close",
        description="Close the current ticket."
    )
    @app_commands.checks.has_permissions(manage_messages=True)
    async def close(self, interaction: Interaction):
        await run_ticket_close(interaction)


async def setup(client: commands.Bot) -> None:
    await client.add_cog(Ticket(client)) 