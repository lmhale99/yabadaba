from typing import Optional, Union, Any
from inspect import isclass

from DataModelDict import DataModelDict as DM

from . import recordmanager, Record
from ..query import load_query
from ..value import Value
from ..tools import aslist, iaslist

class RecordSubsetValue(Value):
    
    def __init__(self,
                 name: str,
                 record,
                 recordclass: Union[str, type[Record]],
                 defaultvalue: Optional[Any] = None,
                 valuerequired: bool = False,
                 allowedvalues: Optional[tuple] = None,
                 metadatakey: Union[str, bool, None] = None,
                 metadataparent: Optional[str] = None,
                 metadataprefix: str = '',
                 modelpath: Optional[str] = None,
                 description: Optional[str] = None):
        """
        Initialize a Value that is a record object.  Allows for the reuse of
        common subsets across multiple records.

        Note: Many of the default Value parameter settings are limited or not
        used by this style. Read below!

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
            The default value to use for the property.  If given, then it must
            be an object of recordclass.  If None (default), a new empty object
            of recordclass will be created and set as the value.
        valuerequired: bool, optional
            This is meaningless for record subsets as an associated record
            object will always exist for the value.
        allowedvalues : tuple or None, optional
            Must be None (default) for record subsets as the data is complex.
        metadatakey: str, bool or None, optional
            Must be None or False for record subset values, where None is the
            default behavior and False indicates no metadata keys from the subset
            will be added to the parent record's metadata.
        metadataparent: str or None, optional
            If given, then this indicates that the metadatakey is actually an
            element of a dict in metadata with this name.  This allows for limited
            support for metadata having embedded dicts.
        metadataprefix: str or None, optional
            This specifies a prefix to add to the beginning of all of the subset's
            metadata keys when incorporated into the parent record's metadata.
            This makes it possible to avoid key name overlaps.  Default value is '',
            i.e. no prefix.
        modelpath: str or None, optional
            The period-delimited path after the record root element for
            where the parameter will be found in the built data model.  If set
            to None (default) then name will be used for modelpath.  Note that the
            final path name will override the subset's modelroot.
        description: str or None, optional
            A short description for the value.
        """
        # Check incompatible parameter values
        if allowedvalues is not None:
            raise ValueError('allowedvalues must be None for record subsets as the data is complex')
        if metadatakey is not None and metadatakey is not False:
            raise ValueError('metadatakey must be None or False for record subsets')

        # Set metadataprefix
        if isinstance(metadataprefix, str):
            self.__metadataprefix = metadataprefix
        else:
            raise TypeError('metadataprefix must be a str')

        # Get recordclass as Record class or style name
        if isclass(recordclass) and issubclass(recordclass, Record):
            self.__recordclass = recordclass
        elif isinstance(recordclass, str):
            self.__recordclass = recordmanager.get_class(recordclass)
        else:
            raise TypeError('invalid recordclass: should be a Record class or string record style')
        
        # Set defaultvalue to an empty record if needed
        if defaultvalue is None:
            defaultvalue = self.recordclass(noname=True)

        super().__init__(name, record, defaultvalue=defaultvalue,
                         valuerequired=valuerequired, allowedvalues=allowedvalues,
                         metadatakey=metadatakey, metadataparent=metadataparent,
                         modelpath=modelpath, description=description)

    @property
    def style(self) -> str:
        """str: The value style"""
        return 'recordsubset'
    
    def valuedoc(self, indent=0) -> str:
        """Builds the valuedoc information for the value"""
        pre = ' '*indent
        doc = [f'{pre}- __{self.name}__ (*{self.recordclass().style} record*): {self.description}']
        for value in self.value.value_objects:
            doc.append(value.valuedoc(indent+4))

        return '\n'.join(doc)
    
    @property
    def recordclass(self) -> type[Record]:
        """Class: The record class associated with this value"""
        return self.__recordclass
    
    @property
    def metadataprefix(self) -> str:
        """str or None: A prefix to append to all metadata keys of the subset record"""
        return self.__metadataprefix


    @property
    def _default_queries(self) -> dict:
        """dict: Default query operations to associate with the Value style"""
        if self.metadatakey is False:
            return {}
        
        # Build __default_queries if it doesn't already exist
        elif not hasattr(self, '__default_queries'):
            
            # Get the metadata key prefix
            prefix = self.metadataprefix
            
            self.__default_queries = {}
            for key, record_query in self.value.queries.items():
                if record_query.parent is not None:
                    # Skip queries that already have parents
                    continue
                
                style = record_query.style
                name = f'{prefix}{record_query.name}'
                parent = self.metadataparent
                path = f'{self.record.modelroot}.{self.modelpath}.{".".join(record_query.path.split(".")[1:])}'
                description = record_query.description
                self.__default_queries[f'{prefix}{key}'] = load_query(style=style, name=name,
                                                         parent=parent, path=path,
                                                         description=description)

        return self.__default_queries

    def set_value_mod(self, val):
        
        # Check that val is of the correct record class
        if isinstance(val, self.recordclass):
            return val
        elif isinstance(val, dict):
            return self.recordclass(noname=True, **val)
        else:
            raise TypeError(f'value must be a {self.recordclass} object')

    def build_model_value(self):
        
        # Get subset's model without root element
        model = self.value.build_model()[self.value.modelroot]

        return model
    
    def metadata(self, meta):
        """
        Adds all subset metadata fields to the record's metadata dict.

        Parameters
        ----------
        meta : dict
            The metadata dict being built for the record.
        """

        if self.metadatakey is False:
            return
        
        # Get the metadata key prefix
        prefix = self.metadataprefix

        # Get the subset's metadata dict
        subsetmetadata = self.value.metadata()

        if self.metadataparent is None:
            for key, value in subsetmetadata.items():
                if key == 'name':
                    continue
                meta[f'{prefix}{key}'] = value

        else:
            if self.metadataparent not in meta:
                meta[self.metadataparent] = {}
            for key, value in subsetmetadata.items():
                if key == 'name':
                    continue
                meta[self.metadataparent][f'{prefix}{key}'] = value
    
    def load_model_value(self, val):
        
        # Load contents into the value object
        model = DM()
        model[self.value.modelroot] = val
        self.value.load_model(model=model)

        # Return value object to reassign it to itself...
        return self.value
