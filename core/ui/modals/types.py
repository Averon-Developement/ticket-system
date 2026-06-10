import emoji
from discord import Interaction, PartialEmoji
from discord.ui import Modal, TextInput

from core import logger
from core.database.handlers import TicketTypeHandler


class SetTypeNameModal(Modal, title="Set name"):
    def __init__(
        self,
        org_interaction: Interaction,
        type_id: int
    ):
        super().__init__()

        self.org_interaction = org_interaction
        self.type_id = type_id

    type_name = TextInput(
        label="Set name",
        placeholder="e.g. Support",
        max_length=50,
        min_length=3,
        required=True
    )

    async def on_submit(self, interaction: Interaction):
        await interaction.response.defer(ephemeral=True)

        type_config = TicketTypeHandler(self.type_id)

        if not type_config:
            return await interaction.followup.send(
                content="No type config found. If this issue persists, please contact our support",
                ephemeral=True
            )
        
        try:
            type_config.set_name(self.type_name.value)
        
        except Exception as error:
            logger.exception(
                f"Failed to save the type name in server ({interaction.guild.name} {interaction.guild.id}): {error}"
            )

            return await interaction.followup.send(
                content="Failed to set the type name. If this issue persists, please contact our support",
                ephemeral=True
            )

        from core.ui.components import TicketTypesConfigMenu
        await self.org_interaction.edit_original_response(
            view=TicketTypesConfigMenu(interaction.guild, self.type_id)
        )


class SetTypeEmojiModal(Modal, title="Set Custom Emoji"):
    def __init__(
        self,
        org_interaction: Interaction,
        type_id: int
    ):
        super().__init__()

        self.org_interaction = org_interaction
        self.type_id = type_id

    type_emoji = TextInput(
        label="Set emoji",
        placeholder="e.g. 📩",
        max_length=50,
        required=True
    )

    async def on_submit(self, interaction: Interaction):
        await interaction.response.defer(ephemeral=True)

        type_config = TicketTypeHandler(self.type_id)

        if not type_config:
            return await interaction.followup.send(
                content="No type config found. If this issue persists, please contact our support.",
                ephemeral=True
            )

        emoji_value = self.type_emoji.value.strip()
        parsed = PartialEmoji.from_str(emoji_value)

        is_custom_emoji = parsed.id is not None
        is_unicode_emoji = emoji.is_emoji(emoji_value)

        if not is_custom_emoji and not is_unicode_emoji:
            return await interaction.followup.send(
                content="Please provide a valid Discord emoji.",
                ephemeral=True
            )

        try:
            type_config.set_emoji(emoji_value)

        except Exception as error:
            logger.exception(
                f"Failed to save the type emoji in server "
                f"({interaction.guild.name} {interaction.guild.id}): {error}"
            )

            return await interaction.followup.send(
                content="Failed to set the type emoji. If this issue persists, please contact our support.",
                ephemeral=True
            )

        from core.ui.components import TicketTypesConfigMenu

        await self.org_interaction.edit_original_response(
            view=TicketTypesConfigMenu(
                interaction.guild,
                self.type_id
            )
        )