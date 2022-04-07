from .scheduller import *
from .schedule import *
from .core import *
from .config import *
from .example import example

# Clean up old temporary files.
config().auto_clean() 

# Check if the AstroScheduller Core File is Valid
core().check_integrity()