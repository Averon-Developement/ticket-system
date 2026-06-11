from discord import ButtonStyle

from core.ui.buttons import AppButton
from ..callbacks import preview_panel, preview_welcome_message


def create_preview_panel_button(
    panel_id: int,
    disabled: bool
) -> AppButton:
    return AppButton(
        label="Preview Panel",
        style=ButtonStyle.blurple,
        custom_id=f"preview_{panel_id}",
        disabled=disabled,
        data={
            "panel_id": panel_id
        },
        callback_func=preview_panel
    )

def create_preview_welcome_message_button(
    panel_id: int,
    disabled: bool
) -> AppButton:
    return AppButton(
        label="Preview Panel",
        style=ButtonStyle.blurple,
        custom_id=f"preview_{panel_id}",
        disabled=disabled,
        data={
            "panel_id": panel_id
        },
        callback_func=preview_welcome_message
    )