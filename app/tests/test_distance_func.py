import pytest
import time

FIRST_KM_FEE = 200	# snt (2 eur)
FEE_PER_500M = 100	# snt (1 eur)

price = 0

def new_func(distance):
	global price
	
	price += FIRST_KM_FEE
	remaining_distance = distance - 1000
	
	if remaining_distance > 0:
		count = max(0, (remaining_distance + 499) // 500)
		price += count * FEE_PER_500M

def og_func(distance):
	global price
	
	price += FIRST_KM_FEE
	remaining_distance = distance - 1000
	
	while (remaining_distance > 0):
		remaining_distance -= 500
		price += FEE_PER_500M



@pytest.mark.parametrize("distance, description", [
    (500, "tiny"),
	(3500, "small"),
    (8000, "normal"),
    (25000, "large"),
	(500000, "extreme")
])
def test_functions(distance, description):
	global price

	start_time = time.perf_counter()
	og_func(distance)
	og_duration = time.perf_counter() - start_time

	price = 0

	start_time = time.perf_counter()
	new_func(distance)
	new_duration = time.perf_counter() - start_time

	if og_duration > 0:
		speed_improvement = ((og_duration - new_duration) / og_duration) * 100
		print(f"\n Speed improvement for {description} ({distance}m): {speed_improvement:.2f}%")