from fastapi import FastAPI
from app.middlewares.cors import setup_cors
from app.routes.contents.contents import contentsRouter
from app.routes.health.health import healthRouter

app = FastAPI()
setup_cors(app)
app.include_router(contentsRouter)
app.include_router(healthRouter)
