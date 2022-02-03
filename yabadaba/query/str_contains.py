from .StrContainsQuery import StrContainsQuery
# Define legacy functions

def description():
    return StrContainsQuery().description

def mongo(qdict, path, val):
    StrContainsQuery(path=path).mongo(qdict, val)

def pandas(df, name, val, parent=None):
    return StrContainsQuery(name=name, parent=parent).pandas(df, val)
