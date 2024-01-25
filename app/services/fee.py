from ..utils.constants import *

price = 0

def calculate_fee(data):
	global price
	price = 0

	# Early return if cart more than 200€
	if data.cart_value >= FREE_DELIVERY_LIMIT:
		return FREE_DELIVERY

	# Iterate over each possible rule for fees and add sum them up
	add_surcharge(data.cart_value)
	price_in_distance(data.delivery_distance)
	item_fees(data.number_of_items)
	rush_multiplier(data.time)

	# If went over the max limit, return max fee (15€)
	# If calculating price would take some heavier math
	# it should be checked before each function not to do
	# any extra work but it would compromise clean code a bit
	if price > MAX_FEE:
		return MAX_FEE
	
	return round(price)



def add_surcharge(cart_value):
	global price
	
	if cart_value < SMALL_ORDER:
		price += SMALL_ORDER - cart_value


# NOTE: readme has toughts on this function and it's original implementation
def price_in_distance(distance):
	global price
	
	price += FIRST_KM_FEE
	remaining_distance = distance - 1000
	
	if remaining_distance > 0:
		count = max(0, (remaining_distance + 499) // 500)
		price += count * FEE_PER_500M


def item_fees(count):
	global price
	
	if count < BIG_ORDER:
		return
	
	for i in range(BIG_ORDER, (count + 1)):
		price += ITEM_FEE
	
	if count >= BULK_ORDER:
		price += BULK_FEE


def rush_multiplier(time):
	global price
	
	if time.weekday() != FRIDAY:
		return

	if time.hour in range(RUSH_HOUR_START, RUSH_HOUR_END):
   		price *= 1.2
	
