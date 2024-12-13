from typing import Optional, Union, Any
import datetime

from DataModelDict import DataModelDict as DM

import numpy as np

from ..query import load_query
from . import Value

class DateValue(Value):
    
    def set_value_mod(self, val):
        
        # Check if value is in #text
        val = self.set_value_mod_textfield(val)
        
        if val is None:
            val = datetime.date.today()
        elif not isinstance(val, datetime.date):
            val = datetime.datetime.strptime(val, '%Y-%m-%d').date()
        return val
        
    def build_model_value(self):
        return str(self.value)

    @property
    def _default_queries(self) -> dict:
        """dict: Default query operations to associate with the Parameter style"""
        if self.metadatakey is False:
            return {}
        else:
            return {
                self.name: load_query('date_match',
                                    name=self.metadatakey,
                                    parent=self.metadataparent,
                                    path=f'{self.record.modelroot}.{self.modelpath}',
                                    description=f'Return only the records where {self.description} matches a given value')
            }
    