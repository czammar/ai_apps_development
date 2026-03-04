from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from typing import List, Optional
from uuid import uuid4

app = FastAPI(title="Restaurant Chain API")

# Modelos de datos
class RestaurantBase(BaseModel):
    name: str = Field(..., example="Tacos Finos")
    city: str = Field(..., example="Apodaca")
    capacity: int = Field(..., example=50)

class RestaurantCreate(RestaurantBase):
    pass

class RestaurantUpdate(BaseModel):
    name: Optional[str] = None
    city: Optional[str] = None
    capacity: Optional[int] = None

class Restaurant(RestaurantBase):
    id: str

class ClientBase(BaseModel):
    name: str = Field(..., example="César Zamora")
    email: str = Field(..., example="cesar@email.com")
    favorite_restaurant_id: Optional[str] = None

class ClientCreate(ClientBase):
    pass

class ClientUpdate(BaseModel):
    name: Optional[str] = None
    email: Optional[str] = None
    favorite_restaurant_id: Optional[str] = None

class Client(ClientBase):
    id: str


# Estructuras de datos para simular una base de datos
restaurants_db: List[Restaurant] = []
clients_db: List[Client] = []

# Endpoints de la aplicacion
## Restaurantes
@app.post("/restaurants", response_model=Restaurant)
def create_restaurant(restaurant: RestaurantCreate):
    new_restaurant = Restaurant(id=str(uuid4()), **restaurant.dict())
    restaurants_db.append(new_restaurant)
    return new_restaurant

@app.get("/restaurants", response_model=List[Restaurant])
def get_restaurants():
    return restaurants_db

@app.get("/restaurants/{restaurant_id}", response_model=Restaurant)
def get_restaurant(restaurant_id: str):
    for restaurant in restaurants_db:
        if restaurant.id == restaurant_id:
            return restaurant
    raise HTTPException(status_code=404, detail="Restaurant not found")

@app.put("/restaurants/{restaurant_id}", response_model=Restaurant)
def update_restaurant(restaurant_id: str, updated_data: RestaurantCreate):
    for index, restaurant in enumerate(restaurants_db):
        if restaurant.id == restaurant_id:
            updated_restaurant = Restaurant(
                id=restaurant_id, **updated_data.dict()
            )
            restaurants_db[index] = updated_restaurant
            return updated_restaurant
    raise HTTPException(status_code=404, detail="Restaurant not found")


@app.patch("/restaurants/{restaurant_id}", response_model=Restaurant)
def patch_restaurant(restaurant_id: str, updated_data: RestaurantUpdate):
    for restaurant in restaurants_db:
        if restaurant.id == restaurant_id:
            update_data = updated_data.dict(exclude_unset=True)
            for key, value in update_data.items():
                setattr(restaurant, key, value)
            return restaurant
    raise HTTPException(status_code=404, detail="Restaurant not found")


@app.delete("/restaurants/{restaurant_id}")
def delete_restaurant(restaurant_id: str):
    for index, restaurant in enumerate(restaurants_db):
        if restaurant.id == restaurant_id:
            restaurants_db.pop(index)
            return {"message": "Restaurant deleted"}
    raise HTTPException(status_code=404, detail="Restaurant not found")


## Clientes
@app.post("/clients", response_model=Client)
def create_client(client: ClientCreate):
    new_client = Client(id=str(uuid4()), **client.dict())
    clients_db.append(new_client)
    return new_client

@app.get("/clients", response_model=List[Client])
def get_clients():
    return clients_db

@app.get("/clients/{client_id}", response_model=Client)
def get_client(client_id: str):
    for client in clients_db:
        if client.id == client_id:
            return client
    raise HTTPException(status_code=404, detail="Client not found")

@app.put("/clients/{client_id}", response_model=Client)
def update_client(client_id: str, updated_data: ClientCreate):
    for index, client in enumerate(clients_db):
        if client.id == client_id:
            updated_client = Client(
                id=client_id, **updated_data.dict()
            )
            clients_db[index] = updated_client
            return updated_client
    raise HTTPException(status_code=404, detail="Client not found")

@app.patch("/clients/{client_id}", response_model=Client)
def patch_client(client_id: str, updated_data: ClientUpdate):
    for client in clients_db:
        if client.id == client_id:
            update_data = updated_data.dict(exclude_unset=True)
            for key, value in update_data.items():
                setattr(client, key, value)
            return client
    raise HTTPException(status_code=404, detail="Client not found")

@app.delete("/clients/{client_id}")
def delete_client(client_id: str):
    for index, client in enumerate(clients_db):
        if client.id == client_id:
            clients_db.pop(index)
            return {"message": "Client deleted"}
    raise HTTPException(status_code=404, detail="Client not found")