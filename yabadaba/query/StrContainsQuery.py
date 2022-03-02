# coding: utf-8

# Standard Python libraries
from typing import Any, Optional

# Relative imports
from ..tools import iaslist
from .Query import Query

# https://pandas.pydata.org/
import pandas as pd

class StrContainsQuery(Query):
    """Class for querying str fields for contained values"""

    @property
    def style(self) -> str:
        """str: The query style"""
        return 'str_contains'

    @property
    def description(self) -> str:
        """str: Describes the query operation that the class performs."""
        return 'Query a str field for containing specific values'

    def mongo(self, querydict: dict, value: Any, prefix: str = ''):
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
            # Add $and if needed
            if '$and' not in querydict:
                querydict['$and'] = []

            # Build a regex query for each given value
            for v in iaslist(value):
                querydict['$and'].append({path:{'$regex': str(v)}})
                #querydict['$and'].append({path:{'$regex': v}})

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
                True if value is None or if all values are contained in the/an
                element being checked.
            """
            
            # Return True for all fields if value is None
            if value is None:
                return True
            
            if parent is None:

                # Check if name is in series
                if name not in series or pd.isna(series[name]):
                    return False

                # Check if all values are in series[name]
                for v in iaslist(value):
                    if v not in series[name]:
                        return False
                return True
            
            else:

                # Loop over all child elements
                for child in iaslist(series[parent]):
                    
                    # Check if child element has name
                    if name in child and pd.notna(child[name]):
                        match = True
                        
                        # Check if all values are in child[name]
                        for v in iaslist(value):
                            if v not in child[name]:
                                match = False
                        if match:
                            return True
                
                # Return default False for no matching child elements
                return False

        # Use apply_function on df using value and object attributes
        return df.apply(apply_function, axis=1, args=(self.name, value, self.parent))
