from .DateMatchQuery import DateMatchQuery

# Define legacy functions

def description():
    return DateMatchQuery().description

def mongo(qdict, path, val):
    DateMatchQuery(path=path).mongo(qdict, val)

def pandas(df, name, val, parent=None):
    return DateMatchQuery(name=name, parent=parent).pandas(df, val)