from IPython.display import display, Markdown

from .record import load_record


def valuedoc(style: str,
             render: bool = False):
    """
    Generate the valuedoc content for a record style.

    Parameters
    ----------
    style : str
        The record style
    render : bool
        If True then the valuedoc will be rendered for IPython environments.
        If False (default) then it will be returned as a str.
    """

    # Load an empty record
    record = load_record(style)

    # Return/render the valuedoc
    if render:
        display(Markdown(record.valuedoc))
    else:
        return record.valuedoc