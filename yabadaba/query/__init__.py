# coding: utf-8

# Relative imports
from . import str_contains, str_match, in_list, int_match, date_match
__all__ = ['str_contains', 'str_match', 'in_list', 'int_match', 'date_match',
           'querymanager', 'load_query']

# Build querymanager
from ..tools import ModuleManager
querymanager = ModuleManager('Query')

from .str_contains import StrContainsQuery
querymanager.loaded_styles['str_contains'] = StrContainsQuery
__all__.append('StrContainsQuery')

from .str_match import StrMatchQuery
querymanager.loaded_styles['str_match'] = StrMatchQuery
__all__.append('StrMatchQuery')

from .in_list import ListContainsQuery
querymanager.loaded_styles['in_list'] = ListContainsQuery
querymanager.loaded_styles['list_contains'] = ListContainsQuery
__all__.append('ListContainsQuery')

from .int_match import IntMatchQuery
querymanager.loaded_styles['int_match'] = IntMatchQuery
__all__.append('IntMatchQuery')

from .date_match import DateMatchQuery
querymanager.loaded_styles['date_match'] = DateMatchQuery
__all__.append('StrContainsQuery')

def load_query(style, name=None, parent=None, path=None):
    """
    Loads a Query subclass associated with a given query style

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
    """
    return querymanager.init(style, name=name, parent=parent, path=path)