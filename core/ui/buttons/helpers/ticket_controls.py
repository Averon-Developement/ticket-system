from discord import ButtonStyle, Interaction

from core.ui.buttons import AppButton
from ..callbacks import (
    close_ticket_confirmed,
    close_ticket_canceled
)


def create_close_yes_button() -> AppButton:
    return AppButton(
        label="Yes",
        style=ButtonStyle.green,
        custom_id="close_ticket_yes",
        callback_func=close_ticket_confirmed
    )

def create_close_no_button() -> AppButton:
    return AppButton(
        label="No",
        style=ButtonStyle.red,
        custom_id="close_ticket_no",
        callback_func=close_ticket_canceled
    )