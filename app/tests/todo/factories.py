import factory
from factory.alchemy import SQLAlchemyModelFactory
from app.models import Todo


class TodoFactory(SQLAlchemyModelFactory):
    class Meta:
        model = Todo
        sqlalchemy_session = None
        sqlalchemy_session_persistence = None

    title = factory.Faker("word")
    description = factory.Faker("paragraph")
