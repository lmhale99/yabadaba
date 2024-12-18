from yabadaba.record import Record

class Track(Record):

    ########################## Basic metadata fields ##########################

    @property
    def style(self):
        """str: The record style"""
        return 'track'

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
        self._add_value('str', 'title')
        self._add_value('int', 'number')
        self._add_value('strlist', 'keyword')

        self._add_value('bool', 'settings.reverb', defaultvalue=False)
        self._add_value('float', 'settings.frequency', unit='kHz')

        self._add_value('longstr', 'description')

        
        self._add_value('floatarray', 'notes')