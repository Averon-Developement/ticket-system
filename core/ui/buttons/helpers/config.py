from discord import ButtonStyle

from core.ui.buttons import AppButton
from core.ui.modals import (
    SetAccentColorModal,
    SetTitleModal,
    SetDescriptionModal,
    SetThumbnailModal
)

from ..helpers import create_modal_button


def create_panel_modal_button(
    *,
    label: str,
    custom_id_prefix: str,
    modal_class,
    panel_id: int,
    panel_type: str = "welcome"
) -> AppButton:
    return create_modal_button(
        label=label,
        style=ButtonStyle.primary,
        custom_id=f"{custom_id_prefix}_{panel_id}",
        data={
            "panel_id": panel_id,
            "panel_type": panel_type
        },
        modal_factory=lambda interaction, button:
            modal_class(
                interaction,
                button.data["panel_id"],
                button.data["panel_type"]
            )
    )

def create_set_accent_color_button(
    panel_id: int,
    panel_type: str = "welcome"
) -> AppButton:
    return create_panel_modal_button(
        label="Set Accent Color",
        custom_id_prefix="accent_color",
        modal_class=SetAccentColorModal,
        panel_id=panel_id,
        panel_type=panel_type
    )

def create_set_title_button(
    panel_id: int,
    panel_type: str = "welcome"
) -> AppButton:
    return create_panel_modal_button(
        label="Set Title",
        custom_id_prefix="title",
        modal_class=SetTitleModal,
        panel_id=panel_id,
        panel_type=panel_type
    )

def create_set_description_button(
    panel_id: int,
    panel_type: str = "welcome"
) -> AppButton:
    return create_panel_modal_button(
        label="Set Description",
        custom_id_prefix="description",
        modal_class=SetDescriptionModal,
        panel_id=panel_id,
        panel_type=panel_type
    )

def create_set_thumbnail_button(
    panel_id: int,
    panel_type: str = "welcome"
) -> AppButton:
    return create_panel_modal_button(
        label="Set Thumbnail",
        custom_id_prefix="thumbnail",
        modal_class=SetThumbnailModal,
        panel_id=panel_id,
        panel_type=panel_type
    )