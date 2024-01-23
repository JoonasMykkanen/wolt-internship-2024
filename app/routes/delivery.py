from pydantic import field_validator
from pydantic import BaseModel
from datetime import datetime
from datetime import timezone
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
	
	# Checking that the request is not too old
	@field_validator('time')
	def test_time(cls, value):
		current_time = datetime.now(timezone.utc)
		input_time = value
		
		# NOTE: after looking into it, if input would be "time": "2024-01-15T13:00:00"
		# it would still comply with ISO 8601 and be valid input but without timezone
		# information, will fix it here since default was UTC
		if input_time.tzinfo == None:
			input_time = value.replace(tzinfo=timezone.utc)

		if input_time > current_time:
			raise ValueError('Timestamp cannot be in future.. Timetravel not allowed!')

		delta = current_time - input_time
		if delta.days >= 1:
			raise ValueError(f'Request too old, server time {current_time}')

		return input_time



delivery_router = APIRouter()

# 1) Takes request body and passes it into Pydantic model 'Data' for validation
# 2) If the input is valid, it will pass it to the calculate_fee function
# 3) assuming no errors, it will return the calculated delivery fee
#
# RETURNS: delivery_fee (int) or error message (str)
@delivery_router.post('/')
def handle_delivery_fee(data: Data):
	try:
		fee = calculate_fee(data)
		return {'delivery_fee': f'{fee}'}, 200

	except Exception as e:
		print(f'Error: {e}')
		return {'message': 'internal server error'}, 500