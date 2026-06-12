import time
from dataclasses import dataclass

from core.database import ensure_cursor, Cursor


@dataclass
class Ticket:
    """Ticket information"""
    ticket_id: int
    guild_id: int
    type_id: int | None
    channel_id: int
    creator_id: int
    claimed_by: int | None
    claimed_at: int | None
    status: int
    created_at: int | None
    closed_by: int | None
    closed_at: int | None
    renamed_at: int | None

class TicketHandler:
    """Manage ticket data"""
    def __init__(self, ticket_id: int):
        self.ticket_id = ticket_id

    @staticmethod
    @ensure_cursor
    def create_ticket(
        guild_id: int,
        type_id: int,
        channel_id: int,
        creator_id: int,
        created_at: int,
        *,
        cursor: Cursor = None
    ) -> int:
        """
        Create a ticket.

        :param guild_id: The Discord guild ID.
        :param type_id: The ticket type ID.
        :param channel_id: The ticket channel ID.
        :param creator_id: The Discord ID of the ticket creator.
        :param created_at: The ticket creation timestamp.
        :return: The ID of the created ticket.
        """
        cursor.execute(
            """
            INSERT INTO tickets (
                guild_id,
                type_id,
                channel_id,
                creator_id,
                created_at
            )
            VALUES (%s, %s, %s, %s, %s)
            """,
            (
                guild_id,
                type_id,
                channel_id,
                creator_id,
                created_at
            )
        )

        return cursor.lastrowid
      
    @ensure_cursor
    def set_claim(
        self,
        user_id: int | None,
        claimed_at: int | None,
        *,
        cursor: Cursor = None
    ) -> None:
        """
        Set the ticket claim information.

        :param user_id: The Discord ID of the claiming user, or ``None`` to remove the claim.
        :param claimed_at: The claim timestamp, or ``None`` if the ticket is not claimed.
        """
        cursor.execute(
            """
            UPDATE tickets
            SET claimed_by=%s,
                claimed_at=%s
            WHERE ticket_id=%s
            """,
            (
                user_id,
                claimed_at,
                self.ticket_id
            )
        )

    @ensure_cursor
    def set_status(
        self,
        status: int,
        *,
        cursor: Cursor = None
    ) -> None:
        """
        Set the ticket status.

        :param status: The ticket status.
        """
        cursor.execute(
            "UPDATE tickets SET status=%s WHERE ticket_id=%s",
            (status, self.ticket_id)
        )

    @ensure_cursor
    def close_ticket(
        self,
        closed_by: int,
        *,
        cursor: Cursor = None
    ) -> None:
        """
        Close a ticket.

        :param closed_by: The Discord ID of the user closing the ticket.
        """
        cursor.execute(
            """
            UPDATE tickets
            SET closed_by=%s,
                closed_at=%s
            WHERE ticket_id=%s
            """,
            (
                closed_by,
                int(time.time()),
                self.ticket_id
            )
        )

    @ensure_cursor
    def set_renamed_at(
        self,
        timestamp: int,
        *,
        cursor: Cursor = None
    ) -> None:
        cursor.execute(
            """
            UPDATE tickets
            SET renamed_at=%s
            WHERE ticket_id=%s
            """,
            (
                timestamp,
                self.ticket_id
            )
        )

    @ensure_cursor
    def get_ticket(
        self,
        *,
        cursor: Cursor = None
    ) -> Ticket | None:
        """
        Get a ticket.

        :return: The ticket, if found.        
        """
        cursor.execute(
            "SELECT * FROM tickets WHERE ticket_id=%s",
            (self.ticket_id,)
        )

        result = cursor.fetchone()

        return Ticket(**result) if result else None
    
    @staticmethod
    @ensure_cursor
    def get_by_channel(
        channel_id: int,
        *,
        cursor: Cursor = None
    ) -> Ticket | None:
        """
        Get a ticket by its channel.

        :param channel_id: The ticket channel ID.
        :return: The ticket, if found.        
        """
        cursor.execute(
            "SELECT * FROM tickets WHERE channel_id=%s",
            (channel_id,)
        )

        result = cursor.fetchone()

        return Ticket(**result) if result else None
    
    @staticmethod
    @ensure_cursor
    def get_open_by_type_and_creator(
        guild_id: int,
        type_id: int,
        creator_id: int,
        *,
        cursor: Cursor = None
    ) -> Ticket | None:
        """
        Get an open ticket of a specific type created by a user.

        :param guild_id: The Discord guild ID.
        :param type_id: The ticket type ID.
        :param creator_id: The Discord ID of the ticket creator.
        :return: The ticket, if found.
        """
        cursor.execute(
            """
            SELECT *
            FROM tickets
            WHERE guild_id=%s
            AND type_id=%s
            AND creator_id=%s
            AND status=0
            LIMIT 1
            """,
            (
                guild_id,
                type_id,
                creator_id
            )
        )

        result = cursor.fetchone()

        return Ticket(**result) if result else None
    
    @staticmethod
    @ensure_cursor
    def get_open_by_creator(
        guild_id: int,
        creator_id: int,
        *,
        cursor: Cursor = None
    ) -> list[Ticket]:
        cursor.execute(
            """
            SELECT *
            FROM tickets
            WHERE guild_id=%s
            AND creator_id=%s
            AND status=0
            ORDER BY created_at
            """,
            (
                guild_id,
                creator_id
            )
        )

        return [
            Ticket(**row)
            for row in cursor.fetchall()
        ]