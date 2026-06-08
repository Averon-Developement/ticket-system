import time
from dataclasses import dataclass

from core.database import ensure_cursor, Cursor


@dataclass
class BlacklistUser:
    """Blacklisted user information"""
    guild_id: int
    user_id: int
    moderator_id: int
    reason: str | None
    created_at: int


class BlacklistHandler:
    """Manage the ticket blacklist for a guild"""
    def __init__(
        self,
        guild_id: int,
        *,
        user_id: int | None = None
    ):
        self.guild_id = guild_id
        self.user_id = user_id

    @ensure_cursor
    def set_blacklist(
        self,
        moderator_id: int,
        reason: str | None = None,
        *,
        cursor: Cursor
    ) -> None:
        """
        Add a user to the ticket blacklist.

        :param moderator_id: The Discord ID of the moderator.
        :param reason: The reason for the blacklist.        
        """
        if self.user_id is None:
            raise ValueError("user_id must be set")

        cursor.execute(
            """
            INSERT INTO tickets_blacklist (
                guild_id, user_id, moderator_id, reason, created_at
            ) VALUES (%s, %s, %s, %s, %s)
            ON DUPLICATE KEY UPDATE
                moderator_id=VALUES(moderator_id),
                reason=VALUES(reason),
                created_at=VALUES(created_at)
            """,
            (
                self.guild_id,
                self.user_id,
                moderator_id,
                reason,
                int(time.time())
            )
        )

    @ensure_cursor
    def remove_blacklist(
        self, *, cursor: Cursor=None
    ) -> bool:
        """
        Remove a user from the ticket blacklist.

        :return: Whether a blacklist entry was removed.
        """
        if self.user_id is None:
            raise ValueError("user_id must be set")

        cursor.execute(
            "DELETE FROM tickets_blacklist WHERE guild_id=%s AND user_id=%s",
            (self.guild_id, self.user_id)
        )

        return cursor.rowcount > 0
    
    @ensure_cursor
    def get_blacklisted_user(
        self, *, cursor: Cursor = None
    ) -> BlacklistUser | None:
        """
        Get a user's blacklist entry.

        :return: The blacklist entry, if found.        
        """
        cursor.execute(
            "SELECT * FROM tickets_blacklist WHERE guild_id=%s AND user_id=%s",
            (self.guild_id, self.user_id)
        )

        result = cursor.fetchone()

        return BlacklistUser(**result) if result else None
