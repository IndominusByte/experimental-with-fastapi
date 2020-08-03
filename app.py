import uvicorn, socket
from typing import Optional, List
from pydantic import BaseModel, Field
from fastapi.middleware.cors import CORSMiddleware
from fastapi import (
    FastAPI,
    Query,
    Path,
    Depends,
    File,
    UploadFile,
    Form,
    HTTPException,
    Request
)

def get_ip_address():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(("8.8.8.8", 80))
    return s.getsockname()[0]


app = FastAPI(debug=True)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://192.168.18.80:8080"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Handles GZip responses for any request that includes "gzip" in the Accept-Encoding header
# from fastapi.middleware.gzip import GZipMiddleware
# app.add_middleware(GZipMiddleware, minimum_size=1000)

# Enforces that all incoming requests have a correctly set Host header,
# in order to guard against HTTP Host Header attacks.
# from fastapi.middleware.trustedhost import TrustedHostMiddleware
# app.add_middleware(TrustedHostMiddleware,allowed_hosts=["192.168.18.80:5000"])

# Any incoming requests to http or ws will be redirected to the secure scheme instead
# from fastapi.middleware.httpsredirect import HTTPSRedirectMiddleware
# app.add_middleware(HTTPSRedirectMiddleware)

@app.get('/', status_code=200)
async def home():
    return {"hello":"world"}

class Items(BaseModel):
    name: str = Field(...,min_length=1)
    description: Optional[str] = None
    price: float = Field(...,gt=1)
    tax: Optional[float] = Field(None,gt=1)

    # example valid data for docs
    class Config:
        schema_extra = {
            "example": {
                "name": "Foo",
                "description": "A very nice Item",
                "price": 35.4,
                "tax": 3.2,
            }
        }

class User(BaseModel):
    username: str
    full_name: Optional[str] = None


@app.put('/items/{item_id}', status_code=200)
async def items(
        items: Items,
        user: User,
        request: Request,
        item_id: int = Path(...,ge=2),
        q: Optional[str] = Query(None,min_length=2)):

    results = {"item_id": item_id, "items": items, "user": user, "ip": request.client.host}
    if q:
        results['q'] = q
    return results

# tags for grouping endpoint to docs

# NOTE: remember install python-multipart
# use uploadfile type hinting instead byte
# detail advantages check documentation about request files
@app.post('/upload-single-file', status_code=201, tags=['upload-file'])
async def single_file(file: UploadFile = File(...), name: str = Form(...)):
    """
    Docstring will be show in docs
    """
    return {"filename": file.filename,"name": name}

# upload multiple file
@app.post('/multiple-files', status_code=201, tags=['upload-file'])
async def multiple_file(files: List[UploadFile] = File(...)):
    return {"filenames": [file.filename for file in files]}

# handling error
@app.get('/user/{id}')
async def user(id: int = Path(...)):
    if id not in [20,30]:
        raise HTTPException(status_code=404,detail="id not found")
    return id

# Classes as dependencies
class CommonQueryParams:
    def __init__(self, q: Optional[str] = None, skip: int = 0, limit: int = 100):
        self.q = q
        self.skip = skip
        self.limit = limit

@app.get('/class-as-dependencies', status_code=200)
async def class_as_dependencies(common: CommonQueryParams = Depends()):
    res = {"skip": common.skip,"limit": common.limit}
    if common.q:
        res['q'] = common.q
    return res

from fastapi.responses import RedirectResponse, StreamingResponse
# custom response
@app.get('/redirect-to-google')
async def go_to_google():
    return RedirectResponse("https://www.google.com/")

@app.get('/intro-automatch')
def automath():
    video = open('intro.mov', mode="rb")
    return StreamingResponse(video, media_type="video/mp4")

# Advanced Dependencies
class FixedContentQueryChecker:
    def __init__(self,content: str):
        self.content = content

    def __call__(self,q: str = Query(..., min_length=1)):
        if q:
            return self.content in q
        return False


checker = FixedContentQueryChecker("bar")

@app.get('/query-checker', status_code=200)
async def query_checker(fixed_content: bool = Depends(checker)):
    return {"fixed_content": fixed_content}

# SIMPLE EXAMPLE async await
async def lol():
    return [x for x in range(100)]

@app.get('/test-await',status_code=200)
async def test_await():
    results = await lol()
    return results

"""
Sub Applications - Mounts
"Mounting" means adding a completely "independent" application in a specific path,
with separate documentation and added prefix to the URL path
"""
subapi = FastAPI()

@subapi.get("/sub")
def read_sub():
    return {"message": "Hello World from sub API"}


app.mount("/subapi", subapi)


if __name__ == '__main__':
    uvicorn.run("app:app",host=get_ip_address(), port=5000, reload=True)
