"""
Setup file to install the Toniq Demo Module.
"""

import setuptools

from src.demo_module import __version__

setuptools.setup(
  name="toniq-demo-module",
  version=__version__,
  author="Axel Sly, Andres Rodriguez",
  author_email="axel@doc.ai, andres@doc.ai",
  description="Toniq Demo Module",
  package_dir={"": "src"},
  packages=setuptools.find_packages(where="src", include="demo_module"),
  classifiers=[
    "Programming Language :: Python :: 3",
    "Operating System :: OS Independent",
  ],
  install_requires=[
    "pandas",
    "presto-python-client",
    "streamlit"
  ],
  python_requires='>=3.6'
)
