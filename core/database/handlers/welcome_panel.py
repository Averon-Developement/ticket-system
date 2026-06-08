from dataclasses import dataclass

from core.database import ensure_cursor, Cursor


@dataclass
class WelcomePanel:
    """Welcome panel configuration"""
    panel_id: int
    guild_id: int
    accent_color: int | None
    title: str | None
    description: str | None
    thumbnail_url: str | None


class WelcomePanelHandler:
    """Manage welcome panel configuration"""
    def __init__(self, panel_id: int):
        self.panel_id = panel_id

    @staticmethod
    @ensure_cursor
    def create_panel(
        guild_id: int, *, cursor: Cursor = None
    ) -> int:
        """
        Create a welcome panel.

        :param guild_id: The Discord guild ID.
        :return: The ID of the created panel.
        """
        cursor.execute(
            """
            INSERT INTO welcome_panels (guild_id)
            VALUES (%s)
            """,
            (guild_id,)
        )

        return cursor.lastrowid

    @ensure_cursor
    def set_accent_color(
        self,
        accent_color: int | None,
        *,
        cursor: Cursor = None
    ) -> None:
        """
        Set the panel accent color.

        :param accent_color: The panel accent color.
        """
        cursor.execute(
            """
            UPDATE welcome_panels SET accent_color=%s
            WHERE panel_id=%s
            """,
            (accent_color, self.panel_id)
        )

    @ensure_cursor
    def set_title(
        self,
        title: str | None,
        *,
        cursor: Cursor = None
    ) -> None:
        """
        Set the panel title.

        :param title: The panel title.
        """
        cursor.execute(
            """
            UPDATE welcome_panels SET title=%s
            WHERE panel_id=%s
            """,
            (title, self.panel_id)
        )

    @ensure_cursor
    def set_description(
        self,
        description: str | None,
        *,
        cursor: Cursor = None
    ) -> None:
        """
        Set the panel description.

        :param description: The panel description.
        """
        cursor.execute(
            """
            UPDATE welcome_panels SET description=%s
            WHERE panel_id=%s
            """,
            (description, self.panel_id)
        )

    @ensure_cursor
    def set_thumbnail_url(
        self,
        thumbnail_url: str | None,
        *,
        cursor: Cursor = None
    ) -> None:
        """
        Set the panel thumbnail URL.

        :param thumbnail_url: The panel thumbnail URL.
        """
        cursor.execute(
            """
            UPDATE welcome_panels SET thumbnail_url=%s
            WHERE panel_id=%s
            """,
            (thumbnail_url, self.panel_id)
        )

    @ensure_cursor
    def get_panel(
        self,
        *,
        cursor: Cursor = None
    ) -> WelcomePanel | None:
        """
        Get a welcome panel.

        :return: The panel configuration, if found.
        """
        cursor.execute(
            "SELECT * FROM welcome_panels WHERE panel_id=%s",
            (self.panel_id,)
        )

        result = cursor.fetchone()

        return WelcomePanel(**result) if result else None