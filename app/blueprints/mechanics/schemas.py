from app.extensions import ma
from app.models import Mechanics

class MechanicSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Mechanics

mechanic_schema = MechanicSchema()
mechanics_schema = MechanicSchema(many=True)
login_mechanic_schema = MechanicSchema(only=['email', 'password'])