import time

from discord.ui import Button, View
from discord import ButtonStyle, Interaction, PermissionOverwrite

from core import Icons
from core.database.handlers import (
    TicketTypeHandler,
    TicketHandler,
    TicketTypeRoleHandler,
    BlacklistHandler,
    WelcomePanelHandler,
    GuildSettingsHandler
)

class PersistentTicketPanel(View):
    def __init__(self):
        super().__init__(timeout=None)

        for type in TicketTypeHandler.get_all_types():
            self.add_item(
                CreateTicketButton(
                    type_id=type.type_id,
                    button_name=type.button_name,
                    style=ButtonStyle(type.button_style),
                    emoji=type.emoji
                )
            )


class CreateTicketButton(Button):
    def __init__(
        self,
        type_id: int,
        button_name: str,
        style: ButtonStyle,
        emoji: str | None = None
    ):
        super().__init__(
            label=button_name,
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
                content=f"{Icons.error} You are not allowed to create a ticket.",
                ephemeral=True
            )

        guild_settings = GuildSettingsHandler(
            interaction.guild.id
        ).get_settings()

        open_tickets = TicketHandler.get_open_by_creator(
            interaction.guild.id,
            interaction.user.id
        )

        if len(open_tickets) >= guild_settings.max_tickets:
            ticket_mentions = []

            for ticket in open_tickets:
                channel = interaction.guild.get_channel(
                    ticket.channel_id
                )

                if channel:
                    ticket_mentions.append(channel.mention)

            return await interaction.followup.send(
                content=(
                    f"{Icons.error} You already have `{len(open_tickets)}`/`{guild_settings.max_tickets}` "
                    f"tickets open.\n"
                    f"-# Open Tickets: {', '.join(ticket_mentions)}"
                ),
                ephemeral=True
            )
        
        msg = await interaction.followup.send(
            content="*Creating ticket...*",
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
        welcome_message = await channel.send(
            view=WelcomePanelPreview(panel_config.panel_id, interaction, preview=False)
        )

        await welcome_message.pin(reason="Ticket welcome message.")

        await msg.edit(
            content=f"{Icons.success} Ticket created: {channel.mention}."
        )


class TicketActionsView(View):
    def __init__(self):
        super().__init__(timeout=None)

        self.add_item(TicketCloseButton())
        self.add_item(TicketClaimButton())

class TicketCloseButton(Button):
    def __init__(self):
        super().__init__(
            label="Close",
            style=ButtonStyle.danger,
            custom_id="ticket_close",
            emoji="🔒"
        )

    async def callback(self, interaction):
        await interaction.response.defer(ephemeral=True)

        if not interaction.user.guild_permissions.manage_messages:
            return await interaction.followup.send(
                content="You do not have the permissions to close this ticket.",
                ephemeral=True
            )

        await interaction.followup.send(
            content="Are you sure you want to close this ticket?",
            view=ConfirmTicketClose(),
            ephemeral=True,
        )


class ConfirmTicketClose(View):
    def __init__(self):
        super().__init__(timeout=30)

        from core.ui.buttons.helpers import (
            create_close_yes_button, create_close_no_button
        )

        self.add_item(create_close_yes_button())
        self.add_item(create_close_no_button())
        

class TicketClaimButton(Button):
    def __init__(self):
        super().__init__(
            label="Claim",
            style=ButtonStyle.gray,
            custom_id="ticket_claim",
            emoji="📌"
        )

    async def callback(self, interaction):
        pass