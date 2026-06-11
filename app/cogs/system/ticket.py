from discord.ext import commands
from discord import app_commands, Interaction

from core.ui.components import SettingsMenu
from core import Icons

from core.database.handlers import (
    GuildSettingsHandler,
    TicketPanelHandler,
    WelcomePanelHandler,
    TicketTypeHandler
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
    async def setup(
        self, interaction: Interaction
    ):
        await interaction.response.defer(ephemeral=True)

        if not interaction.user.guild_permissions.administrator:
            return await interaction.edit_original_response(
                content=f"{Icons.error} You do not have the permissions to execute this command."
            )

        guild_id: int = interaction.guild.id
        settings = GuildSettingsHandler(guild_id).get_settings()

        ticket_panel = TicketPanelHandler.get_panel_by_guild(settings.guild_id)
        ticket_type = TicketTypeHandler.get_total_types(settings.guild_id)

        if not ticket_panel and ticket_type == 0:
            panel_id = TicketPanelHandler.create_panel(settings.guild_id)
            panel_handler = TicketPanelHandler(panel_id)
            panel_handler.set_title("Support")
            panel_handler.set_description("Click the button below to create a ticket.")

            type_id = TicketTypeHandler.create_ticket_type(settings.guild_id)
            type_handler = TicketTypeHandler(type_id)
            type_handler.set_name("Support")
            type_handler.set_button_name("Create ticket")
            
            welcome_panel_id = WelcomePanelHandler.create_panel(settings.guild_id, type_id)
            welcome_handler = WelcomePanelHandler(welcome_panel_id)
            welcome_handler.set_title("Welcome {user.mention}")
            welcome_handler.set_description(
                (
                    "Thank you for contacting support.\n"
                    "Please describe your issue in as much detail as possible below.\n\n"
                    "A staff member will assist you as soon as possible."
                )
            )

        await interaction.edit_original_response(
            view=SettingsMenu(interaction.guild)
        )


async def setup(client: commands.Bot) -> None:
    await client.add_cog(Ticket(client)) 