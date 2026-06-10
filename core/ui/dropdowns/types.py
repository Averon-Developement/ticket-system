from discord import Interaction, SelectOption, ChannelType
from discord.ui import Select, ChannelSelect, RoleSelect

from core.database.handlers import TicketTypeHandler, TicketTypeRoleHandler


class ButtonStyleSelect(Select):
    def __init__(self, type_id: int):
        self.type_id = type_id

        super().__init__(
            placeholder="Select button color",
            min_values=1,
            max_values=1,
            options=[
                SelectOption(label="Blurple", value="1"),
                SelectOption(label="Gray", value="2"),
                SelectOption(label="Green", value="3"),
                SelectOption(label="Red", value="4"),
            ]
        )

    async def callback(self, interaction: Interaction):
        style = int(self.values[0])

        TicketTypeHandler(self.type_id).set_button_style(style)

        from core.ui.components import TicketTypesConfigMenu

        await interaction.response.edit_message(
            view=TicketTypesConfigMenu(interaction.guild, self.type_id)
        )        


class TicketCategorySelect(ChannelSelect):
    def __init__(self, type_id: int):
        self.type_id = type_id

        super().__init__(
            placeholder="Select ticket category",
            min_values=1,
            max_values=1,
            channel_types=[ChannelType.category]
        )

    async def callback(self, interaction: Interaction):
        category = self.values[0]

        TicketTypeHandler(self.type_id).set_category_id(category.id)

        from core.ui.components import TicketTypesConfigMenu

        await interaction.response.edit_message(
            view=TicketTypesConfigMenu(
                interaction.guild,
                self.type_id
            )
        )


class TicketSupportRolesSelect(RoleSelect):
    def __init__(self, type_id: int):
        self.type_id = type_id

        super().__init__(
            placeholder="Select support roles",
            min_values=1,
            max_values=3
        )

    async def callback(self, interaction: Interaction):
        role_ids = [role.id for role in self.values]

        TicketTypeRoleHandler(self.type_id).set_roles(role_ids)

        from core.ui.components import TicketTypesConfigMenu

        await interaction.response.edit_message(
            view=TicketTypesConfigMenu(interaction.guild, self.type_id)
        )