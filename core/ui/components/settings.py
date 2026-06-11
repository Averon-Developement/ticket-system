from discord.ui import LayoutView, Container, Section, Separator, TextDisplay, ActionRow
from discord import Guild, SeparatorSpacing

from core.database.handlers import GuildSettingsHandler
from core.ui.dropdowns import TranscriptsChannelSelect

from core.ui.buttons.helpers import (
    create_max_tickets_button,
    create_toggle_transcripts_button,
    create_ticket_types_button,
    create_ticket_panel_button
)

class SettingsMenu(LayoutView):
    def __init__(self, guild: Guild):
        super().__init__(timeout=None)

        settings = GuildSettingsHandler(guild.id).get_settings()
        transcripts_channel = (
            guild.get_channel(settings.transcripts_channel) if settings.transcripts_channel else None
        )

        container = Container()
        container.add_item(
            TextDisplay(
                content=(
                    "## Configure ticket settings\n"
                    "Manage your ticket system settings, including ticket categories, support roles, "
                    "transcripts and other options that control how tickets are created and handled."
                )
            )
        )
        container.add_item(Separator(spacing=SeparatorSpacing.large))
        container.add_item(
            Section(
                TextDisplay(
                    f"**Max tickets:** `{settings.max_tickets}`\n"
                    "-# Set the maximum number of tickets a user can create per ticket type.\n"
                ),
                accessory=create_max_tickets_button()
            )
        )
        container.add_item(
            Section(
                TextDisplay(
                    f"**Transcripts:** {"`Enabled`" if settings.transcripts else "`Disabled`"}\n"
                    "-# Enable or disable ticket transcripts for closed tickets.\n"
                ),
                accessory=create_toggle_transcripts_button(
                    settings.transcripts
                )
            )
        )

        if settings.transcripts:
            container.add_item(
                TextDisplay(
                    f"**Transcripts Channel:** {transcripts_channel.mention if settings.transcripts_channel else "`Not set`"}\n"
                    "-# Configure the channel used to store ticket transcripts after a ticket is closed.\n"
                )
            )
            container.add_item(
                ActionRow(TranscriptsChannelSelect())
            )

        container.add_item(Separator(spacing=SeparatorSpacing.large))

        container.add_item(
            TextDisplay(
                "**Advanced Configuration**\n"
                "-# Manage ticket types and configure the ticket panel."
            )
        )
        container.add_item(
            ActionRow(
                create_ticket_types_button(),
                create_ticket_panel_button()
            )
        )

        self.add_item(container)