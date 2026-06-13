import asyncio

from discord import Interaction, Forbidden

from core import colors
from core.database.handlers import TicketHandler


async def run_ticket_close(
    interaction: Interaction
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

    me = interaction.guild.me

    if not channel.permissions_for(me).manage_channels:
        return await interaction.response.send_message(
            view=CustomMessageComponent(
                content=(
                    "I do not have permission to delete this channel.\n"
                    "- Missing permissions: `Manage Channels`"
                ),
                accent_color=colors.red
            ),
            ephemeral=True
        )

    handler = TicketHandler(ticket.ticket_id)

    try:
        handler.set_status(1)
        handler.close_ticket(interaction.user.id)

        await interaction.response.send_message(
            view=CustomMessageComponent(
                content=(
                    f"This ticket has been closed by "
                    f"**{interaction.user.mention}** and will be deleted in **5 seconds**."
                ),
                accent_color=0xFE3641
            )
        )

        await asyncio.sleep(5)
        await channel.delete()

    except Forbidden:
        return await interaction.followup.send(
            view=CustomMessageComponent(
                content=(
                    "I could not delete this ticket.\n"
                    "- Check my role hierarchy and channel permissions."
                ),
                accent_color=colors.red
            ),
            ephemeral=True
        )