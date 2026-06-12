from discord import Interaction, Guild

from core import Icons
from core.ui.components import SettingsMenu
from core.database.handlers import (
    GuildSettingsHandler,
    TicketPanelHandler,
    TicketTypeHandler,
    WelcomePanelHandler
)


async def create_default_ticket_setup(guild_id: int) -> None:
    panel_id = TicketPanelHandler.create_panel(guild_id)
    panel = TicketPanelHandler(panel_id)
    panel.set_title("Support")
    panel.set_description("Click the button below to create a ticket.")

    type_id = TicketTypeHandler.create_ticket_type(guild_id)
    ticket_type = TicketTypeHandler(type_id)
    ticket_type.set_name("Support")
    ticket_type.set_button_name("Create ticket")

    welcome_id = WelcomePanelHandler.create_panel(guild_id, type_id)
    welcome = WelcomePanelHandler(welcome_id)
    welcome.set_title("Welcome {user.mention}")
    welcome.set_description(
        "Thank you for contacting support.\n"
        "Please describe your issue in as much detail as possible below.\n\n"
        "A staff member will assist you as soon as possible."
    )    


async def run_ticket_setup(interaction: Interaction) -> None:
    guild: Guild = interaction.guild
    settings = GuildSettingsHandler(guild.id).get_settings()

    if (
        not TicketPanelHandler.get_panel_by_guild(settings.guild_id)
        and TicketTypeHandler.get_total_types(settings.guild_id) == 0
    ):
        await create_default_ticket_setup(guild.id)

    await interaction.edit_original_response(
        view=SettingsMenu(guild)
    )