from typing import Literal, Any, TYPE_CHECKING

if TYPE_CHECKING:
    from ..record import Record

from . import valuemanager, Value

def load_value(style: str,
               name: str | None = None,
               record: str | Record | None = None,
               defaultvalue: Any | None = None,
               valuerequired: bool = False,
               allowedvalues: tuple | None = None,
               allowcustomvalue: bool = False,
               metadatakey: str | Literal[False] | None = None,
               metadataparent: str | None = None,
               modelpath: str | Literal[False] | None = None,
               description: str | None = None,
               **kwargs) -> Value:
    """
    Loads a Value subclass associated with a given value style.

    Parameters
    ----------
    style : str
        The value style.
    name : str
        The name for the parameter value.  This should correspond to the name of
        the associated class attribute.
    record : Record, optional
        The Record object that the Parameter is used with.
    defaultvalue : any or None, optional
        The default value to use for the property.  The default value of
        None indicates that there is no default value.
    valuerequired: bool, optional
        Indicates if a value must be given for the property.  If True, then
        checks will be performed that a value is assigned to the property.
    allowedvalues : tuple or None, optional
        A list/tuple of values that the parameter is restricted to have.
        Setting this to None (default) indicates any value is allowed.
    allowcustomvalue : bool, optional
        Determines how allowedvalues is interpreted. If False (default) then
        values are restricted to what is listed in allowedvalues.  If True,
        then the value is not restricted and allowedvalues becomes a list of
        recommended values.
    metadatakey: str, bool or None, optional
        The key name to use for the property when constructing the record
        metadata dict.  If set to None (default) then name will be used for
        metadatakey.  If set to False then the parameter will not be
        included in the metadata dict.
    metadataparent: str or None, optional
        If given, then this indicates that the metadatakey is actually an
        element of a dict in metadata with this name.  This allows for limited
        support for metadata having embedded dicts.
    modelpath: str, optional
        The period-delimited path after the record root element for
        where the parameter will be found in the built data model.  If set
        to None (default) then name will be used for modelpath.
    description: str or None, optional
        A short description for the value.  If not given, then the record name
        will be used.
    **kwargs : any, optional
        Any additional style-specific keyword parameters.
    """
    return valuemanager.init(style, name=name, record=record, 
                             defaultvalue=defaultvalue,
                             valuerequired=valuerequired,
                             allowedvalues=allowedvalues,
                             allowcustomvalue=allowcustomvalue,
                             metadatakey=metadatakey,
                             metadataparent=metadataparent,
                             modelpath=modelpath, 
                             description=description, **kwargs)
