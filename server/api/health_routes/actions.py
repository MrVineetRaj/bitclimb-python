from api.helper import generateApiResponse,generateError
from api.error_codes import ERROR_CODES
class Actions:
  @staticmethod
  async def healthCheck():
    return generateApiResponse(message="Server is up and running",statusCode=200,result=None)
  
  @staticmethod
  async def healthFailCheck():
    # raise Exception("Forced error")
    return generateError(message="Server is up and running",errorCode=ERROR_CODES.SERVICE_UNAVAILABLE,result=None)
