DEBUG=True

if not DEBUG:
	from settings_production import *
else:
	from settings_local import *