from urllib.parse import urlparse

from discord import Interaction, TextStyle
from discord.ui import Modal, TextInput

from core.database.handlers import WelcomePanelHandler


class SetAccentColorModal(Modal, title="Set Accent Color"):
    def __init__(
        self,
        org_interaction: Interaction,
        panel_id: int
    ):
        super().__init__()

        self.org_interaction = org_interaction
        self.panel_id = panel_id

    accent_color = TextInput(
        label="Set accent color",
        placeholder="e.g. #5865F2",
        max_length=7,
        min_length=6,
        required=True
    )

    async def on_submit(self, interaction: Interaction):
        await interaction.response.defer(ephemeral=True)

        panel_config = WelcomePanelHandler(self.panel_id)

        hex_color = self.accent_color.value.strip().lstrip("#")

        if len(hex_color) != 6:
            return await interaction.followup.send(
                content="Please provide a valid 6-digit hex color (e.g. #5865F2).",
                ephemeral=True
            )

        try:
            color = int(hex_color, 16)
        except ValueError:
            return await interaction.followup.send(
                content="Please provide a valid hex color (e.g. #5865F2).",
                ephemeral=True
            )

        panel_config.set_accent_color(color)

        from core.ui.components import WelcomePanelMenu

        await self.org_interaction.edit_original_response(
            view=WelcomePanelMenu(self.panel_id)
        )


class SetTitleModal(Modal, title="Set Panel Title"):
    def __init__(
        self,
        org_interaction: Interaction,
        panel_id: int
    ):
        super().__init__()

        self.org_interaction = org_interaction
        self.panel_id = panel_id

    panel_title = TextInput(
        label="Set title",
        placeholder="e.g. Welcome {user.mention}",
        max_length=256,
        min_length=1,
        required=True
    )

    async def on_submit(self, interaction: Interaction):
        await interaction.response.defer(ephemeral=True)

        panel_config = WelcomePanelHandler(self.panel_id)

        title = self.panel_title.value.strip()
        panel_config.set_title(title)

        from core.ui.components import WelcomePanelMenu

        await self.org_interaction.edit_original_response(
            view=WelcomePanelMenu(self.panel_id)
        )

class SetDescriptionModal(Modal, title="Set Description"):
    def __init__(
        self,
        org_interaction: Interaction,
        panel_id: int
    ):
        super().__init__()

        self.org_interaction = org_interaction
        self.panel_id = panel_id

    description = TextInput(
        label="Set description",
        placeholder=(
            "**Welcome {user.mention}**\n\n"
            "Thank you for creating a ticket."
        ),
        style=TextStyle.paragraph,
        max_length=4000,
        required=True
    )

    async def on_submit(self, interaction: Interaction):
        await interaction.response.defer(ephemeral=True)

        panel_handler = WelcomePanelHandler(
            self.panel_id
        )

        panel_handler.set_description(
            self.description.value.strip()
        )

        from core.ui.components import WelcomePanelMenu

        await self.org_interaction.edit_original_response(
            view=WelcomePanelMenu(
                self.panel_id
            )
        )

class SetThumbnailModal(Modal, title="Set Thumbnail"):
    def __init__(
        self,
        org_interaction: Interaction,
        panel_id: int
    ):
        super().__init__()

        self.org_interaction = org_interaction
        self.panel_id = panel_id

    thumbnail_url = TextInput(
        label="Set thumbnail",
        placeholder="e.g. {user.avatar} or https://example.com/image.png",
        max_length=512,
        required=True
    )

    async def on_submit(self, interaction: Interaction):
        await interaction.response.defer(ephemeral=True)

        value = self.thumbnail_url.value.strip()

        if value != "{user.avatar}":
            parsed = urlparse(value)

            if parsed.scheme not in ("http", "https") or not parsed.netloc:
                return await interaction.followup.send(
                    content=(
                        "Please provide a valid image URL or "
                        "`{user.avatar}`."
                    ),
                    ephemeral=True
                )

        WelcomePanelHandler(self.panel_id).set_thumbnail_url(value)

        from core.ui.components import WelcomePanelMenu

        await self.org_interaction.edit_original_response(
            view=WelcomePanelMenu(
                self.panel_id
            )
        )