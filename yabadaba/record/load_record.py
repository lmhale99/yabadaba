from typing import TYPE_CHECKING
from pathlib import Path

from DataModelDict import DataModelDict as DM

from . import recordmanager, Record

if TYPE_CHECKING:
    from ..database import Database

# Define load_record
def load_record(style: str,
                model: str | Path | DM | None = None,
                name: str | None = None,
                database: Database | None = None,
                **kwargs) -> Record:
    """
    Loads a Record subclass associated with a given record style.

    Parameters
    ----------
    style : str
        The record style.
    name : str, optional
        The name to give to the specific record.
    model : str, DataModelDict, optional
        Data model content to load for the given record style.
    database : yabadaba.Database, optional
        Allows for a default database to be associated with the record.
    **kwargs : any
        Any extra keyword parameter supported by the record style.

    Returns
    -------
    subclass of Record 
        A Record object for the style
    """
    record = recordmanager.init(style, model=model, name=name, **kwargs)
    if database is not None:
        record.database = database
    return record