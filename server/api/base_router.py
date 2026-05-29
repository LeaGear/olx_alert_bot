from fastapi import APIRouter

from server.api.v1.subscription_router import router as subscription_router

main_router = APIRouter()

# Объединяем все роутеры под одну крышу
main_router.include_router(subscription_router, prefix="/v1")
