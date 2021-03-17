"""Unit tests for secrets.py"""

import unittest

from unittest.mock import patch
from src.demo_module.demo_module import DemoModule
from .mocks import MockToniq, MockStore, MockSecrets

# pylint: disable=arguments-differ
class SecretsTest(unittest.TestCase):
  """Unit tests for demo_module.py"""

  @patch('toniq.Secrets', autospec=True)
  @patch('toniq.Store', autospec=True)
  @patch('toniq.Toniq', autospec=True)
  def setUp(self, mock_toniq, mock_store, mock_secrets):
    mock_toniq.return_value = MockToniq()
    mock_store.return_value = MockStore()
    mock_secrets.return_value = MockSecrets()
    self.dm = DemoModule()

  def test_write_patients(self):
    """Tests for writing a data table of patient information"""
    self.dm.write_patients()
    #Object bellow had no assert call
    self.dm.spark.createDataFrame.assert_called()
    self.dm.store.write_table.assert_called()

  def test_run_patients(self):
    """Tests for loading a data table and running a SQL query"""
    self.dm.run_patients()
    #Objects bellow had no assert call
    self.dm.store.load_table.assert_called()
    self.dm.spark.sql.assert_called()
