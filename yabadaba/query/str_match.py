from .StrMatchQuery import StrMatchQuery

# Define legacy functions

def description():
    return StrMatchQuery().description

def mongo(qdict, path, val):
    StrMatchQuery(path=path).mongo(qdict, val)

def pandas(df, name, val, parent=None):
    return StrMatchQuery(name=name, parent=parent).pandas(df, val)