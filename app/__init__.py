from starlette.exceptions import HTTPException
from fastapi import FastAPI

from .services.exception_handler import handle_not_found
from .routes.delivery import delivery_router

def create_app():
	app = FastAPI()

	app.add_exception_handler(HTTPException, handle_not_found)

	app.include_router(delivery_router, prefix='/api')


	return app