import uvicorn
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from services.routers import Users, Items

app = FastAPI(debug=True)

app.mount('/static', StaticFiles(directory="services/static"), name="static")

app.include_router(Users.router,prefix='/api/v1',tags=['users'])
app.include_router(Items.router,prefix='/api/v1',tags=['items'])

if __name__ == '__main__':
    uvicorn.run("app:app",host="192.168.18.80", port=5000, reload=True)
