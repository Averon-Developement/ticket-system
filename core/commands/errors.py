from discord import Interaction, app_commands

from core import logger, Icons


async def handle_command_error(
    interaction: Interaction,
    error: Exception,
) -> None:
    logger.exception(
        f"An unexpected error occurred in '{interaction.command.qualified_name}'",
        exc_info=error
    )

    message = (
        f"{Icons.error} Something went wrong while processing your request. \n"
        "-# If the issue persists, please contact our support server."
    )

    try:
        await interaction.edit_original_response(content=message)

    except Exception:
        await interaction.followup.send(
            content=message,
            ephemeral=True
        )

async def handle_app_command_error(
    interaction: Interaction,
    error: app_commands.AppCommandError
) -> None:

    if isinstance(error, app_commands.MissingPermissions):
        await interaction.response.send_message(
            f"{Icons.error} You do not have permission to use this command.",
            ephemeral=True
        )
        return

    await handle_command_error(
        interaction,
        error
    )