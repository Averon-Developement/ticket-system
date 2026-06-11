from discord.ui import LayoutView, Container, Separator, TextDisplay, ActionRow
from discord import Guild, SeparatorSpacing

from core.database.handlers import TicketTypeHandler
from core.ui.buttons.helpers import (
    create_ticket_type_button,
    create_ticket_type_edit_button,
    create_ticket_type_delete_button,
    create_back_to_settings_button
)


class TicketTypesMenu(LayoutView):
    def __init__(self, guild: Guild):
        super().__init__(timeout=None)

        total_types = TicketTypeHandler.get_total_types(guild.id)

        container = Container()

        container.add_item(
            TextDisplay(
                content=(
                    "## Ticket Types\n"
                    "Manage your ticket types by creating, editing, or removing them. "
                    "Ticket types define how users open tickets, including their category, "
                    "name, description, and other type-specific settings."
                )
            )
        )
        container.add_item(Separator(spacing=SeparatorSpacing.large))

        if total_types == 0:
            container.add_item(
                TextDisplay(
                    content=(
                        "-# No ticket types found. Please create one.\n"
                    )
                )
            )
            container.add_item(Separator(spacing=SeparatorSpacing.large))
        
        else:
            types = TicketTypeHandler.get_guild_types(guild.id)

            for type in types:
                container.add_item(
                    TextDisplay(
                        f"**{type.name} (#{type.type_id})**\n"
                        f"-# Use the buttons below to edit or delete this ticket type."
                    )
                )
                container.add_item(
                    ActionRow(
                        create_ticket_type_edit_button(type.type_id),
                        create_ticket_type_delete_button(type.type_id)
                    )
                )
                container.add_item(Separator(spacing=SeparatorSpacing.large))

                    
        container.add_item(
            ActionRow(
                create_back_to_settings_button(),
                create_ticket_type_button()
            )
        )

        self.add_item(container)