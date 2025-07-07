import uuid

def is_uuid(val: str,
            strict: bool = True) -> bool:
    """
    Test if a str is a UUID key

    Parameters
    ----------
    val : str
        The value to check.
    strict : bool, optional
        If True (default), then the check requires val to be in the format
        'xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx', where all x are in
        [0123456789abcdef].  If False, then any str representation recognizable
        by uuid.UUID is considered.

    Returns
    -------
    bool
        True if val is recognized as a UUID key, False otherwise
    """
    
    if strict is True:
        
        # Check len of val and - locations
        if (len(val) != 36 or
            val[8] != '-' or
            val[13] != '-' or
            val[18] != '-' or
            val[23] != '-'):
            return False
        
        # Remove - and check len again
        hex = val.replace('-', '')
        if len(hex) != 32:
            return False

        # Check if remaining str is a hex number
        try:
            int(hex, 16)
        except ValueError:
            return False
        return True

    elif strict is False:
        
        # Check if val is any valid UUID
        try:
            uuid.UUID(val)
        except ValueError:
            return False
        return True
    
    else:
        raise TypeError('strict must be bool')