from fastapi import FastAPI
from routers.gen_ai import router as gen_ai_router

app = FastAPI()

app.include_router(gen_ai_router)
