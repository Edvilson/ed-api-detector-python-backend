from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware
from app.config import settings
from app.logger import setup_logger
from app.database import Base, engine
from app.routes.auth_routes import router as auth_router
from app.routes.compare_routes import router as compare_router
from app.routes.plan_routes import router as plan_router

# importa models para criar tabelas
import app.models.user  # noqa
import app.models.comparison  # noqa
import app.models.plan  # noqa

docs_url = "/docs" if settings.ENVIRONMENT == "development" else None
redoc_url = "/redoc" if settings.ENVIRONMENT == "development" else None
app = FastAPI(title="Plagiarism Detector API", docs_url=docs_url, redoc_url=redoc_url)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

setup_logger()
Base.metadata.create_all(bind=engine)

app.include_router(auth_router, prefix="/api/auth", tags=["Auth"]) 
app.include_router(compare_router, prefix="/api", tags=["Compare"]) 
app.include_router(plan_router, prefix="/api", tags=["Plan"]) 
