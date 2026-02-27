import uvicorn
from contextlib import asynccontextmanager
from fastapi import FastAPI
from app.api.v1.router import api_router
from app.core.config import settings

@asynccontextmanager
async def lifespan(app: FastAPI):
    print(f"Starting {settings.PROJECT_NAME} on {settings.HOST}:{settings.PORT}")
    yield
    print(f"Shutting down {settings.PROJECT_NAME}")

def create_app() -> FastAPI:
    app = FastAPI(
        title=settings.PROJECT_NAME,
        lifespan=lifespan
    )
    
    app.include_router(api_router, prefix="/v1")
    
    return app

app = create_app()

def main():
    uvicorn.run(
        "app.main:app", 
        host=settings.HOST, 
        port=settings.PORT, 
        reload=True
    )

if __name__ == "__main__":
    main()
