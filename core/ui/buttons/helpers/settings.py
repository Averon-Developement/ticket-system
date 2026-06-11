
from discord import ButtonStyle

from core.ui.buttons import AppButton
from core.ui.modals import SetMaxTicketsModal
from ..helpers import create_modal_button

from ..callbacks import (
    toggle_transcripts,
    navigate_ticket_types,
    navigate_ticket_panel
)


def create_max_tickets_button() -> AppButton:
    return create_modal_button(
        label="Set Max Tickets",
        style=ButtonStyle.primary,
        custom_id="max_tickets_button",
        modal_factory=lambda interaction, _:
            SetMaxTicketsModal(interaction)
    )

def create_toggle_transcripts_button(enabled: bool) -> AppButton:
    return AppButton(
        label="Disable" if enabled else "Enable",
        style=(
            ButtonStyle.red if enabled 
            else ButtonStyle.green
        ),
        custom_id="toggle_transcripts_button",
        data={
            "enabled": enabled
        },
        callback_func=toggle_transcripts
    )

def create_ticket_types_button() -> AppButton:
    return AppButton(
        label="Types",
        style=ButtonStyle.blurple,
        custom_id="ticket_types_button",
        callback_func=navigate_ticket_types
    )

def create_ticket_panel_button() -> AppButton:
    return AppButton(
        label="Panel",
        style=ButtonStyle.blurple,
        custom_id="ticket_panel_button",
        callback_func=navigate_ticket_panel
    )