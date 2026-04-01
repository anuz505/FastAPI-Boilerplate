import uuid
from app.models import Todo
from app.tests.todo.factories import TodoFactory
import pytest
from sqlalchemy import String


class TestTodoModel:
    def test_creation(self, todo):
        assert todo.id is not None
        assert todo.title
        assert todo.description

    def test_uuid_primary_key(self, todo):
        assert isinstance(todo.id, uuid.UUID)

    def test_todo_fixture(self, todo):
        assert todo.id is not None

    def test_timestamps_populated(self, todo):
        assert todo.created_at is not None
        assert todo.updated_at is not None

    def test_description_nullable(self, db):
        TodoFactory._meta.sqlalchemy_session = db

        assert TodoFactory(description=None).description is None

    def test_batch_ids_are_unique(self, db):
        TodoFactory._meta.sqlalchemy_session = db
        ids = [t.id for t in TodoFactory.create_batch(5)]
        assert len(ids) == 5

    def test_max_length(self, db):
        TodoFactory._meta.sqlalchemy_session = db

    @pytest.mark.parametrize(
        "field,max_length",
        [
            ("title", 255),
            ("description", 255),
        ],
    )
    def test_field_max_length(self, field, max_length, db):
        TodoFactory._meta.sqlalchemy_session = db

        column = Todo.__table__.columns[field]
        assert isinstance(column.type, String)
        assert column.type.length == max_length
