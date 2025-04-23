from config.constant import AI_PROVIDERS
from fastapi import APIRouter, status, \
    HTTPException
from fastapi.responses import JSONResponse
from providers.provider import AIProvider


router = APIRouter(
    prefix="/genai",
    tags=["GenAI API"]
)


class GenAI:
    """Generative AI endpoints"""

    @staticmethod
    @router.get("/text/{provider}/{prompt}", status_code=status.HTTP_200_OK)
    def text_generation(provider: str, prompt: str):
        """Text Generation API through AI Provider"""
        if not provider in AI_PROVIDERS:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Unsupported provider"
            )

        genai_model = AIProvider(provider=provider).factory_model()
        answer = genai_model.text_generation(prompt=prompt)

        return JSONResponse(
            content={"answer": answer},
            status_code=status.HTTP_200_OK
        )
