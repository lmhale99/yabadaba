from yabadaba.record import Record
from yabadaba import load_value

class FAQ(Record):
    """
    Class for representing FAQ (frequently asked question) records.
    """

    ########################## Basic metadata fields ##########################

    @property
    def style(self):
        """str: The record style"""
        return 'FAQ'

    @property
    def modelroot(self):
        """str: The root element of the content"""
        return 'faq'
    
    @property
    def xsl_filename(self):
        """tuple: The module path and file name of the record's xsl html transformer"""
        return ('yabadaba_demo.xsl', 'FAQ.xsl')

    @property
    def xsd_filename(self):
        """tuple: The module path and file name of the record's xsd schema"""
        return ('yabadaba_demo.xsd', 'FAQ.xsd')

    ############################# Define Values  ##############################

    def _init_values(self):
        """
        Method that defines the value objects for the Record.  This should
        call the super of this method, then use self._add_value to create new Value objects.
        Note that the order values are defined matters
        when build_model is called!!!
        """
        self._add_value('longstr', 'question')
        self._add_value('longstr', 'answer')