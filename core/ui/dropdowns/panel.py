from discord.ui import ChannelSelect
from discord import Interaction, ChannelType, Embed

from core import colors


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
        if not channel:
            channel = await interaction.guild.fetch_channel(selected.id)

        permissions = channel.permissions_for(interaction.guild.me)

        if not permissions.send_messages:
            return await interaction.response.edit_message(
                embed=Embed(
                    description=(
                        "I do not have permission to send messages in this channel.\n"
                        "- Missing permissions: `Send Messages`"
                    ),
                    color=colors.red
                ),
                view=None, content=None
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
            embed=Embed(
                description=f"Ticket panel sent to {channel.mention}.",
                color=colors.green
            ),
            view=None, content=None
        )