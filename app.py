import uvicorn
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
    HTTPException
)

app = FastAPI(debug=True)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://192.168.18.80:8080"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

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
        item_id: int = Path(...,ge=2),
        q: Optional[str] = Query(None,min_length=2)):

    results = {"item_id": item_id, "items": items, "user": user}
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


if __name__ == '__main__':
    uvicorn.run("app:app",host="192.168.18.80", port=5000, reload=True)
