from fastapi import APIRouter
from api.health_routes.actions import Actions
from api.helper import AsyncApiHandler


def registerRoutes():
  router = APIRouter()

  @router.get("/")
  async def health_check():
    return await AsyncApiHandler(Actions.healthCheck)
  
  @router.get("/fail")
  async def health_fail_check():
    return await AsyncApiHandler(Actions.healthFailCheck)


  return router