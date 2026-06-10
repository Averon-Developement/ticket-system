from discord.ui import ChannelSelect
from discord import Interaction, ChannelType

from core.database.handlers import GuildSettingsHandler


class TranscriptsChannelSelect(ChannelSelect):
    def __init__(self):
        super().__init__(
            placeholder="Select transcripts channel",
            min_values=1,
            max_values=1,
            channel_types=[ChannelType.text]
        )

    async def callback(self, interaction: Interaction):
        channel = self.values[0]

        GuildSettingsHandler(interaction.guild.id).set_transcripts_channel(channel.id)

        from core.ui.components import SettingsMenu

        await interaction.response.edit_message(
            view=SettingsMenu(interaction.guild)
        )