"""System checking module."""
# stand lib
import os


 def ismac() -> bool:
     return os.uname().sysname == "Darwin"


 def ispi() -> bool:
     return os.uname().sysname == "Linux"
