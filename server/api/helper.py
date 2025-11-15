# from api.error_codes import ERROR_CODES
# from typing import Any

# class ApiResponse:
#   message:str
#   statusCode:int
#   result:any
#   success:bool
#   def __init__(self,message:str,statusCode:int,result:Any):
#     self.message = message
#     self.statusCode = statusCode
#     self.success = statusCode < 400
#     self.result = result
    


# class ErrorResponse:
#   message:str
#   statusCode:int
#   errorCode:ERROR_CODES
#   success:bool


#   def __init__(self, message: str, errorCode: ERROR_CODES, data: Any = None):
#       self.message = message
#       self.errorCode = errorCode
#       self.statusCode = errorCode.value  # because enums hold the int value
#       self.success = self.statusCode < 400
#       self.data = data



from api.error_codes import ERROR_CODES
from typing import Any
from pydantic import BaseModel
from starlette.responses import JSONResponse
from fastapi.encoders import jsonable_encoder


class ApiResponse(BaseModel):
    message: str
    statusCode: int
    result: Any
    success: bool

class ErrorResponse(BaseModel):
    message: str
    statusCode: int
    success: bool
    result: Any = None

async def AsyncApiHandler(handler: Any, *args, **kwargs):
    try:
      result = await handler(*args,**kwargs)
      if isinstance(result, ApiResponse) or isinstance(result,ErrorResponse):
        return JSONResponse(
            jsonable_encoder(result.model_dump()),
            status_code=result.statusCode
        )
      return result;
    except Exception as e:
      print(e)
      return JSONResponse(ErrorResponse(
          message=str(e),
          statusCode=ERROR_CODES.INTERNAL_SERVER_ERROR.value,
          success=False,
          result=None
      ).model_dump(),status_code=500)


def generateApiResponse(message:str,statusCode:int,result:Any)->ApiResponse:
  return ApiResponse(
      message=message,
      statusCode=statusCode,
      result=result,
      success=statusCode < 400
    )


def generateError( message: str, errorCode: ERROR_CODES, result: Any = None):
    return ErrorResponse(
       message=message,
       statusCode=errorCode.value,
       success=errorCode.value < 400,
       result=result
    )

