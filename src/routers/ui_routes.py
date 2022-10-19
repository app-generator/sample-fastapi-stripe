from fastapi import APIRouter, Request, status
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from pathlib import Path
import http3

from src import app, schemas

router = APIRouter(
    tags = ['User Interface']
)

BASE_PATH = Path(__file__).resolve().parent
TEMPLATES = Jinja2Templates(directory=str(BASE_PATH / "../templates"))

@router.get("/", status_code=status.HTTP_200_OK)
async def index(request: Request, response_model=HTMLResponse):
    return TEMPLATES.TemplateResponse("pages/index.html", {"request" : request})


@router.get("/products", status_code=status.HTTP_200_OK)
async def products_index(request: Request, response_model=HTMLResponse):
    featured_product_id = 0
    base_url = request.base_url
    products_url = app.product_router.url_path_for("get_product", id=featured_product_id)
    request_url = base_url.__str__() + products_url.__str__()[1:]

    http3client = http3.AsyncClient()
    response = await http3client.get(request_url)

    featured_product = response.json()

    print (featured_product)



    return TEMPLATES.TemplateResponse("ecommerce/index.html", {
        "request" : request,
        "featured_product" : featured_product
        })


