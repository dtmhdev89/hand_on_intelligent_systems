from fastapi import FastAPI
from simple_ai_text_image_prompt_app.routers.gen_ai import router as gen_ai_router

app = FastAPI()

app.include_router(gen_ai_router)
