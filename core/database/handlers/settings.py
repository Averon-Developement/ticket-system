from dataclasses import dataclass

from core.database import ensure_cursor, Cursor


@dataclass
class GuildSettings:
    """Ticket settings for a guild"""
    guild_id: int
    max_tickets: int
    transcripts: bool
    transcripts_channel: int


class GuildSettingsHandler:
    """Manage ticket settings for a guild"""
    def __init__(self, guild_id: int):
        self.guild_id = guild_id

    @ensure_cursor
    def set_max_tickets(
        self,
        max_tickets: int,
        *, cursor: Cursor=None
    ) -> None:
        """
        Set the maximum number of open tickets per user.

        :param max_tickets: The maximum number of open tickets a user can have.
        """
        cursor.execute(
            """
            INSERT INTO guild_settings (guild_id, max_tickets)
            VALUES (%s, %s)
            ON DUPLICATE KEY UPDATE
                max_tickets=VALUES(max_tickets)
            """,
            (self.guild_id, max_tickets)
        )

    @ensure_cursor
    def set_transcripts(
        self, 
        enabled: bool,
        *,
        cursor: Cursor=None
    ) -> None:
        """
        Enable or disable ticket transcripts.

        :param enabled: Whether ticket transcripts are enabled.
        """
        cursor.execute(
            """
            INSERT INTO guild_settings (guild_id, transcripts)
            VALUES (%s, %s)
            ON DUPLICATE KEY UPDATE
                transcripts=VALUES(transcripts)
            """,
            (self.guild_id, enabled)
        )

    @ensure_cursor
    def set_transcripts_channel(
        self, 
        channel_id: int,
        *,
        cursor: Cursor=None
    ) -> None:
        """
        Set the transcript channel.

        :param channel_id: The ID of the channel used for ticket transcripts.        
        """
        cursor.execute(
            """
            INSERT INTO guild_settings (guild_id, transcripts_channel)
            VALUES (%s, %s)
            ON DUPLICATE KEY UPDATE
                transcripts_channel=VALUES(transcripts_channel)
            """,
            (self.guild_id, channel_id)
        )

    @ensure_cursor
    def get_settings(self, *, cursor: Cursor=None) -> GuildSettings:
        """
        Get the guild's ticket settings.
        Creates default settings if none exist.

        :return: The guild settings.
        """
        cursor.execute(
            "SELECT * FROM guild_settings WHERE guild_id=%s",
            (self.guild_id)
        )

        result = cursor.fetchone()

        if not result:
            cursor.execute(
                "INSERT INTO guild_settings (guild_id) VALUES (%s)",
                (self.guild_id)
            )
        
            return GuildSettings(
                guild_id=self.guild_id,
                max_tickets=1,
                transcripts=False,
                transcripts_channel=None
            )
    
        return GuildSettings(**result)
            
