from yabadaba.record import Record

from DataModelDict import DataModelDict as DM

raise NotImplementedError('BadRecord is meant to fail import!')
class BadRecord(Record):
    """
    Class for representing FAQ (frequently asked question) records.
    """
    @property
    def style(self):
        """str: The record style"""
        return 'BadRecord'

    @property
    def modelroot(self):
        """str: The root element of the content"""
        return 'bad-record'

    def load_model(self, model, name=None):
        """
        Loads record contents from a given model.

        Parameters
        ----------
        model : str or DataModelDict
            The model contents of the record to load.
        name : str, optional
            The name to assign to the record.  Often inferred from other
            attributes if not given.
        """
        super().load_model(model, name=name)

        bad = self.model[self.modelroot]

    def set_values(self, name=None):
        """
        Set multiple object attributes at the same time.

        Parameters
        ----------
        name : str, optional
            The name to assign to the record.  Often inferred from other
            attributes if not given.
        """
        if name is not None:
            self.name = name

    def build_model(self):
        """
        Generates and returns model content based on the values set to object.
        """
        model = DM()
        model['bad'] = DM()

        self._set_model(model)
        return model

    def metadata(self):
        """
        Generates a dict of simple metadata values associated with the record.
        Useful for quickly comparing records and for building pandas.DataFrames
        for multiple records of the same style.
        """
        meta = {}
        meta['name'] = self.name
        return meta