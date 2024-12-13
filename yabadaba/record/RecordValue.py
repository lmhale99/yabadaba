from typing import Optional, Union, Any

from DataModelDict import DataModelDict as DM

from . import recordmanager, Record
from ..query import load_query
from ..value import Value
from ..tools import aslist, iaslist

class RecordValue(Value):
    
    def __init__(self,
                 name: str,
                 record,
                 recordclass: Union[str, type[Record]],
                 defaultvalue: Optional[Any] = None,
                 valuerequired: bool = False,
                 allowedvalues: Optional[tuple] = None,
                 metadatakey: Union[str, bool, None] = None,
                 metadataparent: Optional[str] = None,
                 modelpath: Optional[str] = None,
                 description: Optional[str] = None):
        """
        Initialize a general Parameter object.

        Parameters
        ----------
        name : str
            The name of the parameter.  This should correspond to the name of
            the associated class attribute.
        record : Record
            The Record object that the Value is used with, i.e. which record
            is it contained within.
        recordclass : str or class
            The type of record that this value represents.  Given either as a
            string record style or a Record class.
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
        if issubclass(recordclass, Record):
            self.__recordclass = recordclass
        elif isinstance(recordclass, str):
            self.__recordclass = recordmanager.get_class(recordclass)
        else:
            raise TypeError('invalid recordclass: should be a Record class or string record style')
        self.__emptyrecord = self.recordclass(noname=True)

        super().__init__(name, record, defaultvalue=defaultvalue,
                         valuerequired=valuerequired, allowedvalues=allowedvalues,
                         metadatakey=metadatakey, metadataparent=metadataparent,
                         modelpath=modelpath, description=description)

    @property
    def recordclass(self) -> type[Record]:
        """Class: The record class associated with this value"""
        return self.__recordclass
    
    @property
    def emptyrecord(self) -> Record:
        """Record: An empty record of the appropriate style that is used to check metadata"""
        return self.__emptyrecord
    
    @property
    def _default_queries(self) -> dict:
        """dict: Default query operations to associate with the Value style"""
        if self.metadatakey is False:
            return {}
        elif not hasattr(self, '__default_queries'):
            self.__default_queries = {}
            for key, record_query in self.emptyrecord.queries.items():
                if record_query.parent is not None:
                    # Skip queries that already have parents
                    continue
                
                style = record_query.style
                name = record_query.name
                parent = self.metadatakey
                path = f'{self.record.modelroot}.{self.modelpath}.{".".join(record_query.path.split(".")[1:])}'
                description = record_query.description
                self.__default_queries[key] = load_query(style=style, name=name,
                                                         parent=parent, path=path,
                                                         description=description)

        return self.__default_queries

    def set_value_mod(self, val):
        
        # Set as empty list if None
        if val is None:
            return []

        # Convert val into list
        if isinstance(val, dict):
            val = [val]
        else:
            val = aslist(val)

        for i, v in enumerate(val):
            
            # Check if Record of the correct style, and set noname
            if isinstance(v, Record):
                if v.style != self.emptyrecord.style:
                    raise ValueError('value being set is not of the expected record style')
                v.noname = True
            
            # Build record from dict of init parameters
            elif isinstance(v, dict):
                v['noname'] = True
                val[i] = self.recordclass(**v)
            
            else:
                raise TypeError('value(s) must be Record objects or dicts of Record init parameters')

        return val

    def append(self, **kwargs):
        """
        Appends a Record value to the current list.

        Parameters
        ----------
        val : Record, dict, DM, str, or file-like object
            A record object or the associated content given either as a dict
            of keyword parameters or as a data model.
        """
        kwargs['noname'] = True
        val = self.recordclass(**kwargs)
        self.value.append(val)

    def build_model_value(self):
        models = []
        for val in self.value:
            models.append(val.build_model()[self.emptyrecord.modelroot])

        if len(models) == 0:
            return
        elif len(models) == 1:
            return models[0]
        return models
    
    def metadata_value(self):
        """Function to modify how values are represented in the metadata"""
        metadatas = []
        for val in self.value:
            metadatas.append(val.metadata())
        return metadatas
    
    def load_model_value(self, val):
        if isinstance(val, dict):
            val = [val]
        
        models = []
        for v in val:
            model = DM()
            model[self.emptyrecord.modelroot] = v
            models.append({'model': model})

        return models
