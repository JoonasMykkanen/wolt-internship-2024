from fastapi.testclient import TestClient
from datetime import datetime
from datetime import timezone
from app import create_app
import pytest

app = create_app()
client = TestClient(app)

@pytest.mark.parametrize("input, expected", [
    # Testing small order surcharge with a Friday rush hour fee increase
    ({"cart_value": 890, "delivery_distance": 1000, "number_of_items": 4, "time": datetime(2024, 1, 25, 16, 0, tzinfo=timezone.utc).isoformat()}, 310),
    
    # Testing delivery distance fee (just below and at the threshold)
    ({"cart_value": 5000, "delivery_distance": 1499, "number_of_items": 4, "time": datetime(2024, 1, 25, 16, 0, tzinfo=timezone.utc).isoformat()}, 300),
    ({"cart_value": 5000, "delivery_distance": 1500, "number_of_items": 4, "time": datetime(2024, 1, 25, 16, 0, tzinfo=timezone.utc).isoformat()}, 300),
    
    # Testing delivery distance fee (just over the threshold)
    ({"cart_value": 5000, "delivery_distance": 1501, "number_of_items": 4, "time": datetime(2024, 1, 25, 16, 0, tzinfo=timezone.utc).isoformat()}, 400),
    
    # Testing extra items surcharge (at the threshold and above)
    ({"cart_value": 5000, "delivery_distance": 1000, "number_of_items": 5, "time": datetime(2024, 1, 25, 16, 0, tzinfo=timezone.utc).isoformat()}, 250),
    ({"cart_value": 5000, "delivery_distance": 1000, "number_of_items": 10, "time": datetime(2024, 1, 25, 16, 0, tzinfo=timezone.utc).isoformat()}, 500),
    
    # Testing bulk fee for more than 12 items
    ({"cart_value": 5000, "delivery_distance": 1000, "number_of_items": 13, "time": datetime(2024, 1, 25, 16, 0, tzinfo=timezone.utc).isoformat()}, 770),
    ({"cart_value": 5000, "delivery_distance": 1000, "number_of_items": 14, "time": datetime(2024, 1, 25, 16, 0, tzinfo=timezone.utc).isoformat()}, 820),
    
    # Testing max delivery fee cap
    ({"cart_value": 500, "delivery_distance": 3000, "number_of_items": 20, "time": datetime(2024, 1, 25, 16, 0, tzinfo=timezone.utc).isoformat()}, 1500),
    
    # Testing free delivery for cart value >= 200€
    ({"cart_value": 20000, "delivery_distance": 1000, "number_of_items": 4, "time": datetime(2024, 1, 25, 16, 0, tzinfo=timezone.utc).isoformat()}, 0),
    
    # Testing Friday rush hour fee increase on a different day
    ({"cart_value": 5000, "delivery_distance": 1000, "number_of_items": 4, "time": datetime(2024, 1, 26, 16, 0, 0, tzinfo=timezone.utc).isoformat()}, 240),
	({"cart_value": 5000, "delivery_distance": 1000, "number_of_items": 4, "time": datetime(2024, 1, 26, 15, 0, 0, tzinfo=timezone.utc).isoformat()}, 240),
	({"cart_value": 5000, "delivery_distance": 1000, "number_of_items": 4, "time": datetime(2024, 1, 26, 19, 0, 0, tzinfo=timezone.utc).isoformat()}, 240),
	
	({"cart_value": 5000, "delivery_distance": 1000, "number_of_items": 4, "time": datetime(2024, 1, 26, 14, 59, 0, tzinfo=timezone.utc).isoformat()}, 200),
	({"cart_value": 5000, "delivery_distance": 1000, "number_of_items": 4, "time": datetime(2024, 1, 26, 20, 0, 0, tzinfo=timezone.utc).isoformat()}, 200),
    
    # Testing minimum delivery fee (when distance is less than 1km)
    ({"cart_value": 5000, "delivery_distance": 999, "number_of_items": 4, "time": datetime(2024, 1, 25, 16, 0, tzinfo=timezone.utc).isoformat()}, 200),
	({"cart_value": 5000, "delivery_distance": 1, "number_of_items": 1, "time": datetime(2024, 1, 25, 16, 0, tzinfo=timezone.utc).isoformat()}, 200),
    
    # Testing a very large distance, checking the max cap
    ({"cart_value": 5000, "delivery_distance": 100000, "number_of_items": 4, "time": datetime(2024, 1, 25, 16, 0, tzinfo=timezone.utc).isoformat()}, 1500),
])
def test_valid_inputs(input, expected):
	response = client.post('/api/delivery_fee', json=input)

	assert response.status_code == 200

	delivery_fee = response.json()[0]

	assert delivery_fee == {'delivery_fee': f'{expected}'}



@pytest.mark.parametrize("input, expected_status", [
    ({"cart_value": -100, "delivery_distance": 1000, "number_of_items": 4, "time": datetime(2024, 1, 25, 16, 0, tzinfo=timezone.utc).isoformat()}, 422),
    ({"cart_value": 100, "delivery_distance": -100, "number_of_items": 4, "time": datetime(2024, 1, 25, 16, 0, tzinfo=timezone.utc).isoformat()}, 422),
    ({"cart_value": 100, "delivery_distance": 1200, "number_of_items": -5, "time": datetime(2024, 1, 25, 16, 0, tzinfo=timezone.utc).isoformat()}, 422),
    ({"cart_value": 100, "delivery_distance": 1200, "number_of_items": -5, "time": 123123}, 422),

    ({"cart_value": 100, "delivery_distance": 1200, "number_of_items": -5, "time": "Tue, 25 Jan 2024 15:00:00 +0000"}, 422),
    ({"cart_value": 100, "delivery_distance": 1200, "number_of_items": -5, "time": 1703748000}, 422),

    ({"message": "wrong input"}, 422),

    ({}, 422),
])
def test_invalid_inputs(input, expected_status):
    response = client.post('/api/delivery_fee', json=input)
	
    assert response.status_code == expected_status