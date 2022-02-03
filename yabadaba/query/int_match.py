from .IntMatchQuery import IntMatchQuery
# Define legacy functions

def description():
    return IntMatchQuery().description

def mongo(qdict, path, val):
    IntMatchQuery(path=path).mongo(qdict, val)

def pandas(df, name, val, parent=None):
    return IntMatchQuery(name=name, parent=parent).pandas(df, val)