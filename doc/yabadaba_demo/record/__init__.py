from yabadaba import recordmanager

# Manually install records to recordmanager

# from .FAQ import FAQ as the 'FAQ' record style
recordmanager.import_style('FAQ', '.FAQ', __name__, 'FAQ')

# from .album import Album as the 'album' record style
recordmanager.import_style('album', '.album', __name__, 'Album')

# from .bad_record import BadRecord as the 'bad_record' style - which will be caught as an error
recordmanager.import_style('bad_record', '.bad_record', __name__, 'BadRecord')