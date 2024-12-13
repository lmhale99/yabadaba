from typing import Optional, Union, Any
from copy import deepcopy

from DataModelDict import DataModelDict as DM

from ..query import load_query
from ..tools import dict_insert

class Value():

    def __init__(self,
                 name: str,
                 record,
                 defaultvalue: Optional[Any] = None,
                 valuerequired: bool = False,
                 allowedvalues: Optional[tuple] = None,
                 metadatakey: Union[str, bool, None] = None,
                 metadataparent: Optional[str] = None,
                 modelpath: Optional[str] = None,
                 description: Optional[str] = None):
        """
        Initialize a Value object.

        Parameters
        ----------
        name : str
            The name of the parameter.  This should correspond to the name of
            the associated class attribute.
        record : Record, optional
            The Record object that the Parameter is used with.
        defaultvalue : any or None, optional
            The default value to use for the property.  The default value of
            None indicates that there is no default value.
        valuerequired: bool, optional
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
        """

        self.__name = str(name)
        self.__record = record
        self.__defaultvalue = defaultvalue
        self.__valuerequired = valuerequired
        self.__allowedvalues = allowedvalues

        if description is None:
            description = self.name
        self.__description = description

        if metadatakey is None:
            metadatakey = self.name
        elif isinstance(metadatakey, bool):
            if metadatakey is True:
                raise TypeError('metadatakey can be None, False, or str')
        else:
            metadatakey = str(metadatakey)   
        self.__metadatakey = metadatakey

        self.__metadataparent = metadataparent

        if modelpath is None:
            modelpath = name
        self.__modelpath = str(modelpath)

        self.value = defaultvalue

        self.__queries = deepcopy(self._default_queries)


    @property
    def name(self) -> str:
        """str: The name of the parameter"""
        return self.__name

    @property
    def record(self):
        """Record: The record that this parameter is used with"""
        return self.__record

    @property
    def defaultvalue(self) -> Any:
        """any: The default value to use for the parameter"""
        return self.__defaultvalue
    
    @property
    def valuerequired(self) -> bool:
        """bool: Indicates if the parameter must be given"""
        return self.__valuerequired
    
    @property
    def metadatakey(self) -> Union[str, bool]:
        """str or bool: The key to save the property under in the metadata dict"""
        return self.__metadatakey
    
    @property
    def metadataparent(self) -> Optional[str]:
        """str or None: The parent key in the metadata dict that metadatakey is below"""
        return self.__metadataparent
    
    @property
    def modelpath(self) -> str:
        """str: The period-delimited path after the root element where the parameter is stored in a data model"""
        return self.__modelpath
    
    @property
    def description(self) -> str:
        """str: A short description of the value"""
        return self.__description
    
    @description.setter
    def description(self, val: str):
        self.__description = str(val)

    @property
    def queries(self) -> dict:
        """dict: The Query operations associated with this parameter"""
        return self.__queries
    
    @property
    def value(self) -> Any:
        """any: The value assigned to the parameter"""
        if self.__value is None and self.valuerequired:
            raise ValueError(f'{self.name} has not been set!')
        return self.__value
    
    @value.setter
    def value(self, val):
        val = self.set_value_mod(val)
        
        if self.allowedvalues is not None and val is not None and val not in self.allowedvalues:
            raise ValueError(f'Invalid value {val} for {self.name}. Allowed values are {self.allowedvalues}')
            
        self.__value = val

    def set_value_mod(self, val):
        """Modifies values before setting them"""            
        return val

    @staticmethod
    def set_value_mod_textfield(val: Any) -> Any:
        """
        Utility method for use in set_value_mod that checks for the case where
        a simple value is being set from its modelpath and that element may or
        may not contain XML attributes. 
        """
        # Mod for reading model elements with attributes
        if isinstance(val, dict):
            if '#text' in val:
                val = val['#text']
            else:
                return None
            
        return val

    @property
    def allowedvalues(self) -> Optional[tuple]:
        """tuple or None: tuple containing all allowed values.  If None, no limits."""
        return self.__allowedvalues
    
    @allowedvalues.setter
    def allowedvalues(self, val: Optional[tuple]):
        if val is None:
            self.__allowedvalues = None
        else:
            self.__allowedvalues = tuple(val)

    @property
    def _default_queries(self) -> dict:
        """dict: Default query operations to associate with the Value style"""
        return {}

    def add_query(self,
                  style: str,
                  description: str,
                  name: Optional[str] = None,
                  metadatakey: Optional[str] = None,
                  metadataparent: Optional[str] = None,
                  modelpath: Optional[str] = None):
        """
        Builds and adds a new query operation for the parameter using the
        parameter's settings.

        Parameters
        ----------
        style : str
            The style of Query to add.
        description : str
            The doc description of the Query operation.
        name : str or None, optional
            The name of the keyword argument that will be used in the query
            functions for this Query operation.  If None (default) then the
            name of the parameter will be used which is ideal if only one
            query is associated with the parameter.
        metadatakey : str or None, optional
            The element key of the metadata where the value is.  If None
            (default) then the corresponding parameter value is used.
        metadataparent : str or None, optional
            Allows for the pandas query operations to work on embedded
            metadata dicts.  If given, the pandas query method will check the
            value of metadata[parent][name].
        modelpath : str or None, optional
            The period-delimited path after the record's modelroot where the
            value is found in the model. If None (default) then the corresponding
            parameter value is used.
        """
        if name is None:
            name = self.name
        if metadatakey is None and self.metadatakey is not False:
            metadatakey = self.metadatakey
            metadataparent = self.metadataparent
        if modelpath is None:
            modelpath = self.modelpath
        
        self.queries[name] = load_query(style, name=metadatakey,
                                        parent=metadataparent,
                                        path=f'{self.record.modelroot}.{modelpath}',
                                        description=description)

    def build_model(self,
                    model,
                    **kwargs):
        """
        Inserts the parameter model into the record's model.
        
        Parameters
        ----------
        model : DataModelDict.DataModelDict
            The record content (after root element) to add content to.
        before : any, optional
            An element key at the same final level as this parameter's model
            path that this parameter should be inserted directly before.
            Cannot be given with after.  If neither before nor after is given
            then the parameter will be inserted into the dict normally.
        after : any, optional
            An element key at the same final level as this parameter's model
            path that this parameter should be inserted directly after.
            Cannot be given with before.  If neither before nor after is given
            then the parameter will be inserted into the dict normally.
        """
        # Build value to output
        value = self.build_model_value()
        
        # Do nothing if value not required and empty
        if value is None and self.valuerequired is False:
            return

        # Split path
        path = self.modelpath.split('.')
        
        # Iterate down path and create parent elements if needed
        m = model
        for key in path[:-1]:
            if key not in m:
                m[key] = DM()
            m = m[key]
        
        # Check if target path exists and is a dict
        if path[-1] in m and isinstance(m[path[-1]], dict):
            # Insert the value as #text
            dict_insert(m[path[-1]], '#text', value, **kwargs)

        else:
            # Insert the parameter's value into the model
            dict_insert(m, path[-1], value, **kwargs)


    def build_model_value(self):
        """Function to modify how values are represented in the model"""
        return self.value
    
    def load_model(self, model, setvalue=True) -> Optional[Any]:
        """
        Loads the parameter value from the record's model.
        
        Parameters
        ----------
        model : DataModelDict.DataModelDict
            The record content (after root element) to read.
        setvalue : bool, optional
            If True (default) then the parameter's value will automatically
            be set to the value found at modelpath.  If False, then the
            value at modelpath will be returned instead for further
            manipulations.
        """
        path = self.modelpath.split('.')

        try:
            val = self.load_model_value(model[path])
        except (KeyError, TypeError):
            val = self.defaultvalue

        if setvalue is True:
            self.value = val
        else:
            return val

    def load_model_value(self, val):
        """Function to modify how values are interpreted from the model"""
        return val

    def metadata(self, meta):
        """
        Adds the parameter to the record's metadata dict.

        Parameters
        ----------
        meta : dict
            The metadata dict being built for the record.
        """

        if self.metadatakey is False:
            return
        
        if self.metadataparent is None:
            meta[self.metadatakey] = self.metadata_value()

        else:
            if self.metadataparent not in meta:
                meta[self.metadataparent] = {}
            meta[self.metadataparent][self.metadatakey] = self.metadata_value()

    def metadata_value(self):
        """Function to modify how values are represented in the metadata"""
        return self.value