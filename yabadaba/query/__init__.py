__all__ = ['querymanager', 'Query', 'load_query']

# Relative imports
from .Query import Query

# Initialize a ModuleManager for the query styles
from ..tools import ModuleManager
querymanager = ModuleManager('Query')
ignorelist = ['__pycache__', '__init__', 'load_query', 'Query']
querymanager.dynamic_import(__name__, ignorelist)

# Backwards compatibility aliases
querymanager.import_style('int_match', '.int', __name__, 'IntQuery')
querymanager.import_style('float_match', '.float', __name__, 'FloatQuery')

from .load_query import load_query