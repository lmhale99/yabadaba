__all__ = ['base', 'recordmanager', 'load_record', 'Record']

# Relative imports
from .base import Record
from ..tools import ModuleManager

# Initialize ModuleManager for records
recordmanager = ModuleManager('Record')

from .load_record import load_record

# Append Record Values to valuemanager
from .. import valuemanager
ignorelist = ['__pycache__', '__init__']
valuemanager.dynamic_import(f'{__name__}.record_values', ignorelist)

# Backwards compatibility aliases
valuemanager.import_style('record', '.recordlist', f'{__name__}.record_values', 'RecordListValue')
