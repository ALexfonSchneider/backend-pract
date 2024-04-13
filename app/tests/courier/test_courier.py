from uuid import UUID
from httpx import AsyncClient
from src.routers.courier import schemes

async def test_registration(client: AsyncClient):
    response = await client.post('/curier/', json=schemes.CourierRegistration(
        name="Alex",
        districts=['Павловская', 'Ржевская']
    ).model_dump())
    
    assert response.status_code == 201, f'unexpected response'


async def test_courieres(client: AsyncClient):
    response = await client.get('/curier/')    
    assert response.status_code == 200, f'unexpected response'


# async def test_courier_detail(client: AsyncClient):
    # create user
    # response = await client.post('/curier/', json=schemes.CourierRegistration(
    #     name="Alex",
    #     districts=['Павловская', 'Ржевская']
    # ).model_dump())
    
    # assert response.status_code == 201, f'create courier. unexpected response'
    
    # recived_data = response.json()
    # id: str = recived_data['id']
    
    # # get created user info
    # response = await client.get(f'/curier/{str(id)}/')
    # assert response.status_code == 200, f'get courier info detail. unexpected response'
    
    # recived_data = response.json()
    # assert recived_data['name'] == "Alex", "unexpected user"