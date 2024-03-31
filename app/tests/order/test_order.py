from httpx import AsyncClient
from src.routers.courier.schemes import CourierRegistration 
from src.routers.order.schemes import NewOrder

async def test_make_order(client: AsyncClient):
    response = await client.post('/curier/', json=CourierRegistration(
        name="Alex",
        districts=['test', 'Ржевская']
    ).model_dump())
    assert response.status_code == 201, f'unexpected response'
    
    response = await client.post('/order/', json=NewOrder(
        name="test",
        district="test"
    ).model_dump())
    assert response.status_code == 200, f'unexpected response'
    
    
async def test_get_order(client: AsyncClient):
    response = await client.post('/curier/', json=CourierRegistration(
        name="Alex",
        districts=['test', 'Ржевская']
    ).model_dump())
    assert response.status_code == 201, f'unexpected response'
    
    response = await client.post('/order/', json=NewOrder(
        name="test",
        district="test"
    ).model_dump())
    assert response.status_code == 200, f'unexpected response'
    
    recived_data = response.json()
    order_id = recived_data['order_id']
    
    response = await client.get(f'/order/{order_id}')
    assert response.status_code == 200, f'unexpected response'
    

async def test_close_order(client: AsyncClient):
    response = await client.post('/curier/', json=CourierRegistration(
        name="Alex",
        districts=['test', 'Ржевская']
    ).model_dump())
    assert response.status_code == 201, f'unexpected response'
    
    response = await client.post('/order/', json=NewOrder(
        name="test",
        district="test"
    ).model_dump())
    assert response.status_code == 200, f'unexpected response'
    
    recived_data = response.json()
    order_id = recived_data['order_id']
    
    response = await client.get(f'/order/{order_id}')
    assert response.status_code == 200, f'unexpected response'
    
    response = await client.put(f'/order/{order_id}/close')
    assert response.status_code == 200, f'unexpected response'
    
    