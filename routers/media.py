import os
import string
import random
from typing import List, Optional
from fastapi import APIRouter, UploadFile, File, Depends
from sqlalchemy.orm import Session
from pydantic import BaseModel
from config import (
    MAX_FILE_SIZE,
    SUPPORT_FILE_TYPE,
    UPLOAD_MOUNT_DIR,
    FILE_RAND_EXT_LENGTH,
    Service,
    Toolkit,
    SAFETY_STRICT,
    ExceptionLib,
)

from database import crud
from database import schemas

from dependencies import get_db, is_admin

router = APIRouter()


class RemoteMedia(BaseModel):
    name: Optional[str] = None
    url: str


def generate_random_file_ext():
    characters = string.ascii_letters + string.digits
    random_string = "".join(random.choices(characters, k=FILE_RAND_EXT_LENGTH))
    return random_string


# Function to check file size and type
def is_file_valid(file: UploadFile) -> bool:
    _, file_extension = os.path.splitext(file.filename)
    if file_extension[1:] not in SUPPORT_FILE_TYPE:
        return False
    if file.size > MAX_FILE_SIZE:
        return False
    return True


@router.post(
    "/upload/", response_model=list[schemas.Media], dependencies=[Depends(is_admin)]
)
async def upload_files(
    post_id: int, files: List[UploadFile] = File(...), db: Session = Depends(get_db)
):
    uploaded_files = []
    for file in files:
        if is_file_valid(file):
            # attempt to upload file via user-defined method
            remote_url = Service.upload_file(_file=file)
            if remote_url:
                return add_remote_media(post_id=post_id, remote_url=remote_url, db=db)

            # upload locally
            local_filename, ext = os.path.splitext(file.filename)
            local_filename += f"-{generate_random_file_ext()}{ext}"
            file_dir = os.path.join(UPLOAD_MOUNT_DIR, str(post_id))

            if not os.path.isdir(file_dir):
                os.mkdir(file_dir)

            file_path = os.path.join(UPLOAD_MOUNT_DIR, str(post_id), local_filename)
            with open(file_path, "wb") as f:
                while chunk := await file.read(1024):
                    f.write(chunk)

            media_attr = {"size": file.size, "is_local": True, "name": local_filename}

            db_media = crud.add_media(
                db=db, media=schemas.MediaCreate(**media_attr), post_id=post_id
            )

            uploaded_files.append(db_media)
    return uploaded_files


def add_remote_media(post_id: int, remote_url: str, db: Session = Depends(get_db)):
    if SAFETY_STRICT:
        if not Toolkit.is_valid_url(remote_url):
            raise ExceptionLib.URL_NOT_IN_FORMAT

    media_attr = {"is_local": False, "remote_url": remote_url}

    return crud.add_media(
        db=db, media=schemas.MediaCreate(**media_attr), post_id=post_id
    )
