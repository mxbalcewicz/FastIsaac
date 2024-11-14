import factory

from app.models.user_models import User


class UserFactory(factory.alchemy.SQLAlchemyModelFactory):
    class Meta:
        model = User
        sqlalchemy_session_persistence = "commit"

    email = factory.Faker("email")
    username = factory.Faker("word")
    password = factory.Faker("password")
