import os

import matplotlib as mpl
import matplotlib.pyplot as plt
from IPython.display import Markdown, display
from pycore.core import hash_dict, md5hash


def offer_editable_mpl_figure(func):
    """wrapper to make links to downloadable
    versions of plotted mpl figures
    """

    def _wrapper(*args, **kwargs):

        hashes = []
        for arg in args:
            hashes.append(md5hash(arg))

        hashes.append(hash_dict(kwargs))

        arghash = md5hash(hashes)

        fig = func(*args, **kwargs)
        _save_figure(
            fig=fig,
            file_name=arghash,
            save_folder=".",
            formats=[".pdf"],
        )

        display(
            Markdown(f"[↓ ᴇᴅɪᴛᴀʙʟᴇ ꜰɪɢᴜʀᴇ ({arghash[0:7]})]({arghash}.pdf)")
        )

    return _wrapper


def _save_figure(
    *,
    fig: plt.Figure,
    file_name: str,
    save_folder: str,
    formats: list = [".png"],
    transparent: bool = False,
    dpi: int = 300,
    size: tuple = None,
) -> None:
    """
    Convenience function for saving a matplotlib figure
    Saves high resolution PNG and/or vector editable PDF (with editable text)

    ### Arguments:

    - fig (matplotlib figure canvas): Figure to save
    - fname: Desired filename (without extension)
    - save_folder: Desired save folder.
    If None, will save to current path. Defaults to None.
    - formats (list, optional): Formats to save in (e.g ['.png', '.pdf']
    would save both a PNG and PDF version). Defaults to ['.png'].
    - transparent (bool, optional): Whether background should be transparent.
    Defaults to False.
    - dpi (int, optional): Resolution for PNG. Defaults to 300.
    - size (tuple of floats): Desired size for saved figure.
    If None, uses current figure size. Defaults to None



    """

    # This ensures that font is editable
    mpl.rcParams["pdf.fonttype"] = 42

    # If size is passed, resize the figure to desired size
    if size is not None:
        fig.set_size_inches(size)
    # if size isn't explicitly passed, saves at same size
    # figure is displayed at

    for format in formats:
        fig.savefig(
            os.path.join(save_folder, file_name + format),
            transparent=transparent,
            orientation="landscape",
            dpi=dpi,
        )
