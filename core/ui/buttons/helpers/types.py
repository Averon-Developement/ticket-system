from discord import ButtonStyle

from core.ui.buttons import AppButton
from core.ui.modals import SetTypeNameModal, SetTypeEmojiModal, SetTypeButtonNameModal
from ..helpers import create_modal_button

from ..callbacks import (
    create_ticket_type,
    edit_ticket_type,
    delete_ticket_type
)


def create_ticket_type_button() -> AppButton:
    return AppButton(
        label="Create New Type",
        style=ButtonStyle.blurple,
        custom_id="create_type_button",
        callback_func=create_ticket_type
    )

def create_ticket_type_edit_button(
    type_id: int
) -> AppButton:
    return AppButton(
        label="Edit",
        style=ButtonStyle.primary,
        custom_id=f"edit_type_{type_id}",
        data={"type_id": type_id},
        callback_func=edit_ticket_type
    )

def create_ticket_type_delete_button(
    type_id: int
) -> AppButton:
    return AppButton(
        label="Delete",
        style=ButtonStyle.red,
        custom_id=f"delete_type_{type_id}",
        data={"type_id": type_id},
        callback_func=delete_ticket_type
    )

def create_set_type_name_button(
    type_id: int
) -> AppButton:
    return create_modal_button(
        label="Set Name",
        style=ButtonStyle.blurple,
        custom_id=f"type_{type_id}_name",
        data={"type_id": type_id},
        modal_factory=lambda interaction, button:
            SetTypeNameModal(
                interaction,
                button.data["type_id"]
            )
    )

def create_set_type_button_name_button(
    type_id: int
) -> AppButton:
    return create_modal_button(
        label="Set Button Name",
        style=ButtonStyle.blurple,
        custom_id=f"type_{type_id}_button_name",
        data={"type_id": type_id},
        modal_factory=lambda interaction, button:
            SetTypeButtonNameModal(
                interaction,
                button.data["type_id"]
            )
    )

def create_set_type_emoji_button(
    type_id: int
) -> AppButton:
    return create_modal_button(
        label="Set Button Emoji",
        style=ButtonStyle.blurple,
        custom_id=f"type_{type_id}_emoji",
        data={"type_id": type_id},
        modal_factory=lambda interaction, button:
            SetTypeEmojiModal(
                interaction,
                button.data["type_id"]
            )
    )