"""
Toniq Demo Module package version
"""

import os
import pathlib

file_path = pathlib.Path(__file__).parent.absolute()

with open(os.path.join(file_path, '..', '..', 'VERSION')) as version_file:
  version = version_file.read().strip()

__version__ = version
