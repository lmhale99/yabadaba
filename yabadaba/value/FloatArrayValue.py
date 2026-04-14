from typing import Optional, Union, Any

import numpy as np
import numpy.typing as npt

from . import Value
from .. import unitconvert as uc

class FloatArrayValue(Value):
    
    @property
    def style(self) -> str:
        """str: The value style"""
        return 'floatarray'
    
    def __init__(self,
                 name: str,
                 record,
                 defaultvalue: Optional[Any] = None,
                 valuerequired: bool = False,
                 allowedvalues: Optional[tuple] = None,
                 allowcustomvalue: bool = False,
                 metadatakey: Union[str, bool, None] = False,
                 metadataparent: Optional[str] = None,
                 modelpath: Optional[str] = None,
                 description: Optional[str] = None,
                 unit: Optional[str] = None,
                 shape: Optional[tuple] = None):
        """
        Initialize an FloatArrayValue object for managing arrays of floats.

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
        allowcustomvalue : bool, optional
            Determines how allowedvalues is interpreted. If False (default) then
            values are restricted to what is listed in allowedvalues.  If True,
            then the value is not restricted and allowedvalues becomes a list of
            recommended values.
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
        shape : tuple, optional
            The dimensions the array must have.  A value of None (default) will
            allow the array to be any shape.
        """
        self.__unit = unit

        if isinstance(shape, int):
            shape = (shape, )
        elif shape is not None:
            shape = tuple([int(i) for i in shape])
        self.__shape = shape

        # Require metadatakey to be explicitly given
        if metadatakey is None:
            metadatakey = False
        
        # Check that allowedvalues is not given
        if allowedvalues is not None:
            raise ValueError('allowedvalues not allowed for arrays')

        super().__init__(name, record, defaultvalue=defaultvalue,
                         valuerequired=valuerequired, allowedvalues=allowedvalues,
                         allowcustomvalue=allowcustomvalue,
                         metadatakey=metadatakey, metadataparent=metadataparent,
                         modelpath=modelpath, description=description)
        
    @property
    def unit(self) -> Optional[str]:
        """str or None: The units to use when saving the value to the model."""
        return self.__unit
    
    @property
    def shape(self) -> Optional[tuple]:
        """tuple or None: The required shape of the array."""
        return self.__shape

    def set_value_mod(self, val):        
        if val is None:
            return None
        elif isinstance(val, str) and self.unit is not None:
            val = uc.set_literal(val)
        else:
            val = np.asarray(val, dtype=float)
        
        if self.shape is not None and val.shape != self.shape:
            raise ValueError(f'{self.name} must have shape {self.shape}')
        
        return val
    
    def build_model_value(self):
        if self.value is None:
            return None
        return uc.model(self.value, self.unit)
        
    def load_model_value(self, val):
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