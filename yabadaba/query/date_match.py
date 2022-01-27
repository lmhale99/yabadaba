# coding: utf-8

# Relative imports
from ..tools import iaslist
from .Query import Query

class DateMatchQuery(Query):
    """Class for querying date fields for matching values"""

    @property
    def style(self):
        """str: The query style"""
        return 'date_match'

    @property
    def description(self):
        """str: Describes the query operation that the class performs."""
        return 'Query a date field for specific values'

    def mongo(self, querydict, value):
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
        """
        if value is not None:
            value = [str(v) for v in iaslist(value)]
            querydict[self.path] = {'$in': value}

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
            value = [str(v) for v in iaslist(value)]

            if parent is None:
                return str(series[name]) in value
            
            else:
                for p in series[parent]:
                    if name in p and str(p[name]) in value:
                        return True
                return False

        return df.apply(apply_function, axis=1, args=(self.name, value, self.parent))

# Define legacy functions

def description():
    return DateMatchQuery().description

def mongo(qdict, path, val):
    DateMatchQuery(path=path).mongo(qdict, val)

def pandas(df, name, val, parent=None):
    return DateMatchQuery(name=name, parent=parent).pandas(df, val)