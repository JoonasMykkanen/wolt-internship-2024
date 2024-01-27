# Wolt Summer 2024 Engineering Internships

### How to run (will need python3 instsalled)

Download the package
```
git clone https://github.com/JoonasMykkanen/wolt-internship-2024.git
```

Install requirements
```
pip3 -r requirements.txt
```

Run the App
```
python3 run.py
```

### Or build and run with Docker

```
docker compose up --build
```


### My submission for __BACKEND__ roles with Python and FastAPI.

Originally was going to implement with Flask but since Pydantic models offered nice validation and they are build with
FastAPI, decided to learn more of that. Have no prior experience with FastAPI except for Wolt's workshop @ Hive with it
that was kindly hosted by you.



## Structure

App has been divided into modules and these can be modified independetly from each other. You can add or remove them
without breaking the App. Since subject only has one module, it seems a bit overkill.

* run.py - starts the program
* /tests - individual tests, can be ran with ```pytest -s tests/__FILE__```
* /app - Where everything ties together
* /routes - set up routers to handle paths like '/api' or '/'
* /services - Logic for routers to use, also could include databases, external api's etc...

#### Will answer at ```/api/delivery-fee```

Expected input
```
{"cart_value": [INT], "delivery_distance": [INT], "number_of_items": [INT], "time": [ISO8601 TIMESTAMP]}
```

On success wil return following JSON object
```
{"delivery_fee": [INT]}
```

## Status Codes

| Status Code | Description |
| :--- | :--- |
| 200 | `OK` |
| 404 | `NOT FOUND` |
| 422 | `UNPROCESSABLE ENTITY` |
| 500 | `INTERNAL SERVER ERROR` |


## Notes

### price_in_distance() function and it's two different states
Ok, let me start with the original implementation...
```
def price_in_distance(distance):
	global price
	
	price += FIRST_KM_FEE
	remaining_distance = distance - 1000
	
	while (remaining_distance > 0):
		distance -= 500
		price += FEE_PER_500M
```
Problem is with the loop, it has time complexity ```O(n)``` and could potentially be bottleneck later on. ( a lot of big distance delivieries )

When looking at it for the second time, I had an idea of division and using it like **COUNT * FEE** but was not sure how to handle remainders.
After a while, and from a suggestion of **GPT** (yes, want to be clear, use of the logic to add 499 and // operator was from GPT) got some
interesting results. Now time complexity is ```O(1)```.
With this scale it's quite insignificant difference but I thought this was interesting, with such a small change to implementation, there
was __MAJOR__ difference to performance in precentages atleast.

Refactored function:

```
def price_in_distance(distance):
	global price
	
	price += FIRST_KM_FEE
	remaining_distance = distance - 1000
	
	if remaining_distance > 0:
		count = max(0, (remaining_distance + 499) // 500)
		price += count * FEE_PER_500M
```

I created tests to showcase this during my process of figuring this out. I was unaware of Pythons ```//``` operator and it's potential use case for this.
If nothing else comes off of this assigment, I walk out with one more tool in my toolbox.

```pytest -s tests/test_distance_func.py```

With these, you can see that with bigger distances, performance gain can be up to 98%.. :D But that is with 500km delivery distance so not realistic.
More realistic results are from tiny, small and normal ranges. With small ranges the loop was sometimes faster, unsure why.
Tiny ```from 15% to 40%```
Small ```from -10% to 10%```
Normal ```from 35% to 45%```

### Other tests
For other tests I am accessing my endpoint with a lot of different data, valid and invalid.



### Other notes
I do have other Python backend project's going on, they are on my public github and you should definitely check them out!
I started my backend with Node @ Helsinki Universitys FullStack Open but am most interested on Python currently.
```https://github.com/JoonasMykkanen```
