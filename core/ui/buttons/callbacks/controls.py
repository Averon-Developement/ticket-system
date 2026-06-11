from discord import Interaction
from discord.ui import View

from core.ui.buttons import AppButton
from core.ui.dropdowns import SendTicketPanelToChannelSelect

from core.database.handlers import WelcomePanelHandler


async def send_panel_to_channel(
    interaction: Interaction,
    button: AppButton
) -> None:
    view = View(timeout=60)

    view.add_item(
        SendTicketPanelToChannelSelect(
            button.data["panel_id"]
        )
    )

    await interaction.response.send_message(
        content=(
            "Select the channel where the "
            "ticket panel should be sent to."
        ),
        view=view,
        ephemeral=True
    )

async def back_to_settings(
    interaction: Interaction,
    _: AppButton
) -> None:
    from core.ui.components import SettingsMenu

    await interaction.response.edit_message(
        view=SettingsMenu(interaction.guild)
    )

async def back_to_ticket_types(
    interaction: Interaction,
    _: AppButton
) -> None:
    from core.ui.components import TicketTypesMenu

    await interaction.response.edit_message(
        view=TicketTypesMenu(interaction.guild)
    )


async def back_to_type_config(
    interaction: Interaction,
    button: AppButton
) -> None:
    from core.ui.components import TicketTypesConfigMenu

    await interaction.response.edit_message(
        view=TicketTypesConfigMenu(
            interaction.guild,
            button.data["type_id"]
        )
    )

async def edit_welcome_panel(
    interaction: Interaction,
    button: AppButton
) -> None:
    panel_config = WelcomePanelHandler.get_panel_by_type(
        button.data["type_id"]
    )

    from core.ui.components import WelcomePanelMenu

    await interaction.response.edit_message(
        view=WelcomePanelMenu(
            panel_config.panel_id
        )
    )