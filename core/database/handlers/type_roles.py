from dataclasses import dataclass

from core.database import ensure_cursor, Cursor


@dataclass
class TicketTypeRole:
    """Support role configuration for a ticket type"""
    type_id: int
    role_id: int


class TicketTypeRoleHandler:
    """Manage support roles for a ticket type"""
    def __init__(self, type_id: int):
        self.type_id = type_id

    @ensure_cursor
    def set_roles(
        self,
        role_ids: list[int],
        *,
        cursor: Cursor = None
    ) -> None:
        """
        Set the support roles for a ticket type.

        :param role_ids: The role IDs to notify when a ticket is created.
        """
        cursor.execute(
            "DELETE FROM ticket_type_roles WHERE type_id=%s",
            (self.type_id,)
        )

        if not role_ids:
            return

        cursor.executemany(
            """
            INSERT INTO ticket_type_roles (type_id, role_id)
            VALUES (%s, %s)
            """,
            [(self.type_id, role_id)for role_id in role_ids]
        )

    @ensure_cursor
    def get_roles(
        self,
        *,
        cursor: Cursor = None
    ) -> list[TicketTypeRole]:
        """
        Get the support roles for a ticket type.

        :return: A list of configured support roles.
        """
        cursor.execute(
            "SELECT * FROM ticket_type_roles WHERE type_id=%s",
            (self.type_id,)
        )

        return [TicketTypeRole(**row) for row in cursor.fetchall()]