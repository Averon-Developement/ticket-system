from discord import Interaction, Member, Forbidden

from core import Icons
from core.database.handlers import TicketHandler


async def run_ticket_add(
    interaction: Interaction,
    member: Member
) -> None:

    channel = interaction.channel

    if channel is None:
        return await interaction.edit_original_response(
            content=f"{Icons.error} Unable to determine the current channel."
        )

    ticket = TicketHandler.get_by_channel(channel.id)
    if not ticket:
        return await interaction.edit_original_response(
            content=(
                f"{Icons.error} This is not a ticket channel. "
                "Please use this command in a ticket channel."
            )
        )

    me = interaction.guild.me

    if not channel.permissions_for(me).manage_channels:
        return await interaction.edit_original_response(
            content=(
                f"{Icons.error} I do not have permission to manage this channel.\n"
                "- Missing permissions: **Manage Channels**"
            )
        )

    if channel.permissions_for(member).view_channel:
        return await interaction.edit_original_response(
            content=f"{Icons.error} {member.mention} already has access to this ticket."
        )

    try:
        await channel.set_permissions(
            member,
            view_channel=True,
            send_messages=True,
            read_message_history=True,
            attach_files=True,
            embed_links=True
        )

    except Forbidden:
        return await interaction.edit_original_response(
            content=(
                f"{Icons.error} I could not add {member.mention} to this ticket.\n"
                "- Check my role hierarchy and channel permissions."
            )
        )

    await interaction.edit_original_response(
        content=f"{Icons.success} Added {member.mention} to this ticket."
    )