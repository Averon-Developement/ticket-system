from discord import Interaction, CategoryChannel, Forbidden

from core import colors
from core.database.handlers import TicketHandler


async def run_ticket_move(
    interaction: Interaction,
    category: CategoryChannel
) -> None:

    from core.ui.components import CustomMessageComponent

    channel = interaction.channel

    if channel is None:
        return await interaction.response.send_message(
            view=CustomMessageComponent(
                content="Unable to determine the current channel.",
                accent_color=colors.red
            ),
            ephemeral=True
        )

    ticket = TicketHandler.get_by_channel(channel.id)
    if not ticket:
        return await interaction.response.send_message(
            view=CustomMessageComponent(
                content="This is not a ticket channel. Please use this command inside a ticket channel.",
                accent_color=colors.red
            ),
            ephemeral=True
        )

    try:
        await channel.edit(category=category)

    except Forbidden:
        return await interaction.response.send_message(
            view=CustomMessageComponent(
                content=(
                    f"I could not move this ticket to **{category.name}**.\n"
                    "- Check my role hierarchy and permissions."
                ),
                accent_color=colors.red
            ),
            ephemeral=True
        )

    await interaction.response.send_message(
        view=CustomMessageComponent(
            content=f"Ticket moved to **{category.name}**.",
            accent_color=colors.green
        )
    )