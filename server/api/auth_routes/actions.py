from fastapi import FastAPI, Request
from api.helper import generateApiResponse,generateError
from api.error_codes import ERROR_CODES
from .oauth import oauth
from sqlalchemy import select
from db.models import User
from core.utility import to_dict
class Actions:
  @staticmethod
  async def login_github(request:Request):
    redirect_uri = request.url_for("github_callback")
    return await oauth.github.authorize_redirect(request, redirect_uri)
  
  @staticmethod
  async def github_callback(request:Request,db):
    token = await oauth.github.authorize_access_token(request)
    user = (await oauth.github.get("user", token=token)).json()
    emails = (await oauth.github.get("user/emails", token=token)).json()
    request.session["github_token"] = token
    
    

    name = user["name"]
    avatar = user["avatar_url"]
    primary_email = next(
        (e["email"] for e in emails if e.get("primary")),
        None
    )

    # print(name,avatar,primary_email)
    db_user = await db.execute(select(User).where(User.email == primary_email))
    db_user = db_user.scalar_one_or_none()

    if not db_user:
      db_user = User(
          name=name,
          email=primary_email
      )
      db.add(db_user)
      await db.commit()

    return generateApiResponse(
        message="Logged in",
        statusCode=201,
        # result={**db_user,"avatar":avatar}
        result=None
      )
  
  async def get_profile(request:Request,db):
    token = request.session.get("github_token")
    user = (await oauth.github.get("user", token=token)).json()
    emails = (await oauth.github.get("user/emails", token=token)).json()

    avatar = user["avatar_url"]

    primary_email = next(
      (e["email"] for e in emails if e.get("primary")),
      None
    )

    db_user = await db.execute(select(User).where(User.email == primary_email))
    db_user = db_user.scalar_one_or_none()

    print(to_dict(db_user))
    if not db_user:
      return generateError(
        message="Not a valid user",
        errorCode=ERROR_CODES.UNAUTHORIZED,
        result=None
      )
    

    return generateApiResponse(
        message="Profile Fetched",
        statusCode=200,
        result={**to_dict(db_user),"avatar":avatar}
      )