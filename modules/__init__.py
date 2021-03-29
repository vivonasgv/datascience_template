"""
Toniq Demo Module initialization
"""

import warnings

from .version import __version__
from .module import ToniqEnvManager
from .data_manager import DataManager
from .app_utils import *

warnings.filterwarnings('ignore', category=DeprecationWarning)


'''
# if somebody does "from somepackage import *", this is what they will
# be able to access:
__all__ = [
  '__version__',
  'ToniqEnvManager',
  'DataManager'
]
'''