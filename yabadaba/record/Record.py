# coding: utf-8
# Standard Python libraries
from pathlib import Path
from importlib import resources
from typing import Union, Optional
import io

# https://ipython.org/
from IPython.core.display import display, HTML

# https://lxml.de/
import lxml.etree as ET

import pandas as pd

# https://github.com/usnistgov/DataModelDict
from DataModelDict import DataModelDict as DM

from .. import load_query

class Record():
    """
    Class for handling different record styles in the same fashion.  The
    base class defines the common methods and attributes.
    """

    def __init__(self,
                 model: Union[str, io.IOBase, DM, None] = None,
                 name: Optional[str] = None,
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
        kwargs : any
            Any record-specific attributes to assign.
        """
        self.__model = None
        self.__name = None

        if model is not None:
            assert len(kwargs) == 0, f"cannot specify kwargs with model: '{kwargs.keys()}'"
            self.load_model(model, name=name)
        else:
            self.set_values(name=name, **kwargs)

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

        self._set_model(model)

    def set_values(self, name: Optional[str] = None):
        """
        Set multiple object attributes at the same time.

        Parameters
        ----------
        name : str, optional
            The name to assign to the record.  Often inferred from other
            attributes if not given.
        """
        # Set name if given
        if name is not None:
            self.name = name

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
        if self.__name is not None:
            return self.__name
        else:
            raise AttributeError('record name not set')

    @name.setter
    def name(self, value: Optional[str]):
        if value is not None:
            self.__name = str(value)
        else:
            self.__name = None

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
        raise NotImplementedError('Not defined for this class')

    def metadata(self) -> dict:
        """
        Generates a dict of simple metadata values associated with the record.
        Useful for quickly comparing records and for building pandas.DataFrames
        for multiple records of the same style.
        """
        return {}

    @property
    def queries(self) -> dict:
        """dict: Query objects and their associated parameter names."""
        return {}

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
        matches = load_query('str_match', name='name').pandas(dataframe, name)

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
        load_query('str_match', path='name').mongo(querylist, name)

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
