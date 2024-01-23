# NOTE: For this scope, I feel akward for including this many constants
# and even making code maybe harder to read? unsure but feel weird about it
# Anyways since scalability is one concern, I feel these are a must.
# Lets say there are 5 files and 15 functions assuming the rush hour is when it is
# but company policy changes? Sooo thats why they are here.
# Also I would move them to /utils/constants.py if they were used in more than 1 place

# CONSTANTS
FREE_DELIVERY_LIMIT = 20000	# snt (200 eur)
FREE_DELIVERY = 0			# snt (0 eur)
SMALL_ORDER = 1000			# snt (10 eur)
FIRST_KM_FEE = 200			# snt (2 eur)
MAX_FEE = 1500				# snt (15 eur)
FEE_PER_500M = 100			# snt (1 eur)
ITEM_FEE = 50				# snt (0,5 eur)
BULK_FEE = 120				# snt (1,2 eur)

BULK_ORDER = 12 			# pcs
BIG_ORDER = 5				# pcs
FRIDAY = 4					# index in datetime map of weekdays
RUSH_HOUR_START = 15		# starting hour with 24h clock
RUSH_HOUR_END = 19			# ending hour with 24h clock



# actual return of the service
price = 0

def calculate_fee(data):
	global price

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
	
	return price



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


# This function could basically be one liner but for readibility left it for a bit longer version.
# Also direct comparison shouldn theory be faster than calling for range() but with such small
# range, difference will be negligible and I like the readibility of this.
def rush_multiplier(time):
	global price
	
	if time.weekday() != FRIDAY:
		return

	if time.hour in range(RUSH_HOUR_START, RUSH_HOUR_END):
   		price *= 1.2
	


