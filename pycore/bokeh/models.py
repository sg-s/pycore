from bokeh.core.properties import Float, String
from bokeh.models import Div


class ProgressBar(Div):
    """a model that inherits from Div, and displays
    a small progress bar with customizable text,
    color, and percentage"""

    __implementation__ = "ProgressBar.ts"

    progress = Float(
        default=10,
        help="""
    progress from 0 to 100
    """,
    )

    color = String(default="cornflowerblue", help="color of progressbar")

    def __init__(self, progress: int = 10):
        """constructor"""

        super(Div, self).__init__()
        self.width = 300
        self.height = 10
        self.progress = progress
