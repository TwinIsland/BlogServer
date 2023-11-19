import sys

from fastapi import FastAPI

from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware

from routers import post, tags, blog, auth, comment, visitor, media

from database import models
from database.database import engine
import os

from config import (
    VERSION,
    DESCRIPTION,
    SERVICE_NAME,
    STATIC_MOUNT_DIR,
    UPLOAD_MOUNT_DIR,
)

models.Base.metadata.create_all(bind=engine)

app = FastAPI(
    title=SERVICE_NAME,
    description=DESCRIPTION,
    version=VERSION,
    swagger_ui_parameters={"defaultModelsExpandDepth": -1},
)

if not os.path.isdir(STATIC_MOUNT_DIR):
    print(
        "\033[91m"
        "static mounting point detached, please re-download the source code from: "
        "https://github.com/TwinIsland/SuikaBlogSystem "
        "and drag the /static folder into the project directory"
        "\033[0m"
    )
    sys.exit(1)

if not os.path.isdir(UPLOAD_MOUNT_DIR):
    print(f"creating upload mount directory...", end="")
    os.mkdir(UPLOAD_MOUNT_DIR)
    print("\033[92mok!\033[0m")

app.mount("/static", StaticFiles(directory=STATIC_MOUNT_DIR), name='static')
app.mount("/upload", StaticFiles(directory=UPLOAD_MOUNT_DIR))

app.add_middleware(
    CORSMiddleware,
    allow_origins="*",
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

with open("static/ascii_logo", "r", encoding="UTF-8") as f:
    print("\n", f.read())
    print(f"Welcome to Suika Blog Service!\n" f"Version: {VERSION}\n")

app.include_router(blog.router, prefix="/blog", tags=["blog"])
app.include_router(post.router, prefix="/post", tags=["post"])
app.include_router(tags.router, prefix="/tag", tags=["tag"])
app.include_router(comment.router, prefix="/comment", tags=["comment"])
app.include_router(visitor.router, prefix="/visitor", tags=["visitor"])
app.include_router(media.router, prefix="/media", tags=["media"])
app.include_router(auth.router, prefix="/auth", tags=["auth"])


@app.get("/", include_in_schema=False)
async def index():
    """
    server index page

    """
    return FileResponse("static/service_index.html")
