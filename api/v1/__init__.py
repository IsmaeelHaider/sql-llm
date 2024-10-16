from fastapi import APIRouter
from api.v1.llm import llm_router

v1_router = APIRouter(prefix="/v1")

v1_router.include_router(llm_router)
