from typing import Optional, Union, Any

from DataModelDict import DataModelDict as DM

from ..query import load_query
from . import Value
from .. import unitconvert as uc

class FloatValue(Value):
    
    def __init__(self,
                 name: str,
                 Record,
                 defaultvalue: Optional[Any] = None,
                 valuerequired: bool = False,
                 metadatakey: Union[str, bool, None] = None,
                 metadataparent: Optional[str] = None,
                 modelpath: Optional[str] = None,
                 modelunit: Optional[str] = None):
        """
        Initialize a general Parameter object.

        Parameters
        ----------
        name : str
            The name of the parameter.  This should correspond to the name of
            the associated class attribute.
        record : Record
            The Record object that the Parameter is used with.
        defaultvalue : any or None, optional
            The default value to use for the property.  The default value of
            None indicates that there is no default value.
        valuerequired: bool
            Indicates if a value must be given for the property.  If True, then
            checks will be performed that a value is assigned to the property.
        metadatakey: str, bool or None, optional
            The key name to use for the property when constructing the record
            metadata dict.  If set to None (default) then name will be used for
            metadatakey.  If set to False then the parameter will not be
            included in the metadata dict.
        metadataparent: str or None, optional
            If given, then this indicates that the metadatakey is actually an
            element of a dict in metadata with this name.  This allows for limited
            support for metadata having embedded dicts.
        modelpath: str, optional
            The period-delimited path after the record root element for
            where the parameter will be found in the built data model.  If set
            to None (default) then name will be used for modelpath.
        modelunit: str, optional
            The units to use when saving the value to the model  A value of None
            (default) indicates that no unit conversions should be done.
        """
        self.__modelunit = modelunit
        
        super().__init__(name, Record, defaultvalue=defaultvalue,
                         valuerequired=valuerequired, metadatakey=metadatakey,
                         metadataparent=metadataparent, modelpath=modelpath)
        
    @property
    def modelunit(self) -> Optional[str]:
        """str or None: The units to use when saving the value to the model."""
        return self.__modelunit

    def set_value_mod(self, val):
        if val is None:
            return None
        elif isinstance(val, str) and self.modelunit is not None:
            return uc.set_literal(val)
        else:
            return float(val)
    
    @property
    def _default_queries(self) -> dict:
        """dict: Default query operations to associate with the Parameter style"""
        return {
            self.name: load_query('float_match',
                                  name=self.metadatakey,
                                  parent=self.metadataparent,
                                  path=f'{self.record.modelroot}.{self.modelpath}',
                                  unit=self.modelunit,
                                  description=f'Return only the records where {self.name} matches a given value')
        }
    
    def build_model_value(self):
        
        if self.modelunit is None:
            return self.value
        else:
            return uc.model(self.value, self.modelunit)
        
    def load_model_value(self, val):
        if self.modelunit is None:
            return val
        else:
            return uc.value_unit(val)
        