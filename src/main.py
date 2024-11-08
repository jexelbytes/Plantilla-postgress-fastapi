from config import swagger_config, summary, description, is_develop
from sqlalchemy_utils import database_exists, create_database
from config import host, port, is_develop, swagger_config, title
from fastapi.openapi.docs import get_swagger_ui_html
from auth.base_auth import get_current_username
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import RedirectResponse
from fastapi import FastAPI, Depends
from database import engine
from services.auto_alembic import Automatic_Alembic

if not database_exists(engine.url):
    create_database(engine.url)
    
app = FastAPI(
    summary=summary,
    description=description,
    title=title,
    docs_url=None,
    redoc_url=None,
    openapi_url=None
)

@app.get("/api/v3/healthcheck", tags=["Healthcheck"])
async def healthcheck():
    return "alive"

@app.get("/", include_in_schema=False)
async def go_to_swagger():
    return RedirectResponse(url=f'/docs')

@app.get("/docs", include_in_schema=False)
async def get_swagger_documentation(username: str = Depends(get_current_username)):
    return get_swagger_ui_html(
        title=title,
        swagger_ui_parameters=swagger_config,
        openapi_url="/openapi.json"
    )

@app.get("/openapi.json", include_in_schema=False)
async def openapi(username: str = Depends(get_current_username)):
    return app.openapi()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Routers ---------------------------------------------------------------------------------------------------------------
from auth.routes import user_router
app.include_router(user_router, prefix="/api",tags=["Auth"])

# END Routers -----------------------------------------------------------------------------------------------------------

if is_develop:
    from debug.router import debug_router
    app.include_router(debug_router, tags=["Debug"], prefix="/api")

if __name__ == '__main__':
    import uvicorn
    
    alembic = Automatic_Alembic()
    print(alembic.automatic_migrate())
    
    if is_develop:
        uvicorn.run("main:app", host=host, port=port, reload=True)
    else:
        uvicorn.run("main:app", host=host, port=port)