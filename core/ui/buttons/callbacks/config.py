from discord import ButtonStyle

from core.ui.buttons import AppButton
from core.ui.modals import (
    SetAccentColorModal,
    SetTitleModal,
    SetDescriptionModal,
    SetThumbnailModal
)

from ..helpers import create_modal_button


def create_set_accent_color_button(
    panel_id: int,
    panel_type: str = "welcome"
) -> AppButton:
    return create_modal_button(
        label="Set Accent Color",
        style=ButtonStyle.primary,
        custom_id=f"accent_color_{panel_id}",
        data={
            "panel_id": panel_id,
            "panel_type": panel_type
        },
        modal_factory=lambda interaction, button:
            SetAccentColorModal(
                interaction,
                button.data["panel_id"],
                button.data["panel_type"]
            )
    )