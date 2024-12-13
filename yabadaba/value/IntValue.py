from typing import Optional, Union, Any

from DataModelDict import DataModelDict as DM

import numpy as np

from ..query import load_query
from . import Value

class IntValue(Value):
    
    def set_value_mod(self, val):

        # Check if value is in #text
        val = self.set_value_mod_textfield(val)

        if val is None:
            return None
        elif isinstance(val, float):
            rval = round(val)
            if not np.isclose(rval, val):
                raise TypeError(f'{self.name} not an int!')
            return rval
        else:
            try:
                return int(val)
            except Exception as e:
                raise ValueError(f'{self.name} not an int!') from e
    
    @property
    def _default_queries(self) -> dict:
        """dict: Default query operations to associate with the Parameter style"""
        if self.metadatakey is False:
            return {}
        else:
            return {
                self.name: load_query('int_match',
                                    name=self.metadatakey,
                                    parent=self.metadataparent,
                                    path=f'{self.record.modelroot}.{self.modelpath}',
                                    description=f'Return only the records where {self.description} matches a given value')
            }