# coding: utf-8

# Standard Python libraries
from typing import Any, Optional, NoReturn

import pandas as pd

# Relative imports
from ..tools import iaslist

from .Query import Query

class IntMatchQuery(Query):
    """Class for querying int fields for matching values"""

    @property
    def style(self) -> str:
        """str: The query style"""
        return 'int_match'

    @property
    def description(self) -> str:
        """str: Describes the query operation that the class performs."""
        return 'Query an int field for specific values'

    def mongo(self, querydict: dict, value: Any, prefix: str = '') -> NoReturn:
        """
        Builds a Mongo query operation for the field.

        Parameters
        ----------
        querydict : dict
            The set of mongo query operations that the new operation will be
            added to.
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
        
            # Build the query 
            val = [int(v) for v in iaslist(value)]
            querydict[path] = {'$in': val}

    def pandas(self, df: pd.DataFrame, value: Any) -> pd.Series:
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
            
            # Convert value to list of ints
            value = [int(v) for v in iaslist(value)]

            if parent is None:

                # Check if name is in series
                if name not in series or pd.isna(series[name]):
                    return False
                
                # Check for a value match
                return int(series[name]) in value
            
            else:

                # Loop over all child elements
                for child in iaslist(series[parent]):

                    # Check if child element has name
                    if name in child and pd.notna(child[name]):

                        # Check if child element matches a value
                        if int(child[name]) in value:
                            return True

                # Return default False for no matching child elements
                return False

        # Use apply_function on df using value and object attributes
        return df.apply(apply_function, axis=1, args=(self.name, value, self.parent))
