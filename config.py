class DevelopmentConfig:
  SQLALCHEMY_DATABASE_URI = 'sqlite:///Bagel_Repairs.db'#can rename the database anything. Developement makes sense
  DEBUG = True
  CACHE_TYPE = "SimpleCache"
  CACHE_DEFAULT_TIMEOUT = 300
  
class TestingConfig:
  pass


class ProductionConfig:
    pass