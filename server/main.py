import core.env_conf 
from fastapi import FastAPI
from contextlib import asynccontextmanager
from db import engine,models
from fastapi.responses import RedirectResponse


from api.health_routes import registerRoutes as registerHealthRoutes
from api.auth_routes import registerRoutes as registerAuthRoutes

from starlette.middleware.sessions import SessionMiddleware


@asynccontextmanager
async def lifespan(app: FastAPI):
    # STARTUP
    print("Starting app...")
    async with engine.begin() as conn:
        await conn.run_sync(models.Base.metadata.create_all)

    # If you need DB init / migrations:
    # async with engine.begin() as conn:
    #     await conn.run_sync(models.Base.metadata.create_all)

    yield

    # SHUTDOWN
    print("Shutting down app...")

app = FastAPI(title="BitClimb Backend",lifespan=lifespan)


async def startup():
    async with engine.begin() as conn:
        await conn.run_sync(models.Base.metadata.create_all)

app.add_middleware(
    SessionMiddleware,
    secret_key="some-super-secret-key"  # keep this env-based in prod
)
@app.get("/")
def redirect_to_docs():
  return RedirectResponse(url="/docs")


app.include_router(registerHealthRoutes(),prefix="/api/v1/health")
app.include_router(registerAuthRoutes(),prefix="/api/v1/auth")