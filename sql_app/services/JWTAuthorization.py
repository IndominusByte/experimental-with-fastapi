import jwt, uuid, re
from fastapi import Header, HTTPException
from datetime import datetime, timezone, timedelta
from typing import Optional, Dict, Union

class AuthJWT:
    _EXPIRED_MINUTE_TIME = 1
    _SECRET_KEY = 'secretkey'
    _ALGORITHM = 'HS256'
    _TOKEN = None
    _DATA = None

    def __init__(self,Authorization: str = Header(None)):
        """
        Get header Authorization with format 'Bearer <JWT>' and verified token, when Authorization header exists

        :param Authorization: get Authorization from the header when class initialize
        """
        if Authorization:
            if re.match(r"Bearer\s",Authorization) and len(Authorization.split(' ')) == 2 and Authorization.split(' ')[1]:
                self._TOKEN = Authorization.split(' ')[1]
            else:
                raise HTTPException(status_code=422,detail="Bad Authorization header. Expected value 'Bearer <JWT>'")

            self._verified_token()

    @staticmethod
    def get_jwt_id() -> str:
        return str(uuid.uuid4())

    @staticmethod
    def get_int_from_datetime(value: datetime) -> int:
        """
        :param value: datetime with or without timezone, if don't contains timezone
                      it will managed as it is UTC
        :return: Seconds since the Epoch
        """
        if not isinstance(value, datetime):  # pragma: no cover
            raise TypeError('a datetime is required')
        return int(value.timestamp())

    @staticmethod
    def create_token(identity: int, type_token: str, fresh: Optional[bool] = False) -> str:
        """
        This function create token for access_token and refresh_token, when type_token
        is access add a fresh key to dictionary payload

        :param identity: Identifier for who this token is for example id or username from database.
        :param type_token: for indicate token is access_token or refresh_token
        :param fresh: Optional when token is access_token this param required

        :return: Encoded token
        """
        if type_token not in ['access','refresh']:
            raise ValueError("Type token must be between access or refresh")

        payload = {
            "iat": AuthJWT.get_int_from_datetime(datetime.now(timezone.utc)),
            "nbf": AuthJWT.get_int_from_datetime(datetime.now(timezone.utc)),
            "jti": AuthJWT.get_jwt_id(),
            "exp": AuthJWT.get_int_from_datetime(datetime.now(timezone.utc) +
                timedelta(minutes=AuthJWT._EXPIRED_MINUTE_TIME)),
            "identity": identity,
            "type": type_token
        }

        # for access_token only fresh needed
        if type_token == 'access':
            payload['fresh'] = fresh

        return jwt.encode(payload,AuthJWT._SECRET_KEY,algorithm=AuthJWT._ALGORITHM)

    def _verified_token(self) -> None:
        """
        Verified token and catch all error from jwt package
        """
        try:
            self._DATA = jwt.decode(self._TOKEN,self._SECRET_KEY,algorithms=self._ALGORITHM)
        except jwt.ExpiredSignatureError as err:
            raise HTTPException(status_code=422,detail=str(err))
        except jwt.DecodeError as err:
            raise HTTPException(status_code=422,detail=str(err))
        except jwt.InvalidAlgorithmError as err:
            raise HTTPException(status_code=422,detail=str(err))
        except jwt.InvalidKeyError as err:
            raise HTTPException(status_code=422,detail=str(err))
        except jwt.InvalidTokenError as err:
            raise HTTPException(status_code=422,detail=str(err))
        except jwt.InvalidIssuerError as err:
            raise HTTPException(status_code=422,detail=str(err))
        except jwt.InvalidAudienceError as err:
            raise HTTPException(status_code=422,detail=str(err))
        except jwt.InvalidIssuedAtError as err:
            raise HTTPException(status_code=422,detail=str(err))
        except jwt.InvalidSignatureError as err:
            raise HTTPException(status_code=422,detail=str(err))
        except jwt.ImmatureSignatureError as err:
            raise HTTPException(status_code=422,detail=str(err))
        except jwt.MissingRequiredClaimError as err:
            raise HTTPException(status_code=422,detail=str(err))

    @staticmethod
    def create_access_token(identity: int, type_token: str, fresh: Optional[bool] = False) -> str:
        return AuthJWT.create_token(identity,type_token,fresh)

    @staticmethod
    def create_refresh_token(identity: int, type_token: str) -> str:
        return AuthJWT.create_token(identity,type_token)

    def jwt_required(self) -> None:
        if not self._DATA:
            raise HTTPException(status_code=401,detail="Missing Authorization Header")

    def jwt_optional(self) -> None:
        pass

    def jwt_refresh_token_required(self) -> None:
        if not self._DATA:
            raise HTTPException(status_code=401,detail="Missing Authorization Header")

    def fresh_jwt_required(self) -> None:
        if not self._DATA:
            raise HTTPException(status_code=401,detail="Missing Authorization Header")

    @property
    def get_raw_jwt(self) -> Optional[Dict[str,Union[str,int,bool]]]:
        if self._DATA:
            return self._DATA
        return None

    @property
    def get_jti(self) -> Optional[str]:
        if self._DATA:
            return self._DATA['jti']
        return None

    @property
    def get_jwt_identity(self) -> Optional[Union[str,int]]:
        if self._DATA:
            return self._DATA['identity']
        return None
