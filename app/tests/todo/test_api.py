import pytest
from httpx import AsyncClient

base_URL = "http://localhost:8000"


@pytest.mark.asyncio
async def test_read_todo():
    async with AsyncClient(base_url=base_URL) as client:
        res = await client.get("/todo/")
        assert res.status_code == 200


@pytest.mark.asyncio
async def test_create_todo(db):
    payload = {"title": "Async test blah blah", "description": "whatever"}
    async with AsyncClient(base_url=base_URL) as client:
        res = await client.post("/todo/", json=payload)
        assert res.status_code == 201


@pytest.mark.asyncio
async def test_update_todo(db):
    # First, create a test record
    todo = {"title": "Old Title", "description": "Old Desc"}
    async with AsyncClient(base_url=base_URL) as client:
        create_resp = await client.post("/todo/", json=todo)
        todo_id = create_resp.json()["id"]

        # Now update it
        update_payload = {"title": "Updated Title", "description": "Updated Desc"}
        update_resp = await client.put(f"/todo/{todo_id}", json=update_payload)

    assert update_resp.status_code == 200
    updated_data = update_resp.json()
    assert updated_data["title"] == "Updated Title"


@pytest.mark.asyncio
async def test_delete_todo():
    async with AsyncClient(base_url=base_URL) as client:
        # Create a todo to delete
        create_resp = await client.post("/todo/", json={"title": "To Delete"})
        todo_id = create_resp.json()["id"]

        # Delete it
        delete_resp = await client.delete(f"/todo/{todo_id}")
        assert delete_resp.status_code in (200, 204)

        # Verify it's gone
        get_resp = await client.get(f"/todo/{todo_id}")
        assert get_resp.status_code == 404
