import time

from discord import Interaction

from core import Icons
from core.database.handlers import TicketHandler

RENAME_COOLDOWN: int = 300


async def run_ticket_rename(
    interaction: Interaction,
    name: str
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
    
    new_name = name.strip().lower()

    if channel.name == new_name:
        return await interaction.edit_original_response(
            content=f"{Icons.error} The ticket already has that name."
        )
    
    if (
        ticket.renamed_at is not None
        and int(time.time()) - ticket.renamed_at < RENAME_COOLDOWN
    ):
        remaining = int(
            RENAME_COOLDOWN - (time.time() - ticket.renamed_at)
        ) 

        minutes = remaining // 60
        seconds = remaining % 60

        return await interaction.edit_original_response(
            content=(
                f"{Icons.error} This ticket was renamed recently. "
                f"Please wait **{minutes}m {seconds}s** before renaming it again."
            )
        ) 

    me = interaction.guild.me
    if not channel.permissions_for(me).manage_channels:
        return await interaction.edit_original_response(
            content=(
                f"{Icons.error} I do not have permission to manage this channel.\n"
                "- Missing permissions: `Manage Channels`"
            )
        )

    await channel.edit(name=new_name)

    TicketHandler(ticket.ticket_id).set_renamed_at(int(time.time()))

    await interaction.edit_original_response(
        content=f"{Icons.success} Ticket renamed successfully."
    )
    
