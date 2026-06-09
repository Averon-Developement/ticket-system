from discord import Member


def replace_text_placeholders(
    content: str | None,
    user: Member
) -> str:
    if not content:
        return ""

    return (
        content
        .replace("{user.mention}", user.mention)
        .replace("{user.name}", user.name)
        .replace("{user.displayname}", user.display_name)
        .replace("{user.id}", str(user.id))
    )


def replace_thumbnail_placeholder(
    thumbnail: str | None,
    user: Member
) -> str | None:
    if not thumbnail:
        return None

    if thumbnail == "{user.avatar}":
        return user.display_avatar.url if user.display_avatar else None

    return thumbnail