from discord.ui import LayoutView, Container, Section, Separator, TextDisplay, ActionRow, Thumbnail
from discord import SeparatorSpacing, Interaction

from core import replace_text_placeholders, replace_thumbnail_placeholder
from core.database.handlers import WelcomePanelHandler
from core.ui.buttons import (
    SetAccentColorButton,
    SetTitleButton,
    SetDescriptionButton,
    SetThumbnailButton,
    BackToTypeConfigButton,
    PreviewWelcomeMessageButton
)


class WelcomePanelMenu(LayoutView):
    def __init__(self, panel_id: int):
        super().__init__(timeout=None)

        panel_config = WelcomePanelHandler(panel_id).get_panel()

        container = Container()
        container.add_item(
            TextDisplay(
                content=(
                    "## Configure Welcome Panel\n"
                    "Customize the welcome message displayed when this ticket type is created.\n"
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
                    "-# Set the accent color displayed on the side of the welcome panel."
                ),
                accessory=SetAccentColorButton(panel_id)
            )
        )
        container.add_item(
            Section(
                TextDisplay(
                    f"***Title:** "
                    f"{f'`{panel_config.title}`' if panel_config.title else '`Not set`'}\n"
                    "-# Set the title displayed at the top of the welcome panel "
                    "Available placeholders: `{user.mention}`, `{user.name}`, `{user.displayname}` and `{user.id}`."
                ),
                accessory=SetTitleButton(panel_id)
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
                    f"***Description:**\n"
                    f"```{description_preview if description_preview else 'Not set'}```\n"
                    "-# Set the message displayed in the welcome panel embed. "
                    "Markdown and placeholders are supported: `{user.mention}`, `{user.name}`, `{user.displayname}` and `{user.id}`."
                ),
                accessory=SetDescriptionButton(panel_id)
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
                    "-# Set the thumbnail image displayed in the welcome panel embed. "
                    "Supports image URLs and the `{user.avatar}` placeholder."
                ),
                accessory=SetThumbnailButton(panel_id)
            )
        )

        container.add_item(Separator(spacing=SeparatorSpacing.large))

        is_valid = all([
            panel_config.title,
            panel_config.description
        ])

        container.add_item(
            ActionRow(
                PreviewWelcomeMessageButton(panel_id, disabled=not is_valid),
                BackToTypeConfigButton(panel_config.type_id, disabled=not is_valid)
            )
        )

        self.add_item(container)



class WelcomePanelPreview(LayoutView):
    def __init__(self, panel_id: int, interaction: Interaction):
        super().__init__(timeout=None)

        panel_config = WelcomePanelHandler(panel_id).get_panel()

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

        self.add_item(container)
