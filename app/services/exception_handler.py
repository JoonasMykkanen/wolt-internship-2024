from starlette.status import HTTP_404_NOT_FOUND
from starlette.exceptions import HTTPException
from fastapi.responses import JSONResponse
from fastapi import Request

# Created to detect 404 error and giving user info about correct usage
# IF 404 RETURNS: message containing info and error message
# ELSE RETURNS: error message
def handle_not_found(request: Request, exception: HTTPException):
	if exception.status_code == HTTP_404_NOT_FOUND:
		return JSONResponse(
			status_code=HTTP_404_NOT_FOUND,
			content={"message": "Avaivable endpoint @ /api/delivery-fee"}
		)
	
	return JSONResponse(status_code=exception.status_code, content={"message": f"{exception.detail}"})


