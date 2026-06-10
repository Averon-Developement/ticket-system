from discord import ButtonStyle, Interaction
from discord.ui import Button

from core.database.handlers import WelcomePanelHandler
from core.ui.modals import SetAccentColorModal, SetTitleModal, SetDescriptionModal, SetThumbnailModal


class ConfigureWelcomePanelButton(Button):
    def __init__(
        self,
        type_id: int | None
    ) -> None:
        super().__init__(
            label="Configure Welcome Panel",
            style=ButtonStyle.blurple,
            custom_id="wlc_panel_button",
        )

        self.type_id = type_id

    async def callback(self, interaction: Interaction) -> None:        
        panel_config = WelcomePanelHandler.get_panel_by_type(self.type_id)

        panel_id = (
            panel_config.panel_id if panel_config
            else WelcomePanelHandler.create_panel(
                interaction.guild.id, self.type_id
            )
        )

        from core.ui.components import WelcomePanelMenu

        await interaction.response.edit_message(
            view=WelcomePanelMenu(panel_id)
        )


class SetAccentColorButton(Button):
    def __init__(
        self,
        panel_id: int,
        panel_type: str = "welcome"
    ) -> None:
        super().__init__(
            label="Set Accent Color",
            style=ButtonStyle.primary,
            custom_id=f"accent_color_{panel_id}",
        )

        self.panel_id = panel_id
        self.panel_type = panel_type

    async def callback(self, interaction: Interaction) -> None:
        await interaction.response.send_modal(
            SetAccentColorModal(interaction, self.panel_id, self.panel_type)
        )

class SetTitleButton(Button):
    def __init__(
        self,
        panel_id: int,
        panel_type: str = "welcome"
    ) -> None:
        super().__init__(
            label="Set Title",
            style=ButtonStyle.primary,
            custom_id=f"title_{panel_id}",
        )

        self.panel_id = panel_id
        self.panel_type = panel_type

    async def callback(self, interaction: Interaction) -> None:
        await interaction.response.send_modal(
            SetTitleModal(interaction, self.panel_id, self.panel_type)
        )

class SetDescriptionButton(Button):
    def __init__(
        self,
        panel_id: int,
        panel_type: str = "welcome"
    ) -> None:
        super().__init__(
            label="Set Description",
            style=ButtonStyle.primary,
            custom_id=f"description_{panel_id}",
        )

        self.panel_id = panel_id
        self.panel_type = panel_type

    async def callback(self, interaction: Interaction) -> None:
        await interaction.response.send_modal(
            SetDescriptionModal(interaction, self.panel_id, self.panel_type)
        )

class SetThumbnailButton(Button):
    def __init__(
        self,
        panel_id: int,
        panel_type: str = "welcome"
    ) -> None:
        super().__init__(
            label="Set Thumbnail",
            style=ButtonStyle.primary,
            custom_id=f"thumbnail_{panel_id}",
        )

        self.panel_id = panel_id
        self.panel_type = panel_type

    async def callback(self, interaction: Interaction) -> None:
        await interaction.response.send_modal(
            SetThumbnailModal(interaction, self.panel_id, self.panel_type)
        )


class PreviewWelcomeMessageButton(Button):
    def __init__(self, panel_id: int, disabled: bool) -> None:
        super().__init__(
            label="Preview",
            style=ButtonStyle.blurple,
            custom_id=f"preview_{panel_id}",
            disabled=disabled
        )

        self.panel_id = panel_id

    async def callback(self, interaction: Interaction) -> None:
        from core.ui.components import WelcomePanelPreview

        await interaction.response.send_message(
            view=WelcomePanelPreview(self.panel_id, interaction),
            ephemeral=True
        )


class PreviewPanelButton(Button):
    def __init__(
        self,
        panel_id: int,
        disabled: bool
    ) -> None:
        super().__init__(
            label="Preview",
            style=ButtonStyle.blurple,
            custom_id=f"preview_{panel_id}",
            disabled=disabled
        )

        self.panel_id = panel_id

    async def callback(self, interaction: Interaction) -> None:
        from core.ui.components import TicketPanel

        await interaction.response.send_message(
            view=TicketPanel(self.panel_id, interaction, preview=True),
            ephemeral=True
        )



