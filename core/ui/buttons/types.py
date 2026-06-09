from discord import ButtonStyle, Interaction
from discord.ui import Button

from core.database.handlers import TicketTypeHandler
from core.ui.modals import SetTypeNameModal, SetTypeEmojiModal


class CreateTicketTypeButton(Button):
    def __init__(self) -> None:
        super().__init__(
            label="Create New Type",
            style=ButtonStyle.success,
            custom_id="create_type_button",
        )

    async def callback(self, interaction: Interaction) -> None:
        total_types = TicketTypeHandler.get_total_types(interaction.guild.id)

        if total_types == 3:
            return await interaction.response.send_message(
                content="Ticket type limit reached. A maximum of 3 ticket types can be created.",
                ephemeral=True
            )
        
        type_id = TicketTypeHandler.create_ticket_type(interaction.guild.id)
        if not type_id:
            return await interaction.response.send_message(
                content="Failed to create the ticket type. If this issue persists, please contact our support.",
                ephemeral=True
            )
        
        from core.ui.components import TicketTypesConfigMenu

        await interaction.response.edit_message(
            view=TicketTypesConfigMenu(interaction.guild, type_id)
        )


class TicketTypeEditButton(Button):
    def __init__(self, type_id: int) -> None:
        super().__init__(
            label="Edit",
            style=ButtonStyle.primary,
            custom_id=f"edit_type_{type_id}",
        )

        self.type_id = type_id

    async def callback(self, interaction: Interaction) -> None:
        from core.ui.components import TicketTypesConfigMenu
        await interaction.response.edit_message(
            view=TicketTypesConfigMenu(interaction.guild, self.type_id)
        )


class TicketTypeDeleteButton(Button):
    def __init__(self, type_id: int) -> None:
        super().__init__(
            label="Delete",
            style=ButtonStyle.red,
            custom_id=f"delete_type_{type_id}",
        )

        self.type_id = type_id

    async def callback(self, interaction: Interaction) -> None:
        await interaction.response.send_message(
            content="Callback logic not implemented yet", ephemeral=True
        )


class SetTypeNameButton(Button):
    def __init__(self, type_id: int) -> None:
        super().__init__(
            label="Set Name",
            style=ButtonStyle.blurple,
            custom_id=f"type_{type_id}_name",
        )

        self.type_id = type_id

    async def callback(self, interaction: Interaction) -> None:
        await interaction.response.send_modal(
            SetTypeNameModal(interaction, self.type_id)
        )


class SetTypeEmojiButton(Button):
    def __init__(self, type_id: int) -> None:
        super().__init__(
            label="Set Emoji",
            style=ButtonStyle.blurple,
            custom_id=f"type_{type_id}_emoji",
        )

        self.type_id = type_id

    async def callback(self, interaction: Interaction) -> None:
        await interaction.response.send_modal(
            SetTypeEmojiModal(interaction, self.type_id)
        )    


