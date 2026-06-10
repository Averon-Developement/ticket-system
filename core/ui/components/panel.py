from discord.ui import LayoutView, Container, Section, Separator, TextDisplay, Thumbnail, ActionRow
from discord import SeparatorSpacing, Interaction, ButtonStyle

from core import replace_text_placeholders, replace_thumbnail_placeholder
from core.database.handlers import TicketPanelHandler, TicketTypeHandler
from core.ui.buttons import (
    SetAccentColorButton,
    SetTitleButton,
    SetDescriptionButton,
    SetThumbnailButton,
    BackToSettingsButton,
    PreviewPanelButton,
    SendPanelToChannelButton,
    CreateTicketButton
)


class PanelMenu(LayoutView):
    def __init__(self, panel_id: int):
        super().__init__(timeout=None)

        panel_config = TicketPanelHandler(panel_id).get_panel()

        container = Container()
        container.add_item(
            TextDisplay(
                content=(
                    "## Configure Ticket Panel\n"
                    "Customize the panel users will see when creating this ticket type.\n"
                    "Fields marked with `*` are required."
                )
            )
        )

        container.add_item(Separator(spacing=SeparatorSpacing.large))

        container.add_item(
            Section(
                TextDisplay(
                    f"**Accent Color:** "
                    f"{f'`#{panel_config.accent_color:06X}`' if panel_config.accent_color else '`Not set`'}\n"
                    "-# Set the accent color displayed on the ticket panel."
                ),
                accessory=SetAccentColorButton(panel_id, "main")
            )
        )

        container.add_item(
            Section(
                TextDisplay(
                    f"**Title:** "
                    f"{f'`{panel_config.title}`' if panel_config.title else '`Not set`'}\n"
                    "-# Set the title displayed at the top of the ticket panel. "
                    "Available placeholders: `{user.mention}`, `{user.name}`, `{user.displayname}` and `{user.id}`."
                ),
                accessory=SetTitleButton(panel_id, "main")
            )
        )

        description_preview = (
            panel_config.description[:100] + "..."
            if panel_config.description and len(panel_config.description) > 100
            else panel_config.description
        )

        container.add_item(
            Section(
                TextDisplay(
                    f"**Description:**\n"
                    f"```{description_preview if description_preview else 'Not set'}```\n"
                    "-# Set the description displayed in the ticket panel. "
                    "Markdown and placeholders are supported: `{user.mention}`, `{user.name}`, `{user.displayname}` and `{user.id}`."
                ),
                accessory=SetDescriptionButton(panel_id, "main")
            )
        )

        thumbnail_preview = panel_config.thumbnail_url

        if thumbnail_preview and len(thumbnail_preview) > 50:
            thumbnail_preview = thumbnail_preview[:50] + "..."

        container.add_item(
            Section(
                TextDisplay(
                    f"**Thumbnail URL:** "
                    f"{f'`{thumbnail_preview}`' if thumbnail_preview else '`Not set`'}\n"
                    "-# Set the thumbnail image displayed in the ticket panel. "
                    "Supports image URLs and the `{user.avatar}` placeholder."
                ),
                accessory=SetThumbnailButton(panel_id, "main")
            )
        )

        container.add_item(Separator(spacing=SeparatorSpacing.large))

        is_valid = all([
            panel_config.title,
            panel_config.description
        ])

        container.add_item(
            ActionRow(
                BackToSettingsButton(disabled=not is_valid),
                PreviewPanelButton(panel_config.panel_id, disabled=not is_valid),
                SendPanelToChannelButton(panel_config.panel_id, disabled=not is_valid)
            )
        )

        self.add_item(container)


class TicketPanel(LayoutView):
    def __init__(
        self,
        panel_id: int,
        interaction: Interaction,
        preview: bool
    ):
        super().__init__(timeout=None)

        panel_config = TicketPanelHandler(panel_id).get_panel()

        member = interaction.user

        container = Container(accent_color=panel_config.accent_color)

        content = TextDisplay(
            f"## {replace_text_placeholders(panel_config.title, member)}\n"
            f"{replace_text_placeholders(panel_config.description, member)}"
        )

        thumbnail = (
            replace_thumbnail_placeholder(panel_config.thumbnail_url, member)
            if panel_config.thumbnail_url
            else None
        )

        if thumbnail:
            container.add_item(
                Section(
                    content,
                    accessory=Thumbnail(media=thumbnail)
                )
            )
        else:
            container.add_item(content)

        if not preview:
            container.add_item(Separator(spacing=SeparatorSpacing.large))

            types = TicketTypeHandler.get_guild_types(interaction.guild.id)

            row = ActionRow()

            for type in types:
                row.add_item(
                    CreateTicketButton(
                        type_id=type.type_id,
                        name=type.name,
                        style=ButtonStyle(type.button_style),
                        emoji=type.emoji
                    )
                )                

            container.add_item(row)

        self.add_item(container)
