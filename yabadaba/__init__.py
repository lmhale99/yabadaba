# coding: utf-8
__all__ = sorted(['__version__', 'tools', 'settings',
                 'query', 'load_query', 'querymanager',
                 'record', 'load_record', 'recordmanager',
                 'database', 'load_database', 'databasemanager'])

# Standard Python libraries
from importlib import resources

# Read version from VERSION file
__version__ = resources.read_text('yabadaba', 'VERSION').strip()

__all__ = ['__version__', 'tools', 'settings', 'record', 'load_record']
__all__.sort()

# Relative imports
from . import tools
from .Settings import settings

from . import demo

from . import query
from .query import querymanager, load_query

from . import record
from .record import recordmanager, load_record

from . import database
from .database import databasemanager, load_database
