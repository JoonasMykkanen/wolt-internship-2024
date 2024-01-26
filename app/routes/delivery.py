from pydantic import field_validator
from fastapi import HTTPException
from pydantic import BaseModel
from datetime import datetime
from fastapi import APIRouter

from ..services.fee import calculate_fee

class Data(BaseModel):
	cart_value: int
	delivery_distance: int
	number_of_items: int
	time: datetime

	@field_validator('cart_value')
	def test_cart(cls, value):
		if value < 0:
			raise ValueError('cart_value cannot be lower than zero (0)')
		return value

	@field_validator('delivery_distance')
	def test_distance(cls, value):
		if 	value < 0:
			raise ValueError('distance cannot be lower than zero (0)')
		return value

	@field_validator('number_of_items')
	def test_items(cls, value):
		if value <= 0:
			raise ValueError('number_of_items cannot be equal to or lower than zero (0)')
		return value
	


delivery_router = APIRouter()

# 1) Takes request body and passes it into Pydantic model 'Data' for validation
# 2) If the input is valid, it will pass it to the calculate_fee function
# 3) assuming no errors, it will return the calculated delivery fee
#
# RETURNS: delivery_fee (int) or error message (str)
# NOTE: Except will catch anything that Pydantic HTTPExecption does not
@delivery_router.post('/delivery-fee', status_code=200)
def handle_delivery_fee(data: Data):
	try:
		fee = calculate_fee(data)
		return {'delivery_fee': f'{fee}'}

	except Exception as e:
		print(f'Error during POST handling: {e}')
		raise HTTPException(status_code=500, detail="internal server error")