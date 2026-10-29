__all__ = ['Database', 'databasemanager', 'load_database']

# Import base Database class
from .Database import Database

# Initialize a ModuleManager for the database styles
from ..tools import ModuleManager
databasemanager = ModuleManager('Database')
ignorelist = ['__pycache__', '__init__', 'load_database', 'Database']
databasemanager.dynamic_import(__name__, ignorelist)

# Import load_database
from .load_database import load_database