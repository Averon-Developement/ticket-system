from discord import Interaction

from core.database.handlers import GuildSettingsHandler, TicketPanelHandler
from core.ui.buttons import AppButton


async def toggle_transcripts(
    interaction: Interaction,
    button: AppButton
) -> None:
    enabled = button.data["enabled"]

    GuildSettingsHandler(interaction.guild.id).set_transcripts(not enabled)

    from core.ui.components import SettingsMenu

    await interaction.response.edit_message(
        view=SettingsMenu(interaction.guild)
    )


async def navigate_ticket_types(
    interaction: Interaction,
    _: AppButton
) -> None:
    from core.ui.components import TicketTypesMenu

    await interaction.response.edit_message(
        view=TicketTypesMenu(interaction.guild)
    )


async def navigate_ticket_panel(
    interaction: Interaction,
    _: AppButton        
) -> None:
    panel_config = (
        TicketPanelHandler.get_panel_by_guild(interaction.guild.id)
    )

    panel_id = (
        panel_config.panel_id if panel_config
        else TicketPanelHandler.create_panel(
            interaction.guild.id
        )
    )

    from core.ui.components import PanelMenu

    await interaction.response.edit_message(
        view=PanelMenu(panel_id)
    )