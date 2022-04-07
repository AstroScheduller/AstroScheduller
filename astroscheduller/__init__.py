from .scheduller import *
from .schedule import *
from .core import *
from .config import *
from .example import example

# Clean up old temporary files.
config().auto_clean() 

# Update Core Config
core().get_core_info()

# Check if the AstroScheduller Core File is Valid
core().check_integrity()