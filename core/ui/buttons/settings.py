from discord import ButtonStyle, Interaction
from discord.ui import Button

from core.ui.modals import SetMaxTicketsModal
from core.database.handlers import GuildSettingsHandler


class SetMaxTicketsButton(Button):
    def __init__(self) -> None:
        super().__init__(
            label="Set Max Tickets",
            style=ButtonStyle.primary,
            custom_id="max_tickets_button",
        )

    async def callback(self, interaction: Interaction) -> None:
        await interaction.response.send_modal(
            SetMaxTicketsModal(interaction)
        )


class SetTranscriptsButton(Button):
    def __init__(self, enabled: bool) -> None:
        super().__init__(
            label="Disable" if enabled else "Enable",
            style=ButtonStyle.danger if enabled else ButtonStyle.success,
            custom_id="transcripts_button",
        )

        self.enabled = enabled

    async def callback(self, interaction: Interaction) -> None:
        new_state = not self.enabled

        GuildSettingsHandler(interaction.guild.id).set_transcripts(new_state)
        
        from core.ui.components import SettingsMenu

        await interaction.response.edit_message(
            view=SettingsMenu(interaction.guild)
        )
    
        
