from discord import ButtonStyle, Interaction
from discord.ui import Button, View

from core.database.handlers import TicketPanelHandler
from core.ui.dropdowns import SendTicketPanelToChannelSelect


class NavigateTicketTypesButton(Button):
    def __init__(self) -> None:
        super().__init__(
            label="Ticket Types",
            style=ButtonStyle.primary,
            custom_id="ticket_types_button",
        )

    async def callback(self, interaction: Interaction) -> None:
        from core.ui.components import TicketTypesMenu

        await interaction.response.edit_message(
            view=TicketTypesMenu(interaction.guild)
        )


class NavigateTicketPanelButton(Button):
    def __init__(self) -> None:
        super().__init__(
            label="Ticket Panel",
            style=ButtonStyle.primary,
            custom_id="ticket_panel_button",
        )

    async def callback(self, interaction: Interaction) -> None:
        panel_config = TicketPanelHandler.get_panel_by_guild(interaction.guild.id)

        panel_id = (
            panel_config.panel_id if panel_config
            else TicketPanelHandler.create_panel(interaction.guild.id)
        )

        from core.ui.components import PanelMenu

        await interaction.response.edit_message(
            view=PanelMenu(panel_id)
        )        


class BackToSettingsButton(Button):
    def __init__(self, disabled: bool = False) -> None:
        super().__init__(
            label="Save & Go back",
            style=ButtonStyle.gray,
            custom_id="back_button",
            disabled=disabled
        )

    async def callback(self, interaction: Interaction) -> None:
        from core.ui.components import SettingsMenu

        await interaction.response.edit_message(
            view=SettingsMenu(interaction.guild)
        )


class BackToTicketTypesButton(Button):
    def __init__(self, disabled: bool) -> None:
        super().__init__(
            label="Save & Go back",
            style=ButtonStyle.green,
            custom_id="save_button",
            disabled=disabled
        )

    async def callback(self, interaction: Interaction) -> None:
        from core.ui.components import TicketTypesMenu

        await interaction.response.edit_message(
            view=TicketTypesMenu(interaction.guild)
        )

class BackToTypeConfigButton(Button):
    def __init__(self, type_id: int, disabled: bool) -> None:
        super().__init__(
            label="Save & Go back",
            style=ButtonStyle.green,
            custom_id="type_go_back_button",
            disabled=disabled
        )

        self.type_id = type_id

    async def callback(self, interaction: Interaction) -> None:
        from core.ui.components import TicketTypesConfigMenu

        await interaction.response.edit_message(
            view=TicketTypesConfigMenu(interaction.guild, self.type_id)
        )

class SendTicketPanelView(View):
    def __init__(self, panel_id: int):
        super().__init__(timeout=60)

        self.add_item(
            SendTicketPanelToChannelSelect(panel_id)
        )

class SendPanelToChannelButton(Button):
    def __init__(
        self,
        panel_id: int,
        disabled: bool = False
    ):
        super().__init__(
            label="Send panel",
            style=ButtonStyle.green,
            custom_id="send_panel_button",
            disabled=disabled
        )

        self.panel_id = panel_id

    async def callback(self, interaction: Interaction) -> None:
        await interaction.response.send_message(
            content="Select the channel where the ticket panel should be send to.",
            view=SendTicketPanelView(self.panel_id),
            ephemeral=True
        )