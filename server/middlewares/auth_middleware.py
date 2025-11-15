from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import JSONResponse
from api.helper import generateError;
from api.error_codes import ERROR_CODES;
from api.auth_routes.oauth import oauth
from sqlalchemy import select
from db.models import User
from db import async_session
from core.utility import to_dict
PUBLIC_PATHS = {
    "/api/v1/auth/github",
    "/api/v1/auth/callback/github",
    "/api/v1/health",
    "/api/v1/health/fail",
    "/docs",
    "/",
    "/openapi.json"
}

class AuthMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request, call_next):
        path = request.url.path

        # Allow public paths
        if path in PUBLIC_PATHS or path.startswith("/docs"):
            return await call_next(request)

        # Check session auth
        token = request.session.get("github_token")

        if not token:
             return JSONResponse(generateError(message="Unauthorized",errorCode=ERROR_CODES.UNAUTHORIZED,result=None).model_dump(),status_code=401)
      
            
        
        # Fetch user from DB
        async with async_session() as db:
            github_id = token.get("userinfo", {}).get("id")  # depends on your token format
            user = (await oauth.github.get("user", token=token)).json()
            emails = (await oauth.github.get("user/emails", token=token)).json()

            avatar = user["avatar_url"]

            primary_email = next(
              (e["email"] for e in emails if e.get("primary")),
              None
            )
            result = await db.execute(select(User).where(User.email == primary_email))
            db_user = result.scalar_one_or_none()

            if not db_user:
                return JSONResponse(generateError(message="Unauthorized",errorCode=ERROR_CODES.UNAUTHORIZED,result=None).model_dump(),status_code=401)
      
            
            request.state.user = {**to_dict(db_user),"avatar":avatar}

        # Continue request
        return await call_next(request)
