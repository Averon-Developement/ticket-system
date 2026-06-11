from discord import Interaction

from core import Icons
from core.database.handlers import TicketTypeHandler, WelcomePanelHandler
from core.ui.buttons import AppButton


async def create_ticket_type(
    interaction: Interaction,
    _: AppButton 
) -> None:
    total_types = TicketTypeHandler.get_total_types(
        interaction.guild.id
    )

    if total_types == 3:
        return await interaction.response.send_message(
            content=f"{Icons.error} Ticket type limit reached. A maximum of 3 ticket types can be created.",
            ephemeral=True
        )

    type_id = TicketTypeHandler.create_ticket_type(
        interaction.guild.id
    )

    handler = TicketTypeHandler(type_id)
    handler.set_name("New type")

    panel_id = WelcomePanelHandler.create_panel(
        interaction.guild.id, type_id
    )
    handler = WelcomePanelHandler(panel_id)
    handler.set_title("Welcome {user.mention},")
    handler.set_description(
        (
            "Thank you for contacting support.\n"
            "Please describe your issue in as much detail as possible below.\n\n"
            "A staff member will assist you as soon as possible."
        )
    )

    from core.ui.components import TicketTypesConfigMenu

    await interaction.response.edit_message(
        view=TicketTypesConfigMenu(interaction.guild, type_id)
    )

async def edit_ticket_type(
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

async def delete_ticket_type(
    interaction: Interaction,
    button: AppButton
) -> None:
    total_types = TicketTypeHandler.get_total_types(
        interaction.guild.id
    )

    if total_types <= 1:
        return await interaction.response.send_message(
            content=(
                f"{Icons.error} You must have at least one ticket type."
            ),
            ephemeral=True
        )

    if TicketTypeHandler.has_tickets(
        button.data["type_id"]
    ):
        return await interaction.response.send_message(
            content=(
                f"{Icons.error} This ticket type cannot be deleted "
                "because tickets exist for it."
            ),
            ephemeral=True
        )

    TicketTypeHandler(
        button.data["type_id"]
    ).delete()

    from core.ui.components import TicketTypesMenu

    await interaction.response.edit_message(
        view=TicketTypesMenu(
            interaction.guild
        )
    )