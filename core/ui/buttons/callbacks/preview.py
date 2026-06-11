from discord import Interaction

from core.ui.buttons import AppButton


async def preview_panel(
    interaction: Interaction,
    button: AppButton
) -> None:
    from core.ui.components import TicketPanel

    await interaction.response.send_message(
        view=TicketPanel(
            button.data["panel_id"],
            interaction,
            preview=True
        ),
        ephemeral=True
    )

async def preview_welcome_message(
    interaction: Interaction,
    button: AppButton
) -> None:
    from core.ui.components import WelcomePanelPreview

    await interaction.response.send_message(
        view=WelcomePanelPreview(
            button.data["panel_id"],
            interaction,
            preview=True
        ),
        ephemeral=True
    )