# coding: utf-8

# Relative imports
from ..tools import iaslist
from .Query import Query

class ListContainsQuery(Query):
    """Class for querying list fields for contained values"""

    @property
    def style(self):
        """str: The query style"""
        return 'list_contains'

    @property
    def description(self):
        """str: Describes the query operation that the class performs."""
        return 'Query a str field for containing specific values'

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
            if '$and' not in querydict:
                querydict['$and'] = []
            for v in iaslist(value):
                querydict['$and'].append({self.path:v})

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
                for v in iaslist(value):
                    if v not in series[name]:
                        return False
                return True
            
            else:
                for p in iaslist(series[parent]):
                    if name in p:
                        for v in iaslist(value):
                            if v not in p[name]:
                                return False
                        return True
                    else:
                        return False

        return df.apply(apply_function, axis=1, args=(self.name, value, self.parent))

# Define legacy functions

def description():
    return ListContainsQuery().description

def mongo(qdict, path, val):
    ListContainsQuery(path=path).mongo(qdict, val)

def pandas(df, name, val, parent=None):
    return ListContainsQuery(name=name, parent=parent).pandas(df, val)
