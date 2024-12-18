# coding: utf-8
# Standard Python libraries
from importlib import resources

# Read version from VERSION file
if hasattr(resources, 'files'):
    __version__ = resources.files('yabadaba').joinpath('VERSION').read_text(encoding='UTF-8')
else:
    __version__ = resources.read_text('yabadaba', 'VERSION', encoding='UTF-8').strip()

# Relative imports
from .UnitConverter import unitconvert
from . import tools
from .Settings import settings

from . import query
from .query import querymanager, load_query

from . import value
from .value import valuemanager, load_value

from . import record
from .record import recordmanager, load_record

from . import database
from .database import databasemanager, load_database

from .check_modules import check_modules
from .querydoc import querydoc

__all__ = ['__version__', 'tools', 'settings', 'unitconvert',
           'query', 'load_query', 'querymanager',
           'record', 'load_record', 'recordmanager',
           'value', 'load_value', 'valuemanager',
           'database', 'load_database', 'databasemanager',
           'check_modules', 'querydoc']
__all__.sort()
