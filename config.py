import bcrypt
from enum import Enum
import mistune
import hashlib
import re
from fastapi import Request, UploadFile, HTTPException


# HASH FUNCTION CONFIGURATION
SALT_LENGTH = 15
PASSWORD_ENCODE = "utf-8"

# SQL CONFIGURATION
MAX_OUTPUT_ITEM_NUM = 100
SQLALCHEMY_DATABASE_URL = "sqlite:///./sql_app.db"

# WEB ROUTER CONFIGURATION
STATIC_MOUNT_DIR = "static"
UPLOAD_MOUNT_DIR = "upload"

# BLOG SERVICE CONFIGURATION
VERSION = "1.0.0"
SERVICE_NAME = "Suika Blog Service"
DESCRIPTION = "A simple backend framework for blog system"

# AUTHORIZATION CONFIGURATION
SECRET_KEY = "8e01aa7373f9b0ebec337669cb27f924a634270622cfb21b4b2d35b13b7f6d9b"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

# FILE UPLOAD
FILE_RAND_EXT_LENGTH = 5
MAX_FILE_SIZE = 100 * 1024 * 1024  # 100 MB
SUPPORT_FILE_TYPE = ["jpg", "png", "webp", "mp3", "mp4", "zip", "pdf"]

# BACKEND SAFETY SETTING
SAFETY_STRICT = False
LOGIN_TIME_DELAY_SECOND = 2
COMMENT_GAP_SECOND = 120


class ExceptionLib:
    EMAIL_NOT_IN_FORMAT = HTTPException(400, "safety check failed: email not in format")
    URL_NOT_IN_FORMAT = HTTPException(400, "safety check failed: url not in format")


class Toolkit:
    @staticmethod
    def is_valid_email(email: str):
        # basic email validation
        pattern = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"

        return re.match(pattern, email) is not None

    @staticmethod
    def is_valid_url(url):
        # basic url validation
        url_pattern = re.compile(
            r"^(https?://)?([a-zA-Z0-9.-]+(\.[a-zA-Z]{2,})+)(:\d+)?(/[\w.-]*)*/?$"
        )
        return bool(url_pattern.match(url))


class RendererEnum(str, Enum):
    # declaring for rendering methods
    DEFAULT = "default"
    HUGE_TEXT_RENDER = "huge_text_render"
    # Add more enum values here for other renderers
    # ...


class Renderer:
    # implements for rendering methods
    DEFAULT_RENDERER_NAME = "default"

    def __init__(self):
        self.renderers = {
            "default": mistune.create_markdown(
                plugins=[
                    "strikethrough",
                    "footnotes",
                    "table",
                    "url",
                    "task_lists",
                    "math",
                ]
            ),
            "huge_text_render": self.huge_text_render,
            # Add more renderers here. After adding, update RendererEnum as well
            # ...
        }

    @staticmethod
    def huge_text_render(plain: str):
        # This is a renderer for DEMO only, rendering the plain string to be in h1 tag
        return f"<h1>{plain}</h1>"


class Service:
    @staticmethod
    def hash_password(password: str):
        # implement for hashing the password, the default method is slow but safe,
        # changing the check_password() method as well when modifying this method
        byte_password = bytes(password, PASSWORD_ENCODE)
        salt = bcrypt.gensalt(rounds=SALT_LENGTH)
        hashed_password = bcrypt.hashpw(byte_password, salt)
        return hashed_password.decode("utf-8")

    @staticmethod
    def check_password(password: str, hashed_password: str):
        # given the target & given hashed_password,
        # return the boolean indicate if the password is correct or not
        byte_password = bytes(password, PASSWORD_ENCODE)
        byte_hashed_password = bytes(hashed_password, PASSWORD_ENCODE)
        return bcrypt.checkpw(byte_password, byte_hashed_password)

    @staticmethod
    def get_avatar(email: str | None = None, url: str | None = None):
        # implementation for how to gain the avatar for visitors, default using
        # gravatar as avatar service.
        if not email and not url:
            return "/static/default_avatar.jpg"

        if email:
            email = email.strip().lower()
            hash_value = hashlib.md5(email.encode("utf-8")).hexdigest()

            # Construct the Gravatar URL
            gravatar_url = f"https://www.gravatar.com/avatar/{hash_value}"
            return gravatar_url
        return url

    @staticmethod
    def get_default_banner(_post_body):
        # input parameter include all field in PostCreate schema, generated everytime
        # when post getter been called, so keep the time complexity as low as possible
        return "/static/default_banner.jpg"

    @staticmethod
    def get_default_description(_post_body):
        # input parameter include all field in PostCreate schema, the content will be called everytime
        # when calling post getter, so keep the time complexity as low as possible
        return _post_body.content[: min(len(_post_body.content), 20)]

    @staticmethod
    def hash_visitor_inf(request: Request):
        # each visitor should have a unique hashed_info, this info will be used to identified user
        client_host = request.client.host
        hash_value = hashlib.md5(client_host.encode("utf-8")).hexdigest()
        return hash_value

    @staticmethod
    def upload_file(_file: UploadFile):
        # upload the file and return the url, return None if upload to local
        return None

    @staticmethod
    def generate_description(_post_body):
        # given PostCreate schema return the description generating method, return None if you use default
        # description (which generated by get_default_description() method in config), this method will be called
        # once when add new post, and the content will be written to database.
        return None
