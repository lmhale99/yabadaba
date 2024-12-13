from typing import Optional, Union, Any

from DataModelDict import DataModelDict as DM

from ..query import load_query
from . import Value
from ..tools import iaslist

class StrListValue(Value):
    
    def set_value_mod(self, val):
        if val is None:
            return None
        else:
            return [str(v) for v in iaslist(val)]
    
    @property
    def _default_queries(self) -> dict:
        """dict: Default query operations to associate with the Parameter style"""
        if self.metadatakey is False:
            return {}
        else:
            return {
                self.name: load_query('list_contains',
                                    name=self.metadatakey,
                                    parent=self.metadataparent,
                                    path=f'{self.record.modelroot}.{self.modelpath}',
                                    description=f'Return only the records where {self.description} contains a given value')
            }
    
    def build_model_value(self):
        if self.value is None or len(self.value) == 0:
            return
        elif len(self.value) == 1:
            return self.value[0]
        return self.value