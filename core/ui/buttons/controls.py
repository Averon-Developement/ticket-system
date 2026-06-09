from discord import ButtonStyle, Interaction
from discord.ui import Button



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
        await interaction.response.send_message(
            content="Worked", ephemeral=True
        )


class BackToSettingsButton(Button):
    def __init__(self) -> None:
        super().__init__(
            label="Back",
            style=ButtonStyle.gray,
            custom_id="back_button",
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