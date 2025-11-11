from fastapi import FastAPI
from api.health_routes.main import registerRoutes as registerHealthRoutes


app = FastAPI(title="BitClimb Backend")

app.include_router(registerHealthRoutes(),prefix="/api/v1/health")