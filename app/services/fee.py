from ..utils.constants import *

def calculate_fee(data):
	# Early return if cart more than 200€
	if data.cart_value >= FREE_DELIVERY_LIMIT:
		return FREE_DELIVERY

	# Iterate over each possible rule for fees and add sum them up
	fee = 0
	fee = add_surcharge(data.cart_value, fee)
	fee = price_in_distance(data.delivery_distance, fee)
	fee = item_fees(data.number_of_items, fee)
	fee = rush_multiplier(data.time, fee)

	# If went over the max limit, return max fee (15€)
	# If calculating price would take some heavier math
	# it should be checked before each function not to do
	# any extra work but it would compromise clean code a bit
	if fee > MAX_FEE:
		return MAX_FEE
	
	return round(fee)


def add_surcharge(cart_value, fee):
	if cart_value < SMALL_ORDER:
		fee += SMALL_ORDER - cart_value

	return fee


# NOTE: readme has toughts on this function and it's original implementation
def price_in_distance(distance, fee):
	fee += FIRST_KM_FEE
	remaining_distance = distance - 1000
	
	if remaining_distance > 0:
		count = max(0, (remaining_distance + 499) // 500)
		fee += count * FEE_PER_500M
	
	return fee


def item_fees(count, fee):
	if count < BIG_ORDER:
		return fee
	
	for i in range(BIG_ORDER, (count + 1)):
		fee += ITEM_FEE
	
	if count >= BULK_ORDER:
		fee += BULK_FEE
	
	return fee


def rush_multiplier(time, fee):
	if time.weekday() != FRIDAY:
		return fee
	
	if time.hour in range(RUSH_HOUR_START, RUSH_HOUR_END):
		fee *= 1.2

	return fee