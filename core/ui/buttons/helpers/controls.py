from discord import ButtonStyle, Interaction

from core.ui.buttons import AppButton
from ..callbacks import (
    back_to_settings,
    back_to_type_config,
    back_to_ticket_types,
    send_panel_to_channel,
    edit_welcome_panel
)


def create_back_to_settings_button(
    disabled: bool = False
) -> AppButton:
    return AppButton(
        label="Save & Go back",
        style=ButtonStyle.green,
        custom_id="back_button",
        disabled=disabled,
        callback_func=back_to_settings
    )

def create_back_to_ticket_types_button(
    disabled: bool
) -> AppButton:
    return AppButton(
        label="Save & Go back",
        style=ButtonStyle.green,
        custom_id="save_button",
        disabled=disabled,
        callback_func=back_to_ticket_types
    )

def create_back_to_type_config_button(
    type_id: int,
    disabled: bool
) -> AppButton:
    return AppButton(
        label="Save & Go back",
        style=ButtonStyle.green,
        custom_id="type_go_back_button",
        disabled=disabled,
        data={
            "type_id": type_id
        },
        callback_func=back_to_type_config
    )


def create_send_panel_button(
    panel_id: int,
    disabled: bool = False
) -> AppButton:
    return AppButton(
        label="Send Panel",
        style=ButtonStyle.gray,
        custom_id="send_panel_button",
        disabled=disabled,
        data={
            "panel_id": panel_id
        },
        callback_func=send_panel_to_channel
    )

def create_edit_welcome_panel_button(
    type_id: int
) -> AppButton:
    return AppButton(
        label="Edit Welcome Panel",
        style=ButtonStyle.blurple,
        custom_id="wlc_panel_button",
        data={
            "type_id": type_id
        },
        callback_func=edit_welcome_panel
    )