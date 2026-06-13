from discord import Interaction, app_commands

from core import logger, colors


async def handle_command_error(
    interaction: Interaction,
    error: Exception,
) -> None:
    logger.exception(
        f"An unexpected error occurred in '{interaction.command.qualified_name}'",
        exc_info=error
    )

    from core.ui.components import CustomMessageComponent

    content = (
        f"Something went wrong while processing your request. "
        "If the issue persists, please contact our support server."
    )

    view = CustomMessageComponent(
        content=content,
        accent_color=colors.red
    )

    try:
        await interaction.edit_original_response(view=view)

    except Exception:
        await interaction.followup.send(
            view=view,
            ephemeral=True
        )

async def handle_app_command_error(
    interaction: Interaction,
    error: app_commands.AppCommandError
) -> None:

    from core.ui.components import CustomMessageComponent

    if isinstance(error, app_commands.MissingPermissions):
        await interaction.response.send_message(
            view=CustomMessageComponent(
                content="You do not have permission to execute this command.",
                accent_color=colors.red
            ),
            ephemeral=True
        )
        return

    await handle_command_error(
        interaction,
        error
    )