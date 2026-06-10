from dataclasses import dataclass

from core.database import ensure_cursor, Cursor


@dataclass
class TicketType:
    """Ticket type configuration"""
    type_id: int
    guild_id: int
    name: str
    emoji: str | None
    button_style: int
    category_id: int


class TicketTypeHandler:
    """Manage ticket type configuration"""
    def __init__(self, type_id: int):
        self.type_id = type_id

    @staticmethod
    @ensure_cursor
    def create_ticket_type(
        guild_id: int, *, cursor: Cursor = None
    ) -> int:
        """
        Create a ticket type.

        :param guild_id: The Discord guild ID.
        :return: The created ticket type ID.
        """
        cursor.execute(
            """
            INSERT INTO ticket_types (guild_id)
            VALUES (%s)
            """,
            (guild_id,)
        )

        return cursor.lastrowid    

    @staticmethod
    @ensure_cursor
    def get_all_types(
        *, cursor: Cursor = None
    ) -> list[TicketType]:
        """
        Get all ticket types.

        :return: A list of all ticket types.
        """
        cursor.execute(
            """
            SELECT * FROM ticket_types
            ORDER BY guild_id, type_id
            """
        )

        results = cursor.fetchall()

        return [TicketType(**row) for row in results]

    @ensure_cursor
    def set_name(
        self, name: str, *, cursor: Cursor = None
    ) -> None:
        """
        Set the ticket type name.

        :param name: The new ticket type name        
        """
        cursor.execute(
            """
            UPDATE ticket_types SET name=%s
            WHERE type_id=%s
            """,
            (name, self.type_id)
        )

    @ensure_cursor
    def set_emoji(
        self, emoji: str | None, *, cursor: Cursor = None
    ) -> None:
        """
        Set the ticket type emoji.

        :param emoji: The emoji displayed on the ticket button.
        """
        cursor.execute(
            """
            UPDATE ticket_types SET emoji=%s
            WHERE type_id=%s
            """,
            (emoji, self.type_id)
        )

    @ensure_cursor
    def set_button_style(
        self, style: int, *, cursor: Cursor = None
    ) -> None:
        """ 
        Set the ticket button style.

        :param style: The Discord button style.
        """
        cursor.execute(
            """
            UPDATE ticket_types SET button_style=%s
            WHERE type_id=%s
            """,
            (style, self.type_id)
        )

    @ensure_cursor
    def set_category_id(
        self, category_id: int, *, cursor: Cursor = None
    ) -> None:
        """
        Set the ticket category.

        :param category_id: The category used for created tickets.        
        """
        cursor.execute(
            """
            UPDATE ticket_types SET category_id=%s
            WHERE type_id=%s
            """,
            (category_id, self.type_id)
        )

    @ensure_cursor
    def get_type(
        self,
        *,
        cursor: Cursor = None
    ) -> TicketType | None:
        """
        Get a ticket type.

        :return: The ticket type, if found.
        """
        cursor.execute(
            "SELECT * FROM ticket_types WHERE type_id=%s",
            (self.type_id,)
        )

        result = cursor.fetchone()

        return TicketType(**result) if result else None
    
    @staticmethod
    @ensure_cursor
    def get_guild_types(
        guild_id: int, *, cursor: Cursor = None
    ) -> list[TicketType]:
        """
        Get all ticket types for a guild.

        :param guild_id: The Discord guild ID.
        :return: A list of ticket types.
        """
        cursor.execute(
            """
            SELECT * FROM ticket_types WHERE guild_id=%s
            ORDER BY type_id
            """,
            (guild_id,)
        )

        results = cursor.fetchall()

        return [TicketType(**row) for row in results]
    
    @staticmethod
    @ensure_cursor
    def get_total_types(
        guild_id: int, *, cursor: Cursor = None
    ) -> int:
        """
        Get the total number of ticket types for a guild.

        :param guild_id: The Discord guild ID.
        :return: The total amount of ticket types.
        """
        cursor.execute(
            "SELECT COUNT(*) AS total FROM ticket_types WHERE guild_id=%s",
            (guild_id,)
        )

        result = cursor.fetchone()

        return int(result["total"])