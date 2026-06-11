from collections.abc import Awaitable, Callable
from discord import Interaction
from discord.ui import Button


class AppButton(Button):
    def __init__(
        self,
        *,
        callback_func: Callable[
            [Interaction, "AppButton"],
            Awaitable[None]
        ],
        data: dict | None = None,
        **kwargs
    ):
        super().__init__(**kwargs)

        self.callback_func = callback_func
        self.data = data or {}

    async def callback(self, interaction: Interaction):
        await self.callback_func(interaction, self)