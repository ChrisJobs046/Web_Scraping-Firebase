from fastapi import APIRouter
from .controller import *

router = APIRouter()


@router.get("/webscraping")
def get_webscraping_routes():
    return web_scraping_routes()