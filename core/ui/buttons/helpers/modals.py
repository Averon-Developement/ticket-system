from collections.abc import Callable
from discord import ButtonStyle, Interaction

from ..button import AppButton


def create_modal_button(
    *,
    label: str,
    style: ButtonStyle,
    custom_id: str,
    modal_factory: Callable[
        [Interaction, AppButton], 
        object
    ],
    data: dict | None = None,
    disabled: bool = False,
) -> AppButton:

    async def callback(
        interaction: Interaction,
        button: AppButton
    ) -> None:
        await interaction.response.send_modal(
            modal_factory(interaction, button)
        )

    return AppButton(
        label=label,
        style=style,
        custom_id=custom_id,
        disabled=disabled,
        data=data,
        callback_func=callback,
    )