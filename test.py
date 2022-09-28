import bokeh.layouts
from bokeh.core.properties import Float, String
from bokeh.io import curdoc
from bokeh.models import Div


class ProgressBar(Div):

    __implementation__ = "ProgressBar.ts"

    progress = Float(
        default=10,
        help="""
    progress from 0 to 100
    """,
    )

    color = String(default="cornflowerblue", help="color of progressbar")

    def __init__(self, progress: int = 90):
        super(Div, self).__init__()
        self.width = 300
        self.progress = progress


pbar = ProgressBar()

layout = bokeh.layouts.column(
    Div(text="this is a normal div"),
    pbar,
    Div(text="this is another normal div"),
)

curdoc().add_root(layout)


pbar.progress = 90
pbar.width = 500
pbar.color = "red"
