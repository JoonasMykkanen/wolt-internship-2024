from fastapi import FastAPI

from .routes.delivery import delivery_router

def create_app():
	app = FastAPI()

	app.include_router(delivery_router, prefix='/api')

	return app