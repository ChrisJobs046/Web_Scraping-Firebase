from fastapi import APIRouter
from service.web_scraping import webscrapingRoutes



router = APIRouter()

router.include_router(webscrapingRoutes.router, prefix="/webscraping", tags=["Web Scraping"])