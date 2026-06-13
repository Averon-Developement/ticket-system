from discord import Interaction, Member, Forbidden

from core import colors
from core.database.handlers import TicketHandler


async def run_ticket_remove(
    interaction: Interaction,
    member: Member
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
                    "I do not have permission to manage this channel.\n"
                    "- Missing permissions: `Manage Channels`"
                ),
                accent_color=colors.red
            ),
            ephemeral=True
        )

    if not channel.permissions_for(member).view_channel:
        return await interaction.response.send_message(
            view=CustomMessageComponent(
                content=f"{member.mention} does not have access to this ticket.",
                accent_color=colors.red
            ),
            ephemeral=True
        )

    try:
        await channel.set_permissions(member, overwrite=None)

    except Forbidden:
        return await interaction.response.send_message(
            view=CustomMessageComponent(
                content=(
                    f"I could not remove {member.mention} from this ticket.\n"
                    "- Check my role hierarchy and channel permissions."
                ),
                accent_color=colors.red
            )
        )

    await interaction.response.send_message(
        view=CustomMessageComponent(
            content=f"{member.mention} has been removed from this ticket.",
            accent_color=colors.green
        )
    )