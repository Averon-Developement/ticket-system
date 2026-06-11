from urllib.parse import urlparse

from discord import Interaction, TextStyle
from discord.ui import Modal, TextInput

from core.database.handlers import WelcomePanelHandler, TicketPanelHandler


class BasePanelModal(Modal):
    def __init__(
        self,
        org_interaction: Interaction,
        panel_id: int,
        panel_type: str
    ):
        super().__init__()

        self.org_interaction = org_interaction
        self.panel_id = panel_id
        self.panel_type = panel_type

    @property
    def handler(self):
        if self.panel_type == "welcome":
            return WelcomePanelHandler(self.panel_id)

        return TicketPanelHandler(self.panel_id)

    @property
    def menu(self):
        if self.panel_type == "welcome":
            from core.ui.components import WelcomePanelMenu
            return WelcomePanelMenu(self.panel_id)

        from core.ui.components import PanelMenu
        return PanelMenu(self.panel_id)

    async def refresh(self):
        await self.org_interaction.edit_original_response(
            view=self.menu
        )


class SetAccentColorModal(BasePanelModal, title="Set Accent Color"):
    accent_color = TextInput(
        label="Set accent color",
        placeholder="e.g. #5865F2",
        max_length=7,
        min_length=0,
        required=False
    )

    async def on_submit(self, interaction: Interaction):
        await interaction.response.defer(ephemeral=True)

        value = self.accent_color.value.strip()

        if not value:
            self.handler.set_accent_color(None)

            return await self.refresh()

        hex_color = value.lstrip("#")

        try:
            if len(hex_color) != 6:
                raise ValueError

            color = int(hex_color, 16)

        except ValueError:
            return await interaction.followup.send(
                content="Please provide a valid hex color (e.g. #5865F2).",
                ephemeral=True
            )

        self.handler.set_accent_color(color)

        await self.refresh()


class SetTitleModal(BasePanelModal, title="Set Panel Title"):
    panel_title = TextInput(
        label="Set title",
        placeholder="e.g. Welcome {user.mention}",
        max_length=256,
        min_length=1,
        required=True
    )

    async def on_submit(self, interaction: Interaction):
        await interaction.response.defer(ephemeral=True)

        self.handler.set_title(
            self.panel_title.value.strip()
        )

        await self.refresh()


class SetDescriptionModal(BasePanelModal, title="Set Description"):
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

        self.handler.set_description(
            self.description.value.strip()
        )

        await self.refresh()


class SetThumbnailModal(BasePanelModal, title="Set Thumbnail"):
    thumbnail_url = TextInput(
        label="Set thumbnail",
        placeholder="e.g. {user.avatar} or https://example.com/image.png",
        max_length=512,
        required=False
    )

    async def on_submit(self, interaction: Interaction):
        await interaction.response.defer(ephemeral=True)

        value = self.thumbnail_url.value.strip()

        if not value:
            self.handler.set_thumbnail_url(None)
            return await self.refresh()

        if value != "{user.avatar}":
            parsed = urlparse(value)

            if parsed.scheme not in {"http", "https"} or not parsed.netloc:
                return await interaction.followup.send(
                    content=(
                        "Please provide a valid image URL or "
                        "`{user.avatar}`."
                    ),
                    ephemeral=True
                )

        self.handler.set_thumbnail_url(value)

        await self.refresh()
