import uvicorn, os
from fastapi import FastAPI
from fastapi.responses import FileResponse, Response
from tortoise.contrib.fastapi import register_tortoise

from apps.blogs.routers import router as blog_router
from apps.users.routers import router as user_router
from config import settings

app = FastAPI(docs_url="/swagger", debug=settings.DEBUG,title="Blogapp backend")

app.include_router(user_router)
app.include_router(blog_router)

@app.get(settings.MEDIA_URL+"/{file_path}",include_in_schema = False)
async def send_media_file(file_path, response: Response):
    file_path = os.path.join(settings.MEDIA_ROOT,file_path)
    if os.path.exists(file_path):
        return FileResponse(file_path)
    response.status_code = 404
    return {"error":"no media found"}


register_tortoise(
    app,
    # db_url=f"postgres://{settings.DB_USER}:{settings.DB_PASSWORD}@{settings.DB_HOST}:{settings.DB_PORT}/{settings.DB_NAME}",
    db_url=f"sqlite://./db.sqlite3",
    generate_schemas=True,
    modules={"models": ["apps.users.models", "apps.blogs.models"]},
    add_exception_handlers=True,
)

if __name__ == "__main__":
    uvicorn.run(
        "main:app", host=settings.HOST, port=settings.PORT, reload=settings.RELOAD
    )
