"""small bokeh statusbar. 
This is simply a Div with some helper functions.

The reason this is not a class is because I can't figure out how
to correctly subclass Bokeh models, see:

https://discourse.bokeh.org/t/error-when-trying-to-subclass-bokeh-models-div/9584/5

"""

from bokeh.models import Div


def make(*, text: str = "", status: str = "hidden") -> Div:
    """makes a Div that sticks to the top of the page and is wide"""
    return Div(
        text="",
        style={
            "box-shadow": "0px 4px 5px rgba(0, 0, 0, 0.54)",
            "background-color": "#2e7d32",
            "color": "white",
            "width": "110%",
            "height": "25px",
            "margin-bottom": "5px",
            "visibility": "hidden",
        },
        margin=(-10, -10, 0, -10),
        sizing_mode="scale_both",
    )


def set_message(status_bar: Div, message: str) -> None:
    """update text in div"""
    status_bar.text = f"""
    <div style = "padding: 5px 0px 10px 5px;">        
        {message}
    </div>
    """


def set_status(status_bar: Div, status: str) -> None:
    """change color and style of Div based on status"""
    status_bar.style["visibility"] = "visible"
    if status == "ok":
        status_bar.style["background-color"] = "#aed581"
    elif status == "error":
        status_bar.style["background-color"] = "#b71c1c"
    elif status == "warning":
        status_bar.style["background-color"] = "#ffca28"
        status_bar.style["color"] = "black"
    elif status == "hidden":
        status_bar.style["visibility"] = "hidden"
