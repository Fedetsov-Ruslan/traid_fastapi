from httpx import AsyncClient


async def test_add_specific_operation(ac: AsyncClient):
    response = await ac.post("/operations", json={
        "id":1,
        "quantity": "20",
        "figi": "figi_CODE",
        "instrument_type": "bond",
        "date": "2022-01-01T00:00:00",
        "type": "выплота купонов"
    }, follow_redirects=False)
    assert response.status_code == 200


async def  test_get_specific_operations(ac: AsyncClient):
    response = await ac.get("/operations", params={"operation type": "выплота купонов"}, follow_redirects=False)


    assert response.status_code == 200
    assert response.json()["status"] == "success"
    assert len(response.json()["data"]) == 1