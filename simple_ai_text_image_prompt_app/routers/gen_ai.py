from config.constant import AI_PROVIDERS
from fastapi import APIRouter, status, \
    HTTPException
from fastapi.responses import JSONResponse
from providers.provider import AIProvider
from pydantic import BaseModel, Field

router = APIRouter(
    prefix="/genai",
    tags=["GenAI API"]
)


class GenerationRequest(BaseModel):
    """Generation Request Serializer"""

    prompt: str = Field(min_length=10)


class GenAI:
    """Generative AI endpoints"""

    @staticmethod
    @router.post("/text/{provider}", status_code=status.HTTP_200_OK)
    def text_generation(
        provider: str,
        text_generation_request: GenerationRequest
    ):
        """Text Generation API through AI Provider"""

        if provider not in AI_PROVIDERS:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Unsupported provider"
            )

        genai_model = AIProvider(provider=provider).factory_model()
        answer = genai_model.text_generation(
            prompt=text_generation_request.prompt
        )

        return JSONResponse(
            content={"answer": answer},
            status_code=status.HTTP_200_OK
        )
    
    @staticmethod
    @router.post("/image/{provider}", status_code=status.HTTP_200_OK)
    def image_generation(
        provider: str,
        image_generation_request: GenerationRequest
    ):
        """Image Generation API through AI Provider"""

        if provider not in AI_PROVIDERS:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Unsupported provider"
            )
        
        genai_model = AIProvider(provider=provider).factory_model()
        image_responses = genai_model.image_generation(
            prompt=image_generation_request.prompt
        )

        if not image_responses:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Cannot generated any image"
            )
        
        return JSONResponse(
            content={"images": image_responses},
            status_code=status.HTTP_200_OK
        )
