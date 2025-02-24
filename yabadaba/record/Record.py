# coding: utf-8
# Standard Python libraries
from pathlib import Path
from importlib import resources
from typing import Union, Optional, Any
import io
from tarfile import TarFile

# https://ipython.org/
from IPython.display import display, HTML

from PIL import Image

# https://lxml.de/
import lxml.etree as ET

import pandas as pd

# https://github.com/usnistgov/DataModelDict
from DataModelDict import DataModelDict as DM

from .. import load_query, load_value

class Record():
    """
    Class for handling different record styles in the same fashion.  The
    base class defines the common methods and attributes.
    """

    def __init__(self,
                 model: Union[str, io.IOBase, DM, None] = None,
                 name: Optional[str] = None,
                 database = None,
                 noname: bool = False,
                 **kwargs: any):
        """
        Initializes a Record object for a given style.
        
        Parameters
        ----------
        model : str, file-like object, or DataModelDict, optional
            The contents of the record.
        name : str, optional
            The unique name to assign to the record.  If model is a file
            path, then the default record name is the file name without
            extension.
        database : yabadaba.Database, optional
            A default Database to associate with the Record, typically the
            Database that the Record was obtained from.  Can allow for Record
            methods to perform Database operations without needing to specify
            which Database to use.
        nonoame : bool, optional
            Flag indicating if the record does not get assigned a name.  This
            is primarily for when a record class is used as a value inside
            another class, i.e., this record is a subset of another.
        kwargs : any
            Any record-specific attributes to assign.
        """
        self.__model = None
        self.__name = None
        self.tar = None
        self.database = database
        self.noname = noname

        self.__value_objects = None
        self.__value_objects = tuple(self._init_value_objects())
        self._init_values()
        if len(self.__value_dict) > 0:
            if len(self.value_objects) > 0:
                raise ValueError('Value objects should not be set using both _init_value_objects and _init_value_dict')
            self.__value_objects = tuple(self.__value_dict.values())

        if model is not None:
            assert len(kwargs) == 0, f"cannot specify kwargs with model: '{kwargs.keys()}'"
            self.load_model(model, name=name)
        else:
            self.set_values(name=name, **kwargs)

    def _init_value_objects(self) -> list:
        """
        Method that defines the value objects for the Record.  This should
        1. Call the method's super().
        2. Use yabadaba.load_value() to build Value objects that are set to
           private attributes of self.
        3. Append the list returned by the super() with the new Value objects.

        Returns
        -------
        value_objects: A list of all value objects.
        """
        if self.__value_objects is not None:
            raise RuntimeError('_init_value_objects should only be called by Record.__init__')

        return []

    def _init_values(self):
        """
        Method that defines the value objects for the Record.  This should
        call the super of this method, then use self._add_value to create new Value objects.
        Note that the order values are defined matters
        when build_model is called!!!
        """
        pass

    def _add_value(self,
                   style: str,
                   name: str,
                   defaultvalue: Optional[Any] = None,
                   valuerequired: bool = False,
                   allowedvalues: Optional[tuple] = None,
                   metadatakey: Union[str, bool, None] = None,
                   metadataparent: Optional[str] = None,
                   modelpath: Optional[str] = None,
                   description: Optional[str] = None,
                   **kwargs):
        """
        Method to add Value objects when defining the class.  This should only be
        used when defining _init_values()!

        Parameters
        ----------
        style : str
            The value style.
        name : str
            The name for the parameter value.  This corresponds to the name of
            the associated class attribute.
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
        **kwargs : any, optional
            Any additional style-specific keyword parameters.
        """
        self.__value_dict[name] = load_value(style=style, name=name, record=self,
                                             defaultvalue=defaultvalue,
                                             valuerequired=valuerequired,
                                             allowedvalues=allowedvalues,
                                             metadatakey=metadatakey,
                                             metadataparent=metadataparent,
                                             modelpath=modelpath,
                                             description=description,
                                             **kwargs)

    def __getattr__(self, name: str):
        """Adjusted to get value attributes from Value objects"""
        if name.startswith('__'):
            super().__getattr__(self, name)

        elif name == '_Record__value_dict':
            self.__value_dict = {}
            return self.__value_dict
        
        elif name in self.__value_dict:
            return self.__value_dict[name].value
    
    def __setattr__(self, name: str, value: Any):
        """Adjusted to set to value attributes of Value objects"""
        if name == '_Record__value_dict' or name.startswith('__'):
            super().__setattr__(name, value)
        elif name in self.__value_dict:
            self.__value_dict[name].value = value
        else:
            super().__setattr__(name, value)


    def load_model(self,
                   model: Union[str, io.IOBase, DM],
                   name: Optional[str] = None):
        """
        Loads record contents from a given model.

        Parameters
        ----------
        model : str, file-like object, or DataModelDict
            The model contents of the record to load.
        name : str, optional
            The name to assign to the record.  Often inferred from other
            attributes if not given.
        """
        # Get name if model is a filename
        if name is None:
            try:
                if Path(model).is_file():
                    self.name = Path(model).stem
            except (ValueError, OSError, TypeError):
                pass
        else:
            self.name = name

        # Read/set model
        self._set_model(model)

        # Extract parameter values 
        rec = self.model[self.modelroot]
        for value_object in self.value_objects:
            value_object.load_model(rec)

        if self.noname is False:
            try:
                assert self.name is not None
            except:
                try:
                    self.name = self.defaultname
                except:
                    self.name = None

    def set_values(self, **kwargs):
        """
        Set multiple object attributes at the same time.

        Parameters
        ----------
        **kwargs: any
            Any parameters for the record that you wish to set values for.
        """
        if 'name' in kwargs:
            self.name = kwargs['name']
        
        for value_object in self.value_objects:
            if value_object.name in kwargs:
                setattr(self, value_object.name, kwargs[value_object.name])

        if self.noname is False:
            try:
                assert self.name is not None
            except:
                try:
                    self.name = self.defaultname
                except:
                    self.name= None

    def __str__(self) -> str:
        """str: The string representation of the record"""
        return f'{self.style} record named {self.name}'

    @property
    def style(self) -> str:
        """str: The record style"""
        return 'base'

    @property
    def xsd_filename(self) -> tuple:
        """tuple: The module path and file name of the record's xsd schema"""
        raise NotImplementedError('Not implemented')

    @property
    def xsd(self) -> bytes:
        """bytes: The xml schema for the record style."""
        return resources.read_binary(*self.xsd_filename)

    @property
    def xsl_filename(self) -> tuple:
        """tuple: The module path and file name of the record's xsl html transformer"""
        raise NotImplementedError('Not implemented')

    @property
    def xsl(self) -> bytes:
        """bytes: The xsl transformer for the record style."""
        return resources.read_binary(*self.xsl_filename)

    @property
    def name(self) -> str:
        """str: The record's name."""
        if self.__name is not None or self.noname:
            return self.__name
        else:
            raise AttributeError('record name not set')

    @name.setter
    def name(self, value: Optional[str]):
        if value is not None:
            if self.noname:
                raise TypeError('name turned off for this record')
            self.__name = str(value)
        else:
            self.__name = None

    @property
    def defaultname(self) -> Optional[str]:
        """str: The name to default to, usually based on other properties"""
        return None

    @property
    def noname(self) -> bool:
        """bool: Indicates that the record should not have a name."""
        return self.__noname

    @noname.setter
    def noname(self, val: bool):
        if not isinstance(val, bool):
            raise TypeError('noname must be a bool')
        self.__noname = val

    @property
    def value_objects(self) -> tuple:
        """tuple: The Value objects associated with the Record"""
        return self.__value_objects

    def get_value(self, name):
        """Returns a Value object from __value_dict by name"""
        return self.__value_dict[name]

    @property
    def modelroot(self) -> str:
        """str : The name of the root element in the model contents."""
        raise NotImplementedError('Specific to subclasses')

    @property
    def model(self) -> DM:
        """DataModelDict: The record's model content."""
        if self.__model is not None:
            return self.__model
        else:
            raise AttributeError('model content has not been loaded or built')

    def reload_model(self):
        """
        Reloads the record based on the model content.  This allows for direct
        changes to the model to be updated to the object. 
        """
        self.load_model(model=self.model, name=self.name)

    def _set_model(self, model: DM):
        """
        Sets model content - called by build_model() and load_model() to update
        content.  Use load_model() if you are passing in an external model.
        """
        try:
            modelroot = self.modelroot
        except NotImplementedError:
            self.__model = DM(model)
        else:
            # Load model as DataModelDict
            content = DM(model).find(modelroot)
            self.__model = DM([(modelroot, content)])

    def build_model(self):
        """
        Generates and returns model content based on the values set to object.
        """
        self.__model = DM()
        self.__model[self.modelroot] = rec = DM()

        for value_object in self.value_objects:
            value_object.build_model(rec)        

        return self.__model

    def metadata(self) -> dict:
        """
        Generates a dict of simple metadata values associated with the record.
        Useful for quickly comparing records and for building pandas.DataFrames
        for multiple records of the same style.
        """
        meta = {}
        # Initialize with only name
        if self.noname is False:
            meta['name'] = self.name

        # Add value object values
        for value_object in self.value_objects:
            value_object.metadata(meta)
        
        return meta

    @property
    def metadatakeys(self) -> list:
        """list: The keys included in the metadata dict"""
        keys = []
        if self.noname is False:
            keys.append('name')
        
        # Add value object values
        for value_object in self.value_objects:
            if value_object.metadataparent is not None:
                keys.append(value_object.metadataparent)
            elif value_object.metadatakey is not False:
                keys.append(value_object.metadatakey)
        
        return keys

    @property
    def queries(self) -> dict:
        """dict: Query objects and their associated parameter names."""
        
        # Build dict containing all queries of all values
        queries = {}
        for value_object in self.value_objects:
            queries.update(value_object.queries)
        
        return queries

    @property
    def querynames(self) -> list:
        """list: The query parameter names supported by the record."""
        return list(self.queries.keys())

    @property
    def querydoc(self) -> str:
        """str: A description of all the queries supported by the record."""
        doc = f'# {self.style} Query Parameters\n\n'
        for name, query in self.queries.items():
            doc += f'- __{name}__ (*{query.parameter_type}*): {query.description}\n'

        return doc

    def pandasfilter(self,
                     dataframe: pd.DataFrame,
                     name: Union[str, list, None] = None,
                     **kwargs: any) -> pd.Series:
        """
        Filters a pandas.DataFrame based on kwargs values for the record style.
        
        Parameters
        ----------
        dataframe : pandas.DataFrame
            A table of metadata for multiple records of the record style.
        name : str or list, optional
            The record name(s) to parse by.
        **kwargs : any
            Any of the record style-specific search parameters.

        Returns
        -------
        pandas.Series
            Boolean map of matching values
        """
        # Get defined queries
        queries = self.queries

        # Query name
        if self.noname is False:
            matches = load_query('str_match', name='name').pandas(dataframe, name)
        elif name is not None:
            raise ValueError('name turned off for record')

        # Apply queries based on given kwargs
        for key in kwargs:
            matches = (matches & queries[key].pandas(dataframe, kwargs[key]))

        return matches

    def mongoquery(self,
                   name: Union[str, list, None] = None,
                   **kwargs: any) -> dict:
        """
        Builds a Mongo-style query based on kwargs values for the record style.

        Parameters
        ----------
        name : str or list, optional
            The record name(s) to parse by.
        **kwargs : any
            Any of the record style-specific search parameters.

        Returns
        -------
        dict
            The Mongo-style query
        """
        # Get the dict of queries
        queries = self.queries

        # Initialize the full query dict and list of query operations
        querydict = {}
        querydict['$and'] = querylist = [{}]

        # Query name
        if self.noname is False:
            load_query('str_match', path='name').mongo(querylist, name)
        elif name is not None:
            raise ValueError('name turned off for record')

        # Apply queries based on given kwargs
        for key in kwargs:
            queries[key].mongo(querylist, kwargs[key], prefix='content.')

        return querydict

    def cdcsquery(self,
                  **kwargs: any) -> dict:
        """
        Builds a CDCS-style query based on kwargs values for the record style.
        
        Parameters
        ----------
        **kwargs : any
            Any of the record style-specific search parameters.
        
        Returns
        -------
        dict
            The CDCS-style query
        """
        # Get the dict of queries
        queries = self.queries

        # Initialize the query dictionary
        querydict = {}
        querydict['$and'] = querylist = [{}]

        # Apply queries based on given kwargs
        for key in kwargs:
            queries[key].mongo(querylist, kwargs[key])

        return querydict

    def html(self,
             render: bool = False) -> Optional[str]:
        """
        Returns an HTML representation of the object.
        
        Parameters
        ----------
        render : bool, optional
            If True, then IPython is used to render the HTML.  If False
            (default), then the HTML code is returned as a str.

        Returns
        -------
        str
            The HTML code contents.  Returned if render=False.
        """

        # Build xml content
        xml_content = self.model.xml()

        xml = ET.fromstring(xml_content.encode('UTF-8'))

        # Read xsl content
        xsl = ET.fromstring(self.xsl)

        # Transform to html
        transform = ET.XSLT(xsl)
        html = transform(xml)
        html_content = ET.tostring(html).decode('UTF-8')

        if render:
            display(HTML(html_content))
        else:
            return html_content

    def valid_xml(self,
                  xml_content: Optional[str] = None) -> bool:
        """
        Tests if XML content is valid with schema.
        
        Parameters
        ----------
        xml_content : str, optional
            XML content to test against the record's schema.
            If not given, will generate the xml using build_model.
        
        Returns
        -------
        bool
            Indicating if XML is valid.
        """

        # Build xml content
        if xml_content is None:
            xml_content = self.model.xml()

        xml = ET.fromstring(xml_content.encode('UTF-8'))

        # Read xsd content
        xsd = ET.fromstring(self.xsd)

        schema = ET.XMLSchema(xsd)
        return schema.validate(xml)

    @property
    def database(self):
        """yabadaba.Database or None: The default Database associated with the Record"""
        return self.__database

    @database.setter
    def database(self, value):
        if value is None or hasattr(value, 'get_records'):
            self.__database = value
        else:
            raise TypeError('database must be a yabadaba.Database or None')

    @property
    def tar(self):
        """tarfile.TarFile: The tar archive associated with the record"""
        # Return tarfile if set
        if self.__tar is not None:
            return self.__tar

        # Check if database is set
        if self.database is None:
            raise ValueError('tar not loaded and no database set')

        # Fetch tar from database, set to cache and return
        self.tar = self.database.get_tar(record=self)
        return self.__tar

    @tar.setter
    def tar(self, value: Optional[TarFile]):
        if value is None or isinstance(value, TarFile):
            self.__tar = value
        else:
            raise TypeError('tar must ne a TarFile or None')

    def clear_tar(self):
        """Closes and unsets the record's tar file to save memory"""
        if self.__tar is not None:
            self.__tar.close()
            self.tar = None

    def get_file(self,
                 filename: Union[str, Path],
                 localroot: Union[str, Path, None] = None,
                 local: bool = True):
        """
        Retrieves a file either locally or from the record's tar archive.

        Parameters
        ----------
        filename : str or Path
            The name/path for the file.  For local files, this is taken
            relative to localroot.  For files in the tar archive, this is taken
            relative to the tar's root directory which is always named for the
            record, i.e., {self.name}/{filename}.
        localroot : str, Path or None, optional
            The local root directory that filename (if it exists) is relative
            to.  The default value of None will use the current working
            directory.
        local : bool, optional
            If True (default) then the localroot will be checked for the file
            prior to retrieving the file from the tar.  If False then only the
            tar will be checked.
        
        Raises
        ------
        ValueError
            If filename exists in the tar but is not a file.

        Returns
        -------
        io.IOBase
            A file-like object in binary read mode that allows for the file
            contents to be read.
        """
        if local:
            # Set default root path
            if localroot is None:
                localroot = Path.cwd()
            else:
                localroot = Path(localroot)

            # Return local copy of file if it exists
            localfile = Path(localroot, filename)
            if Path(localfile).is_file():
                return open(localfile, 'rb')

        # Return file extracted from tar
        fileio = self.tar.extractfile(f'{self.name}/{filename}')
        if fileio is not None:
            return fileio
        else:
            raise ValueError(f'{filename} exists in tar, but is not a file')

    def display_image(self,
                      filename: Union[str, Path],
                      localroot: Union[str, Path, None] = None,
                      width: Optional[int] = None,
                      height: Optional[int] = None):
        """
        For IPython-based environments, this retrieves an image file either
        locally or from within the record's tar archive and displays it.

        Parameters
        ----------
        filename : str or Path
            The name/path for the file.  For local files, this is taken
            relative to localroot.  For files in the tar archive, this is taken
            relative to the tar's root directory which is always named for the
            record, i.e., {self.name}/{filename}.
        localroot : str, Path or None, optional
            The local root directory that filename (if it exists) is relative
            to.  The default value of None will use the current working
            directory.
        
        Raises
        ------
        ValueError
            If filename exists in the tar but is not a file.
        """
        fileio = self.get_file(filename=filename, localroot=localroot)
        img = Image.open(fileio)

        if width is not None:
            if height is None:
                oldwidth, oldheight = img.size
                height = round(oldheight * (width / oldwidth))
            size = (width, height)
            img = img.resize(size)

        elif height is not None:
            oldwidth, oldheight = img.size
            width = round(oldwidth * (height / oldheight))
            size = (width, height)
            img = img.resize(size)

        display(img)