from IPython.display import display, Markdown

from .record import load_record


def querydoc(style: str,
             render: bool = False):
    """
    Generate the querydoc content for a record style.

    Parameters
    ----------
    style : str
        The record style
    render : bool
        If True then the query doc will be rendered for IPython environments.
        If False (default) then it will be returned as a str.
    """

    # Load an empty record
    record = load_record(style)

    # Return/render the querydoc
    if render:
        display(Markdown(record.querydoc))
    else:
        return record.querydoc