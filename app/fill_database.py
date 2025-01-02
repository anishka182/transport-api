import requests
import random
from faker import Faker

API_BASE_URL = "http://127.0.0.1:8000"
fake = Faker()


def generate_random_transport_type():
    return {
        "name": fake.word(),
        "avg_speed": round(random.uniform(10.0, 150.0), 2),
        "fleet_size": random.randint(1, 100),
        "fuel_consumption": round(random.uniform(5.0, 100.0), 2),
    }

def generate_random_route():
    return {
        "route_number": random.randint(1, 1000),
        "daily_passenger_count": random.randint(100, 1000),
        "fare": round(random.uniform(1.0, 5.0), 2),
        "num_vehicles_on_route": random.randint(1, 10),
    }

def generate_random_path():
    return {
        "starting_point": fake.city(),
        "end_point": fake.city(),
        "num_stops": random.randint(1, 10),
        "distance": round(random.uniform(5.0, 100.0), 2),
    }


def add_transport_type(data):
    response = requests.post(f"{API_BASE_URL}/transport-types/", json=data)
    if response.status_code == 200:
        print(f"Transport type {data['name']} added successfully.")
    else:
        print(f"Failed to add transport type {data['name']}.")

def add_route(data):
    response = requests.post(f"{API_BASE_URL}/routes/", json=data)
    if response.status_code == 200:
        print(f"Route {data['route_number']} added successfully.")
    else:
        print(f"Failed to add route {data['route_number']}.")

def add_path(data):
    response = requests.post(f"{API_BASE_URL}/paths/", json=data)
    if response.status_code == 200:
        print(f"Path from {data['starting_point']} to {data['end_point']} added successfully.")
    else:
        print(f"Failed to add path from {data['starting_point']} to {data['end_point']}.")


def fill_database(num_entries=1000):
    
    for _ in range(num_entries):
        transport = generate_random_transport_type()
        add_transport_type(transport)
    
    
    for _ in range(num_entries):
        route = generate_random_route()
        route['transport_type_id'] = random.choice([1, 2, 3, 4, 5])  
        add_route(route)

    
    for _ in range(num_entries):
        path = generate_random_path()
        path['route_id'] = random.choice([1, 2, 3, 4, 5]) 
        add_path(path)

if __name__ == "__main__":
    fill_database(1000)  
