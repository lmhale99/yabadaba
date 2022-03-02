from .ListContainsQuery import ListContainsQuery

# Define legacy functions

def description():
    return ListContainsQuery().description

def mongo(qdict, path, val):
    ListContainsQuery(path=path).mongo(qdict, val)

def pandas(df, name, val, parent=None):
    return ListContainsQuery(name=name, parent=parent).pandas(df, val)
