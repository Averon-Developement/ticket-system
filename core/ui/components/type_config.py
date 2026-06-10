from discord.ui import LayoutView, Container, Section, Separator, TextDisplay, ActionRow
from discord import Guild, SeparatorSpacing

from core.database.handlers import TicketTypeHandler, TicketTypeRoleHandler, WelcomePanelHandler
from core.ui.buttons import (
    SetTypeNameButton,
    SetTypeEmojiButton,
    ConfigureWelcomePanelButton,
    BackToTicketTypesButton
)
from core.ui.dropdowns import ButtonStyleSelect, TicketCategorySelect, TicketSupportRolesSelect


STYLE_NAMES = {
    1: "Blurple",
    2: "Gray",
    3: "Green",
    4: "Red"
}

class TicketTypesConfigMenu(LayoutView):
    def __init__(
        self,
        guild: Guild,
        type_id: int
    ):
        super().__init__(timeout=None)

        type_config = TicketTypeHandler(type_id).get_type()
        support_roles = TicketTypeRoleHandler(type_id).get_roles()

        category = (
            guild.get_channel(type_config.category_id) if type_config.category_id else None
        )

        role_mentions = []
        for role_data in support_roles:
            role = guild.get_role(role_data.role_id)

            if role:
                role_mentions.append(role.mention)

        roles_text = (
            ", ".join(role_mentions)
            if role_mentions
            else "`Not set`"
        )

        container = Container()
        container.add_item(
            TextDisplay(
                content=(
                    f"## Ticket Type #{type_id}\n"
                    "Manage the settings and behavior of this ticket type.\n"
                    "Fields marked with `*` are required."
                )
            )
        )
        container.add_item(Separator(spacing=SeparatorSpacing.large))
        container.add_item(
            Section(
                TextDisplay(
                    f"***Name:** `{type_config.name if type_config.name else '`Not set (Required)`'}`\n"
                    "-# Set the name of this ticket type. This will be displayed on the ticket button.\n"
                ),
                accessory=SetTypeNameButton(type_id)
            )
        )
        container.add_item(
            Section(
                TextDisplay(
                    f"**Custom Emoji:** {type_config.emoji if type_config.emoji else '`Not set`'}\n"
                    "-# Set an emoji to display alongside the ticket button. Must be a valid Discord emoji.\n"
                ),
                accessory=SetTypeEmojiButton(type_id)
            )
        )
        container.add_item(
            TextDisplay(
                f"**Button Color:** `{STYLE_NAMES.get(type_config.button_style)}`\n"
                "-# Choose the color of the button displayed to users."
            )
        )
        container.add_item(
            ActionRow(ButtonStyleSelect(type_id))
        )
        container.add_item(
            TextDisplay(
                f"***Category:** "
                f"`{category.name if category else '`Not set (Required)`'}`\n"
                "-# Select the category where tickets of this type will be created."
            )
        )
        container.add_item(
            ActionRow(
                TicketCategorySelect(type_id)
            )
        )
        container.add_item(
            TextDisplay(
                f"**Support Roles:** {roles_text}\n"
                "-# Select up to 3 roles that should have access to tickets of this type."
            )
        )
        container.add_item(
            ActionRow(
                TicketSupportRolesSelect(type_id)
            )
        )
        container.add_item(Separator(spacing=SeparatorSpacing.large))

        panel_config = WelcomePanelHandler.get_panel_by_type(type_id)

        is_valid = all([
            type_config.name,
            type_config.category_id,
            panel_config,
            panel_config.title if panel_config else None,
            panel_config.description if panel_config else None
        ])

        container.add_item(
            ActionRow(
                ConfigureWelcomePanelButton(type_id),
                BackToTicketTypesButton(disabled=not is_valid)
            )
        )

        self.add_item(container)