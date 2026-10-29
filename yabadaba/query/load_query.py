# Standard Python libraries
from typing import Optional

from . import Query, querymanager

def load_query(style: str,
               name: Optional[str] = None,
               parent: Optional[str] = None,
               path: Optional[str] = None,
               description: Optional[str] = None,
               **kwargs) -> Query:
    """
    Loads a Query subclass associated with a given query style.

    Parameters
    ----------
    style : str
        The query style.
    name : str or None, optional
        The metadata key associated with the data field.  Must be set
        to use the pandas query method.
    parent : str or None, optional
        Allows for the pandas query operations to work on embedded
        metadata dicts.  If given, the pandas query method will check the
        value of metadata[parent][name].
    path : str or None, optional
        The record data path to the data field.  Levels are delimited by
        periods.  Must be given to use the mongo query method.
    description : str, optional
        Description of the query operation, i.e. what it is searching.
    **kwargs : any, optional
        Any additional style-specific keyword parameters.
    """
    return querymanager.init(style, name=name, parent=parent, path=path,
                             description=description, **kwargs)