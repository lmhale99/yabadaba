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

from . import demo

from . import query
from .query import querymanager, load_query

from . import record
from .record import recordmanager, load_record

from . import database
from .database import databasemanager, load_database

__all__ = ['__version__', 'tools', 'settings', 'unitconvert',
           'query', 'load_query', 'querymanager', 'demo',
           'record', 'load_record', 'recordmanager',
           'database', 'load_database', 'databasemanager']
__all__.sort()
