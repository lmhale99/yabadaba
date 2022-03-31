# coding: utf-8
__all__ = ['Record', 'recordmanager', 'load_record']

# Standard Python libraries
from typing import Optional, Union

from DataModelDict import DataModelDict as DM

# Relative imports
from .Record import Record
from ..tools import ModuleManager

# Initialize ModuleManager for records
recordmanager = ModuleManager('Record')

# Define load_record 
def load_record(style: str,
                name: Optional[str] = None,
                model: Union[str, DM, None] = None,
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
    **kwargs : any
        Any extra keyword parameter supported by the record style.

    Returns
    -------
    subclass of Record 
        A Record object for the style
    """
    return recordmanager.init(style, model=model, name=name, **kwargs)
