from pydantic import field_validator
from pydantic import BaseModel
from datetime import datetime
from fastapi import APIRouter

from ..services.fee import calculate_fee

# incase of most errors, it will be handled with fastApis HTTPException
# that gets automaticly thrown if Data model is not populated properly
# by request. Rest are taken care of with validators and except block
class Data(BaseModel):
	cart_value: int
	delivery_distance: int
	number_of_items: int
	time: datetime

	# Will accept zero here since with some coupons or other discounts, maaaaybe
	# someone could somehow get order down to zero but definitely not under
	@field_validator('cart_value')
	def test_cart(cls, value):
		if value < 0:
			raise ValueError('cart_value cannot be lower than zero (0)')
		return value


	# would be easy to add max distance like there is in real WOLT APP
	# since delivieries dont run from Helsinki till Oulu.. :(
	@field_validator('delivery_distance')
	def test_distance(cls, value):
		if 	value < 0:
			raise ValueError('distance cannot be lower than zero (0)')
		return value

	# Kinda obvious check isnt it? Has to be something to deliver. Also I guess there could
	# be a cap for this in real world?
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
@delivery_router.post('/delivery_fee')
def handle_delivery_fee(data: Data):
	try:
		fee = calculate_fee(data)
		return {'delivery_fee': f'{fee}'}, 200

	except Exception as e:
		print(f'Error: {e}')
		return {'message': 'internal server error'}, 500