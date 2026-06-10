from discord.ui import ChannelSelect
from discord import Interaction, ChannelType, TextChannel

from core.database.handlers import GuildSettingsHandler


class SendTicketPanelToChannelSelect(ChannelSelect):
    def __init__(self, panel_id: int):
        super().__init__(
            placeholder="Select a channel",
            min_values=1,
            max_values=1,
            channel_types=[ChannelType.text]
        )

        self.panel_id = panel_id

    async def callback(self, interaction: Interaction):
        selected = self.values[0]

        channel = interaction.guild.get_channel(selected.id)

        if channel is None:
            return await interaction.response.edit_message(
                content="Unable to find that channel.",
                view=None
            )

        permissions = channel.permissions_for(interaction.guild.me)

        if not permissions.send_messages:
            return await interaction.response.edit_message(
                content=f"I can't send messages in {channel.mention}.",
                view=None
            )

        from core.ui.components import TicketPanel

        await channel.send(
            view=TicketPanel(
                self.panel_id,
                interaction,
                preview=False
            )
        )

        await interaction.response.edit_message(
            content=f"Successfully sent the ticket panel to {channel.mention}.",
            view=None
        )