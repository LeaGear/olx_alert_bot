from fastapi import APIRouter

from server.api.v1.subscription_router import router as subscription_router
from server.api.v1.parser_router import router as parser_router
from server.config import API_VERSION


main_router = APIRouter()

# Connect all routers in one main
main_router.include_router(subscription_router, prefix=API_VERSION)
main_router.include_router(parser_router, prefix=API_VERSION)
