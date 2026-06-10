import time

from discord.ui import Button, View
from discord import ButtonStyle, Interaction, PermissionOverwrite

from core.database.handlers import (
    TicketTypeHandler,
    TicketHandler,
    TicketTypeRoleHandler,
    BlacklistHandler,
    WelcomePanelHandler
)

class PersistentTicketPanel(View):
    def __init__(self):
        super().__init__(timeout=None)

        for type in TicketTypeHandler.get_all_types():
            self.add_item(
                CreateTicketButton(
                    type_id=type.type_id,
                    name=type.name,
                    style=ButtonStyle(type.button_style),
                    emoji=type.emoji
                )
            )


class CreateTicketButton(Button):
    def __init__(
        self,
        type_id: int,
        name: str,
        style: ButtonStyle,
        emoji: str | None = None
    ):
        super().__init__(
            label=name,
            style=style,
            emoji=emoji,
            custom_id=f"ticket_type:{type_id}"
        )

        self.type_id = type_id

    async def callback(self, interaction: Interaction):
        await interaction.response.defer(ephemeral=True)

        is_blacklisted = BlacklistHandler(
            interaction.guild.id, user_id=interaction.user.id
        ).get_blacklisted_user()

        if is_blacklisted:
            return await interaction.followup.send(
                content="You are not allowed to create a ticket.",
                ephemeral=True
            )

        ticket_open = TicketHandler.get_open_by_type_and_creator(
            interaction.guild.id, self.type_id, interaction.user.id
        )

        if ticket_open:
            channel = interaction.guild.get_channel(ticket_open.channel_id)

            return await interaction.followup.send(
                content=f"You already have a ticket open at {channel.mention} for this type.",
                ephemeral=True
            )

        type_config = TicketTypeHandler(self.type_id).get_type()
        support_roles = TicketTypeRoleHandler(self.type_id).get_roles()

        category = interaction.guild.get_channel(type_config.category_id)

        overwrites = {
            interaction.guild.default_role: PermissionOverwrite(
                view_channel=False
            ),
            interaction.user: PermissionOverwrite(
                view_channel=True, send_messages=True, read_message_history=True,
                attach_files=True, embed_links=True
            )
        }

        for role in support_roles:
            role = interaction.guild.get_role(role.role_id)

            if role:
                overwrites[role] = PermissionOverwrite(
                    view_channel=True, send_messages=True, read_message_history=True,
                    attach_files=True, embed_links=True
                )

        channel = await interaction.guild.create_text_channel(
            name=f"{type_config.name.lower()}-{interaction.user.name}",
            category=category, overwrites=overwrites,
            reason=f"{type_config.name} ticket created by {interaction.user.name}"
        )

        TicketHandler.create_ticket(
            interaction.guild.id, self.type_id, channel.id,
            interaction.user.id, int(time.time())
        )

        panel_config = WelcomePanelHandler.get_panel_by_type(type_config.type_id)

        from core.ui.components import WelcomePanelPreview
        await channel.send(
            view=WelcomePanelPreview(panel_config.panel_id, interaction, preview=False)
        )

        await interaction.followup.send(
            content=f"Ticket created at {channel.mention}.",
            ephemeral=True
        )



