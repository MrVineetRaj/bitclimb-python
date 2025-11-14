# health_routes/main.py
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import APIRouter, Request,Depends
from .actions import Actions
from api.helper import AsyncApiHandler
from db import get_db


def registerRoutes():
  router = APIRouter()

  @router.get("/github")
  async def login_github(request:Request):
    return await AsyncApiHandler(Actions.login_github,request)
  
  @router.get("/callback/github")
  async def github_callback(request: Request, db: AsyncSession = Depends(get_db)):
    return await AsyncApiHandler(Actions.github_callback, request,db)
  
  @router.get("/profile")
  async def get_profile(request:Request,db: AsyncSession = Depends(get_db)):
    return await AsyncApiHandler(Actions.get_profile,request,db)


  return router