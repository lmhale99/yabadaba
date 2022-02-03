# coding: utf-8

# Relative imports
from ..tools import aslist, iaslist
from .Query import Query

# https://pandas.pydata.org/
import pandas as pd

class StrContainsQuery(Query):
    """Class for querying str fields for contained values"""

    @property
    def style(self):
        """str: The query style"""
        return 'str_contains'

    @property
    def description(self):
        """str: Describes the query operation that the class performs."""
        return 'Query a str field for containing specific values'

    def mongo(self, querydict, value, prefix=''):
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
        path = f'{prefix}{self.path}'
        if value is not None:
            val = aslist(value)
            querydict['$and'] = []
            for v in val:
                querydict['$and'].append({path:{'$regex': v}})

    def pandas(self, df, value):
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

        def apply_function(series, name, value, parent):
            if value is None:
                return True
            
            if parent is None:
                if pd.isna(series[name]):
                    return False

                for v in iaslist(value):
                    if v not in series[name]:
                        return False
                return True
            
            else:
                for v in iaslist(value):
                    match = False
                    for p in series[parent]:
                        if name in p and v in p[name]:
                            match = True
                            break
                    if match is False:
                        return False
                return True

        return df.apply(apply_function, axis=1, args=(self.name, value, self.parent))
