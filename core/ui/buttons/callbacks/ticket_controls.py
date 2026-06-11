import asyncio
from discord import Interaction

from core.database.handlers import TicketHandler
from core.ui.buttons import AppButton

from core import Icons


async def close_ticket_canceled(
    interaction: Interaction,
    _: AppButton
) -> None:
    
    await interaction.response.edit_message(
        content=f"{Icons.error} Ticket close canceled.",
        view=None,
        delete_after=5
    )


async def close_ticket_confirmed(
    interaction: Interaction,
    _: AppButton
) -> None:
    
    ticket = TicketHandler.get_by_channel(interaction.channel.id)
    handler = TicketHandler(ticket.ticket_id)

    handler.set_status(1) # set status 1 (closed) 
    handler.close_ticket(interaction.user.id)

    await interaction.response.edit_message(
        content=f"{Icons.success} You have successfully closed the ticket.",
        view=None
    )

    from core.ui.components import CustomMessageComponent

    await interaction.channel.send(
        view=CustomMessageComponent(
            title="Ticket Closed",
            content=(
                "This ticket has been closed and will be closed in **3 seconds**.\n"
                f"-# Closed by: `{interaction.user.name}`"
            ),
            accent_color=0xFE3641
        )
    )

    await asyncio.sleep(3)
    await interaction.channel.delete()
    