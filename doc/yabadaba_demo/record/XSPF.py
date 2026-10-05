from yabadaba.record import Record

class XSPFTrack(Record):
    """yabadaba translator for XSPF playlist track elements"""

    ########################## Basic metadata fields ##########################

    @property
    def style(self):
        """str: The record style"""
        return 'xspf_track'

    @property
    def modelroot(self):
        """str: The root element of the content"""
        return 'track'

    ############################# Define Values  ##############################
    
    def _init_values(self):
        """
        Method that defines the value objects for the Record.  This should
        call the super of this method, then use self._add_value to create new Value objects.
        Note that the order values are defined matters
        when build_model is called!!!
        """
        self._add_value('str', 'location', description='file path or URL where the track can be found')
        self._add_value('str', 'title', description='name of the track')
        self._add_value('str', 'creator', description="name of the entity that created the track (author, artist, etc.)")
        self._add_value('str', 'album', description='name of the collection from which the track originated')


class XSPF(Record):
    """yabadaba translator of XSPF playlist files"""

    ########################## Basic metadata fields ##########################

    @property
    def style(self):
        """str: The record style"""
        return 'xspf'

    @property
    def modelroot(self):
        """str: The root element of the content"""
        return 'playlist'

    ############################# Define Values  ##############################

    def _init_values(self):
        """
        Method that defines the value objects for the Record.  This should
        call the super of this method, then use self._add_value to create new Value objects.
        Note that the order values are defined matters
        when build_model is called!!!
        """
        self._add_value('longstr', 'title', description='name of the playlist')
        self._add_value('str', 'creator', description='name of the person who created the playlist')
        self._add_value('recordlist', 'track', recordclass=XSPFTrack,
                        description='the list of tracks')
