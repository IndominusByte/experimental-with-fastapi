import uvicorn
from fastapi import FastAPI, Depends
from fastapi.staticfiles import StaticFiles
from dotenv import load_dotenv
from services.routers import Users, Items
from services.JWTAuthorization import AuthJWT

app = FastAPI(debug=True)

load_dotenv()

app.mount('/static', StaticFiles(directory="services/static"), name="static")

app.include_router(Users.router,prefix='/api/v1',tags=['users'])
app.include_router(Items.router,prefix='/api/v1',tags=['items'])

# MAKE JWT SYSTEM EXAMPLE
@app.get('/api/v1/jwt-create')
def test_jwt():
    access_token = AuthJWT.create_access_token(identity=5,type_token="access",fresh=True)
    refresh_token = AuthJWT.create_refresh_token(identity=5,type_token="refresh")
    # print(AuthJWT.get_jti(encoded_token=access_token))
    return {"access_token": access_token, "refresh_token": refresh_token}

@app.get('/api/v1/jwt-required')
def check_jwt_required(Authorize: AuthJWT = Depends()):
    Authorize.jwt_required()

@app.get('/api/v1/jwt-optional')
def check_jwt_optional(Authorize: AuthJWT = Depends()):
    Authorize.jwt_optional()

@app.get('/api/v1/jwt-refresh-required')
def check_jwt_refresh_required(Authorize: AuthJWT = Depends()):
    Authorize.jwt_refresh_token_required()

@app.get('/api/v1/jwt-fresh-required')
def check_jwt_fresh(Authorize: AuthJWT = Depends()):
    Authorize.fresh_jwt_required()


if __name__ == '__main__':
    uvicorn.run("app:app",host="192.168.18.82", port=5000, reload=True)
