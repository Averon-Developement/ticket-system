from discord.ui import LayoutView, Container, TextDisplay


class CustomMessageComponent(LayoutView):
    def __init__(
        self,
        title: str,
        content: str,
        accent_color: str = None
    ):
        super().__init__(timeout=None)

        container = Container(
            accent_color=accent_color
        )
        container.add_item(
            TextDisplay(content=(
                f"## {title}\n"
                f"{content}"
            ))
        )
        self.add_item(container)