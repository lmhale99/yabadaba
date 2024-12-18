from yabadaba.record import Record
from yabadaba import load_value

class Album(Record):
    """
    Class for representing a music album.
    """

    ########################## Basic metadata fields ##########################

    @property
    def style(self):
        """str: The record style"""
        return 'album'

    @property
    def modelroot(self):
        """str: The root element of the content"""
        return 'album'
    

    ############################# Define Values  ##############################

    def _init_values(self):
        """
        Method that defines the value objects for the Record.  This should
        call the super of this method, then use self._add_value to create new Value objects.
        Note that the order values are defined matters
        when build_model is called!!!
        """
        self._add_value('str', 'title')
        self._add_value('longstr', 'artist')
        self._add_value('date', 'releasedate')
        self._add_value('strlist', 'keyword')

        self._add_value('int', 'numtracks')
        self._add_value('bool', 'settings.reverb', defaultvalue=False)
        self._add_value('float', 'settings.frequency', unit='kHz')

        self._add_value('longstr', 'description')



    def _init_value_objects(self) -> list:
        """
        Method that defines the value objects for the Record.  This should
        1. Call the method's super() to get default Value objects.
        2. Use yabadaba.load_value() to build Value objects that are set to
           private attributes of self.
        3. Append the list returned by the super() with the new Value objects.

        Returns
        -------
        value_objects: A list of all value objects.
        """
        value_objects = super()._init_value_objects()

        self.__intval = load_value('int', 'intval', self,
                                   defaultvalue = 6,
                                   modelpath = 'settings.intval')
        value_objects.append(self.__intval)

        self.__floatval = load_value('float', 'floatval', self, 
                                     defaultvalue = 0.0,
                                     modelpath = 'settings.floatval')
        value_objects.append(self.__floatval)
        
        self.__option = load_value('str', 'option', self,
                                   defaultvalue = 'a',
                                   allowedvalues = ['a', 'b', 'c'],
                                   modelpath = 'settings.option')
        value_objects.append(self.__option)

        self.__length = load_value('float', 'length', self,
                                   defaultvalue = '1.0 nm',
                                   modelunit = 'nm')
        value_objects.append(self.__length)
        
        self.__notes = load_value('longstr', 'notes',self)
        value_objects.append(self.__notes)

        return value_objects

    @property
    def intval(self) -> int:
        """int: An int value."""
        return self.__intval.value

    @intval.setter
    def intval(self, val: int):
        self.__intval.value = val

    @property
    def floatval(self) -> float:
        """float: A float value."""
        return self.__floatval.value

    @floatval.setter
    def floatval(self, val: float):
        self.__floatval.value = val

    @property
    def option(self) -> str:
        """str: A simple str option value."""
        return self.__option.value

    @option.setter
    def option(self, val: str):
        self.__option.value = val

    @property
    def length(self) -> float:
        """float: A length value demonstrating unit conversions."""
        return self.__length.value

    @length.setter
    def length(self, val: float):
        self.__length.value = val

    @property
    def notes(self) -> str:
        """str: A long/complex notes str."""
        return self.__notes.value

    @notes.setter
    def notes(self, val: str):
        self.__notes.value = val
