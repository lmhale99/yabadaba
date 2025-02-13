import datetime

from yabadaba.value import Value
import pandas as pd

class TimeDeltaValue(Value):
    """Value object for time segments"""

    def set_value_mod(self, val):
        
        # Check if value is in #text
        val = self.set_value_mod_textfield(val)
        
        if val is None:
            return None
        elif not isinstance(val, datetime.timedelta):
            val = pd.to_timedelta(val)
        return val

    def build_model_value(self):
        return str(self.value)
