from rich.console import Console
from rich.default_styles import DEFAULT_STYLES
from rich.style import Style
from rich.theme import Theme

styles = {**DEFAULT_STYLES, "important": Style(bold=True, underline=True)}

standard_output = Console(theme=Theme(styles))
standard_error = Console(stderr=True, theme=Theme(styles))
