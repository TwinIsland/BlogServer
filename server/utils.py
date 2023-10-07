from fastapi import Request
from jose import JWTError, jwt
from datetime import datetime
from config import SECRET_KEY, ALGORITHM


class Utils:
    @staticmethod
    def is_admin(request: Request):
        authorization_header = request.headers.get("Authorization")

        if not authorization_header or not authorization_header.lower().startswith(
                "bearer "
        ):
            return False

        token = authorization_header.split()[1]

        try:
            payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
            admin_username = payload.get("sub")

            if not admin_username:
                return False

            # Check if the token has expired
            expiration = datetime.utcfromtimestamp(payload.get("exp", 0))
            if datetime.utcnow() > expiration:
                return False

            return True

        except JWTError:
            return False
