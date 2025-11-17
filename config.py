class DevelopmentConfig:
  SQLALCHEMY_DATABASE_URI = 'sqlite:///Bagel_Repairs.db'#can rename the database anything. Developement makes sense
  DEBUG = True
  
  
class TestingConfig:
  pass


class ProductionConfig:
    pass