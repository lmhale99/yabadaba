# coding: utf-8

# Standard Python libraries
from typing import Any, Optional

import numpy as np

import pandas as pd

# Relative imports
from .. import unitconvert as uc
from ..tools import iaslist

from .Query import Query

class FloatMatchQuery(Query):
    """Class for querying float fields for closely matching values"""

    def __init__(self,
                 name: Optional[str] = None,
                 parent: Optional[str] = None,
                 path: Optional[str] = None,
                 description: str = '',
                 unit: Optional[str] = None,
                 atol: float = 1e-5):
        """
        Query initialization

        Parameters
        ----------
        name : str or None, optional
            The metadata key associated with the data field.  Must be set
            to use the pandas query method.
        parent : str or None, optional
            Allows for the pandas query operations to work on embedded
            metadata dicts.  If given, the pandas query method will check the
            value of metadata[parent][name].
        path : str or None, optional
            The record data path to the data field.  Levels are delimited by
            periods.  Must be given to use the mongo query method.
        description : str, optional
            Description of the query operation, i.e. what it is searching.
        unit : str or None, optional
            Unit to use for the given query value.  This should be the unit
            used in the JSON/XML records for the value in question.  A value
            of None indicates no unit or conversion needed.
        atol : float, optional
            Absolute tolerance for comparison.  Returned True values will be
            for float fields between +-atol of the target value.  Default
            value is 1e-5.
        """
        self.__atol = atol
        self.__unit = unit
        super().__init__(name=name, parent=parent, path=path, description=description)

    @property
    def style(self) -> str:
        """str: The query style"""
        return 'float_match'

    @property
    def parameter_type(self) -> str:
        """str: The types of query parameter values accepted by this query style"""
        return 'float or list, optional'

    @property
    def unit(self) -> str:
        """str : The unit to use for the query value"""
        return self.__unit

    @property
    def atol(self) -> float:
        """float: The absolute tolerance to use for value comparison"""
        return self.__atol

    def mongo(self,
              querylist: list,
              value: Any,
              prefix: str = ''):
        """
        Builds a Mongo query operation for the field.

        Parameters
        ----------
        querylist : list
            The working list of mongo query operations which is to be appended
            with the operation for this query object.
        value : any
            The value of the field to query on.  If None, then no new query
            operation will be added.
        prefix : str, optional
            An optional prefix to add before the query path.  Used by Record's
            mongoquery to start each path with "content."
        """
        # Get path and add prefix
        path = f'{prefix}{self.path}'

        if value is not None:

            # Init newquery as list of $or evaluations
            newquery = {'$or':[]}

            # Iterate over all values
            for v in iaslist(value):
                v = float(v)

                # Add query operation for ranged search
                newquery['$or'].append({path:{'$gte': v - self.atol, '$lte' : v + self.atol}})
            
            # Append newquery to querylist
            querylist.append(newquery)

    def pandas(self,
               df: pd.DataFrame,
               value: Any) -> pd.Series:
        """
        Applies a query filter to the metadata for the field.
        
        Parameters
        ----------
        df : pandas.DataFrame
            A table of metadata for multiple records of the record style.
        value : any
            The value of the field to query on.  If None, then it should return
            True for all rows of df.
        
        Returns
        -------
        pandas.Series
            Boolean map of matching values
        """

        def apply_function(series: pd.Series,
                           name: str,
                           value: Any,
                           parent: Optional[str]) -> bool:
            """
            function for pandas.DataFrame.apply with axis=1
            
            Parameters
            ----------
            series : pd.Series
                A series of the DataFrame being operated on.
            name : str
                The element name.
            value : any
                The values to search for.
            parent : str or None
                The parent element name, if there is one.

            Returns
            -------
            bool
                True if value is None or if one given value matches the
                element being checked.
            """
            # Return True for all fields if value is None
            if value is None:
                return True
            
            # Convert value to array of floats
            value = np.array([float(v) for v in iaslist(value)])

            # Convert value to target units
            value = uc.set_in_units(value, self.unit)

            if parent is None:

                # Check if name is in series
                if name not in series or pd.isna(series[name]):
                    return False
                
                # Check for a value match
                return np.any(np.isclose(float(series[name]), value, rtol=0.0, atol=self.atol))
            
            else:

                # Loop over all child elements
                for child in iaslist(series[parent]):

                    # Check if child element has name
                    if name in child and pd.notna(child[name]):

                        # Check if child element matches a value
                        if np.any(np.isclose(float(child[name]), value, rtol=0.0, atol=self.atol)):
                            return True

                # Return default False for no matching child elements
                return False

        # Use apply_function on df using value and object attributes
        return df.apply(apply_function, axis=1, args=(self.name, value, self.parent)).astype(bool)
