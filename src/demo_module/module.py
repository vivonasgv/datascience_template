"""Base Module definition file"""

import prestodb
import toniq

class ToniqEnvManager:
  """Base Module class that initiallizes all the Toniq clients"""
  def __init__(self, provider='gcp'):
    self.tq = toniq.Toniq()
    self.tq.authenticate()
    self.store = toniq.Store(client=self.tq)
    self.secrets = toniq.Secrets(provider=provider)
    self.conn = prestodb.dbapi.connect(
      host='toniq-presto',
      port=8080,
      schema='default',
      catalog='hive',
      user='any'
    )
    self.cur = self.conn.cursor()
