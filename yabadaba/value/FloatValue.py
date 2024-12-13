from typing import Optional, Union, Any

from DataModelDict import DataModelDict as DM

from ..query import load_query
from . import Value
from .. import unitconvert as uc

class FloatValue(Value):
    
    def __init__(self,
                 name: str,
                 record,
                 defaultvalue: Optional[Any] = None,
                 valuerequired: bool = False,
                 allowedvalues: Optional[tuple] = None,
                 metadatakey: Union[str, bool, None] = None,
                 metadataparent: Optional[str] = None,
                 modelpath: Optional[str] = None,
                 description: Optional[str] = None,
                 unit: Optional[str] = None):
        """
        Initialize a FloatValue object.

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
        allowedvalues : tuple or None, optional
            A list/tuple of values that the parameter is restricted to have.
            Setting this to None (default) indicates any value is allowed.
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
        description: str or None, optional
            A short description for the value.  If not given, then the record name
            will be used.
        unit: str, optional
            The units to use when saving the value in a database.  A value of None
            (default) indicates that no unit conversions should be done.
        """
        self.__unit = unit
        
        super().__init__(name, record, defaultvalue=defaultvalue,
                         valuerequired=valuerequired, allowedvalues=allowedvalues,
                         metadatakey=metadatakey, metadataparent=metadataparent,
                         modelpath=modelpath, description=description)
        
    @property
    def unit(self) -> Optional[str]:
        """str or None: The units to use when saving the value to the model."""
        return self.__unit

    def set_value_mod(self, val):

        # Check if value is in #text
        val = self.set_value_mod_textfield(val)

        if val is None:
            return None
        elif isinstance(val, str) and self.unit is not None:
            return uc.set_literal(val)
        else:
            return float(val)
    
    @property
    def _default_queries(self) -> dict:
        """dict: Default query operations to associate with the Parameter style"""
        if self.metadatakey is False:
            return {}
        else:
            return {
                self.name: load_query('float_match',
                                    name=self.metadatakey,
                                    parent=self.metadataparent,
                                    path=f'{self.record.modelroot}.{self.modelpath}',
                                    description=f'Return only the records where {self.description} matches a given value')
            }
    
    def build_model_value(self):
        if self.value is None:
            return None
        
        if self.unit is None:
            return self.value
        else:
            return uc.model(self.value, self.unit)
        
    def load_model_value(self, val):
        if self.unit is None:
            return val
        else:
            return uc.value_unit(val)
        
    def metadata(self, meta):
        """
        Adds the parameter to the record's metadata dict.

        Parameters
        ----------
        meta : dict
            The metadata dict being built for the record.
        """
        if self.metadatakey is False or self.value is None:
            return
        
        # Convert value to unit 
        value = self.value
        if self.unit is not None:
            value = uc.get_in_units(value, self.unit)
        
        if self.metadataparent is None:
            meta[self.metadatakey] = value

        else:
            if self.metadataparent not in meta:
                meta[self.metadataparent] = {}
            meta[self.metadataparent][self.metadatakey] = value
        