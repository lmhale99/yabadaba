from typing import Optional, Union, Any

from DataModelDict import DataModelDict as DM

import numpy as np

from ..query import load_query
from . import Value

class BoolValue(Value):
    
    def set_value_mod(self, val):
        
        # Check if value is in #text
        val = self.set_value_mod_textfield(val)
        
        # Pass Boolean values through without changing
        if val is True or val is False or val is None:
            return val

        if isinstance(val, str):
            # Convert strings
            if val.lower() in ['true', 't']:
                return True
            elif val.lower() in ['false', 'f']:
                return False
            else:
                raise ValueError(f'String value for {self.name} not recognized as a Boolean value.')
        else:
            raise TypeError(f'Invalid type for Boolean {self.name}. Must be True, False, None, or a str representation of True or False')
    
    @property
    def _default_queries(self) -> dict:
        """dict: Default query operations to associate with the Parameter style"""
        if self.metadatakey is False:
            return {}
        else:
            return {
                self.name: load_query('bool_match',
                                    name=self.metadatakey,
                                    parent=self.metadataparent,
                                    path=f'{self.record.modelroot}.{self.modelpath}',
                                    description=f'Return only the records where {self.description} matches a given value')
            }